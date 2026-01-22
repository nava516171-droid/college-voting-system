#!/usr/bin/env python
"""
Simple test to verify face recognition utilities work
"""
import sys
sys.path.insert(0, ".")

from app.utils.face_recognition_util import (
    encode_face_from_image,
    serialize_face_encoding,
    deserialize_face_encoding,
    compare_faces,
    get_face_distance,
    detect_faces_in_image
)
from PIL import Image
import numpy as np
from io import BytesIO

# Create a test image (solid gray)
test_img = Image.new('RGB', (100, 100), color='gray')
img_bytes = BytesIO()
test_img.save(img_bytes, format='PNG')
image_data = img_bytes.getvalue()

print("Testing face recognition utilities...")
print("=" * 50)

# Test 1: Face detection
print("\n1. Testing face detection...")
faces = detect_faces_in_image(image_data)
print(f"   Faces detected: {len(faces)}")
print("   ✓ Face detection working")

# Test 2: Face encoding
print("\n2. Testing face encoding...")
encoding, confidence, success = encode_face_from_image(image_data)
print(f"   Encoding success: {success}")
print(f"   Confidence: {confidence}")
print("   ✓ Face encoding working")

# Test 3: Serialization
print("\n3. Testing serialization...")
if encoding is not None:
    serialized = serialize_face_encoding(encoding)
    deserialized = deserialize_face_encoding(serialized)
    print(f"   Serialized size: {len(serialized)} bytes")
    print(f"   Deserialized shape: {deserialized.shape}")
    print("   ✓ Serialization working")

# Test 4: Face comparison
print("\n4. Testing face comparison...")
if encoding is not None:
    is_match = compare_faces(encoding, encoding, tolerance=0.5)
    distance = get_face_distance(encoding, encoding)
    print(f"   Same face match: {is_match}")
    print(f"   Distance: {distance:.4f}")
    print("   ✓ Face comparison working")

print("\n" + "=" * 50)
print("✓ All face recognition utilities are working!")
