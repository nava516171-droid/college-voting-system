from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
import base64
from app.database import get_db
from app.models.user import User
from app.models.face import FaceEncoding
from app.schemas.face import FaceRegisterRequest, FaceVerifyRequest, FaceStatusResponse
from app.utils.security import get_current_user
from app.utils.face_recognition_util import (
    encode_face_from_image,
    serialize_face_encoding,
    deserialize_face_encoding,
    verify_face_from_stored_encoding
)

router = APIRouter(prefix="/api/face", tags=["face-recognition"])


@router.post("/register")
def register_face(
    request: FaceRegisterRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register user's face for authentication"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image data"
        )
    
    # Encode face from image
    face_encoding, confidence_score, success = encode_face_from_image(image_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face detected in image. Please provide a clear face photo."
        )
    
    if confidence_score < 0.4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Face quality too low. Please provide a clearer image."
        )
    
    # Check if user already has face registered
    existing_face = db.query(FaceEncoding).filter(
        FaceEncoding.user_id == current_user.id
    ).first()
    
    if existing_face:
        # Update existing face
        existing_face.face_encoding = serialize_face_encoding(face_encoding)
        existing_face.confidence_score = confidence_score
        existing_face.is_verified = "verified"
        existing_face.verified_at = datetime.utcnow()
        db.commit()
        return {
            "message": "Face updated successfully",
            "user_id": current_user.id,
            "status": "verified"
        }
    
    # Create new face encoding
    face_record = FaceEncoding(
        user_id=current_user.id,
        face_encoding=serialize_face_encoding(face_encoding),
        face_image=image_data,
        confidence_score=confidence_score,
        is_verified="verified",
        verified_at=datetime.utcnow()
    )
    
    db.add(face_record)
    db.commit()
    db.refresh(face_record)
    
    return {
        "message": "Face registered successfully",
        "user_id": current_user.id,
        "status": "verified"
    }


@router.post("/verify")
def verify_face(
    request: FaceVerifyRequest,
    db: Session = Depends(get_db)
):
    """Verify user's face for voting"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image data"
        )
    
    # First, encode the provided face
    provided_encoding, confidence, success = encode_face_from_image(image_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face detected in image"
        )
    
    # Try to find matching user by face
    all_face_encodings = db.query(FaceEncoding).filter(
        FaceEncoding.is_verified == "verified"
    ).all()
    
    matched_user = None
    matched_distance = 1.0
    
    for face_record in all_face_encodings:
        stored_encoding = deserialize_face_encoding(face_record.face_encoding)
        is_match, distance = verify_face_from_stored_encoding(
            image_data, 
            stored_encoding
        )
        
        if is_match and distance < matched_distance:
            matched_user = face_record.user
            matched_distance = distance
    
    if not matched_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face not recognized. Please register your face first."
        )
    
    # Update last used time
    face_record = db.query(FaceEncoding).filter(
        FaceEncoding.user_id == matched_user.id
    ).first()
    
    if face_record:
        face_record.last_used_at = datetime.utcnow()
        db.commit()
    
    return {
        "is_match": True,
        "user_id": matched_user.id,
        "user_email": matched_user.email,
        "confidence_distance": float(matched_distance),
        "message": "Face verified successfully",
        "verified": True
    }


@router.post("/verify-for-voting")
def verify_face_for_voting(
    request: FaceVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify user's face before casting vote - ensures it's the same person who registered"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image data"
        )
    
    # Get the current user's registered face encoding
    face_record = db.query(FaceEncoding).filter(
        FaceEncoding.user_id == current_user.id,
        FaceEncoding.is_verified == "verified"
    ).first()
    
    if not face_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven't registered your face yet. Please register during login."
        )
    
    # Verify the provided face against the stored face
    stored_encoding = deserialize_face_encoding(face_record.face_encoding)
    is_match, distance = verify_face_from_stored_encoding(
        image_data, 
        stored_encoding
    )
    
    if not is_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face verification failed. The face does not match your registered face."
        )
    
    # Update last used time
    face_record.last_used_at = datetime.utcnow()
    db.commit()
    
    return {
        "verified": True,
        "is_match": True,
        "user_id": current_user.id,
        "confidence_distance": float(distance),
        "message": "Face verified successfully for voting"
    }


@router.get("/status")
def check_face_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user has registered face"""
    face_record = db.query(FaceEncoding).filter(
        FaceEncoding.user_id == current_user.id
    ).first()
    
    if not face_record:
        return FaceStatusResponse(
            has_face_registered=False,
            is_verified=False,
            last_used_at=None,
            created_at=None
        )
    
    return FaceStatusResponse(
        has_face_registered=True,
        is_verified=face_record.is_verified == "verified",
        last_used_at=face_record.last_used_at,
        created_at=face_record.created_at
    )


@router.delete("/remove")
def remove_face(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove user's registered face"""
    face_record = db.query(FaceEncoding).filter(
        FaceEncoding.user_id == current_user.id
    ).first()
    
    if not face_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No face registered"
        )
    
    db.delete(face_record)
    db.commit()
    
    return {"message": "Face removed successfully"}
