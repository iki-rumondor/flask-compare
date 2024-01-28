from flask import Flask, request, jsonify, render_template
from handler import compareFace, generateFaceEncodings, checkFace
from werkzeug.utils import secure_filename
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = "secter"
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSION = set(['jpg', 'png', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def get_file_extension(filename):
    path = Path(filename)
    return path.suffix

@app.get("/")
def home():
    return render_template('form.html')

@app.get("/view_encode")
def view_encode():
    return render_template('encode_face.html')

@app.post("/check_face")
def check_face():
    if 'image' not in request.files:
        resp = jsonify({'message' : 'Image file not found'})
        resp.status_code = 400
        return resp
    
    image = request.files['image']
    
    if not allowed_file(image.filename):
        resp = jsonify({'message' : 'File is not an image'})
        resp.status_code = 400
        return resp
    
    image_filename = "check%s" % get_file_extension(secure_filename(image.filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)

    try:
        result = checkFace(image_path)
        if not result["success"]:
            resp = jsonify(result)
            resp.status_code = 500
            return resp
        resp = jsonify(result)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        os.remove(image_path)

@app.post("/encode_face")
def encode_face():
    if 'image' not in request.files:
        resp = jsonify({'message' : 'Image file not found'})
        resp.status_code = 400
        return resp
    
    image = request.files['image']
    
    if not allowed_file(image.filename):
        resp = jsonify({'message' : 'File is not an image'})
        resp.status_code = 400
        return resp
    
    image_filename = "check%s" % get_file_extension(secure_filename(image.filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)

    try:
        result = generateFaceEncodings(image_path)
        if not result["success"]:
            resp = jsonify(result)
            resp.status_code = 500
            return resp
        resp = jsonify(result)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        os.remove(image_path)
    

@app.post("/compare")
def compare():
    print("Masuk Ke Endpoint")
    if 'image1' not in request.files or 'image2' not in request.files:
        resp = jsonify({'message' : 'Please check your files, must be include image1 and image2'})
        resp.status_code = 400
        return resp

    image1 = request.files['image1']
    image2 = request.files['image2']
    
    print("Masuk Ke Validasi Image")
    if not allowed_file(image1.filename) or not allowed_file(image2.filename):
        resp = jsonify({'message' : 'File is not an image'})
        resp.status_code = 400
        return resp

    print("Masuk Ke Simpan Gambar")
    image1_filename = "one%s" % get_file_extension(secure_filename(image1.filename))
    image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1_filename)
    image1.save(image1_path)

    image2_filename = "two%s" % get_file_extension(secure_filename(image2.filename))
    image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2_filename)
    image2.save(image2_path)
    print("Berhasil Menyimpan Gambar")
    

    try:
        res = checkFace(image1_path)
        if not res["success"]:
            resp = jsonify(res)
            resp.status_code = 500
            return resp
        
        res = checkFace(image2_path)
        if not res['success']:
            resp = jsonify(res)
            resp.status_code = 500
            return resp
        
        result = compareFace(image1_path, image2_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        os.remove(image1_path)
        os.remove(image2_path)


if __name__ == '__main__':
    app.run(port=8082)