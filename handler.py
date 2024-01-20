import face_recognition as fr
import cv2

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
    
    return result
