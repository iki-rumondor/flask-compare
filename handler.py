import face_recognition as fr
import cv2
import numpy as np
import json
from utils import convertToList

def compareFace(path1, path2):
    print("Masuk Ke Compare")
    faceOne = fr.load_image_file(path1)
    faceTwo = fr.load_image_file(path2)
    
    rgbFaceOne = cv2.cvtColor(faceOne, cv2.COLOR_BGR2RGB)
    rgbFaceTwo = cv2.cvtColor(faceTwo, cv2.COLOR_BGR2RGB)

    faceOneEnco = fr.face_encodings(rgbFaceOne)[0]
    faceTwoEnco = fr.face_encodings(rgbFaceTwo)[0]

    matchResult = fr.compare_faces([faceOneEnco], faceTwoEnco)
    result, = matchResult
    return {
        'success': True,
        'matching': bool(result)
    }

def checkFace(imagePath):
    image = fr.load_image_file(imagePath)
    rgbFace = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faceLocation = fr.face_locations(rgbFace)
    if not faceLocation:
        return {
            'success': False,
            'message': "Wajah Tidak Ditemukan"
        }
    
    return {
        'success': True,
        'message': "Wajah Ditemukan"
    }

def generateFaceEncodings(imagePath):
    image = fr.load_image_file(imagePath)
    rgbFace = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    faceLocation = fr.face_locations(rgbFace)
    if not faceLocation:
        return {
            'success': False,
            'message': "Wajah Tidak Ditemukan"
        }
    
    encodeFace = fr.face_encodings(rgbFace)[0]
    return {
        'success': True,
        'face': convertToList(encodeFace)
    }

def compareFacesWithImage(json_faces, encode_face):
    face = np.array(encode_face)
    faces_data = json.loads(json_faces)
    for id, face_encoding_list in faces_data.items():
        known_face_encoding = np.array(face_encoding_list)
        results = fr.compare_faces([known_face_encoding], face)

        if results[0]:
            return {
                'success': True,
                'data': {
                    'id': id,
                }
            }

    return {
        'success': False,
        'message': "Face not found"
    }