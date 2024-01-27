import numpy as np

def convertToList(face_encode):
    numpy_encode = np.array(face_encode)
    face_encoding_list = numpy_encode.tolist()
    return face_encoding_list
