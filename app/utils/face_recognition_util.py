import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import pickle
import logging
import base64

logger = logging.getLogger(__name__)


def encode_face_from_image(image_data: bytes) -> tuple:
    """
    Encode face from image bytes using OpenCV Haar Cascade.
    Returns: (face_encoding, confidence_score, success)
    """
    try:
        # Load pre-trained face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Convert bytes to image
        image = Image.open(BytesIO(image_data))
        image_array = np.array(image)
        
        # Convert to grayscale if needed
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        # Detect faces with more lenient parameters
        # Lower minNeighbors = more lenient (default is 5, we use 2 for better phone detection)
        # Lower scaleFactor = more thorough search
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=2, minSize=(15, 15))
        
        if len(faces) == 0:
            # Try even more lenient detection if first attempt fails
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))
        
        if len(faces) == 0:
            return None, 0.0, False
        
        # Get the largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        # Extract face region
        face_region = image_array[y:y+h, x:x+w]
        
        # Create a simple encoding by converting face region to a hash
        face_encoding = cv2.resize(face_region, (100, 100))
        face_hash = pickle.dumps(face_encoding)
        
        # Confidence score based on face size (more lenient, minimum 0.4 instead of 0.5)
        confidence_score = min(1.0, max(0.4, (w * h) / (image_array.shape[0] * image_array.shape[1]) * 80))
        
        return face_encoding, confidence_score, True
        
    except Exception as e:
        logger.error(f"Error encoding face: {str(e)}")
        return None, 0.0, False


def serialize_face_encoding(face_encoding: np.ndarray) -> bytes:
    """Serialize numpy array to bytes for storage"""
    return pickle.dumps(face_encoding)


def deserialize_face_encoding(encoded_bytes: bytes) -> np.ndarray:
    """Deserialize bytes back to numpy array"""
    return pickle.loads(encoded_bytes)


def compare_faces(face_encoding_1: np.ndarray, face_encoding_2: np.ndarray, tolerance: float = 0.6) -> bool:
    """
    Compare two face encodings using histogram comparison.
    Returns: True if faces match, False otherwise
    """
    try:
        # Resize both images to same size
        img1 = cv2.resize(face_encoding_1, (100, 100))
        img2 = cv2.resize(face_encoding_2, (100, 100))
        
        # Convert to grayscale if needed
        if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        if len(img2.shape) == 3:
            img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        
        # Compare using histogram
        hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
        
        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()
        
        # Calculate similarity using chi-square distance
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        
        # Lower similarity score is better (0 = identical, 1 = different)
        return similarity < (1.0 - tolerance)
        
    except Exception as e:
        logger.error(f"Error comparing faces: {str(e)}")
        return False


def get_face_distance(face_encoding_1: np.ndarray, face_encoding_2: np.ndarray) -> float:
    """
    Get distance between two face encodings.
    Lower distance = more similar (0.0 = identical, 1.0 = completely different)
    """
    try:
        img1 = cv2.resize(face_encoding_1, (100, 100))
        img2 = cv2.resize(face_encoding_2, (100, 100))
        
        if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        if len(img2.shape) == 3:
            img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        
        # Calculate histogram distance
        hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
        
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()
        
        distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        return float(distance)
        
    except Exception as e:
        logger.error(f"Error calculating face distance: {str(e)}")
        return 1.0


def detect_faces_in_image(image_data: bytes) -> list:
    """
    Detect all faces in an image.
    Returns: list of face locations
    """
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        image = Image.open(BytesIO(image_data))
        image_array = np.array(image)
        
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        # Use same lenient parameters as encode_face_from_image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=2, minSize=(15, 15))
        
        # Try more lenient detection if first attempt fails
        if len(faces) == 0:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))
        
        return list(faces)
        
    except Exception as e:
        logger.error(f"Error detecting faces: {str(e)}")
        return []


def verify_face_from_stored_encoding(image_data: bytes, stored_encoding: np.ndarray) -> tuple:
    """
    Verify if face in image matches stored encoding.
    Returns: (is_match, confidence_distance)
    """
    try:
        face_encoding, confidence, success = encode_face_from_image(image_data)
        
        if not success:
            return False, 1.0
        
        # Compare faces
        is_match = compare_faces(stored_encoding, face_encoding, tolerance=0.5)
        distance = get_face_distance(stored_encoding, face_encoding)
        
        return is_match, distance
        
    except Exception as e:
        logger.error(f"Error verifying face: {str(e)}")
        return False, 1.0
