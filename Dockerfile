FROM orgoro/dlib-opencv-python:latest
WORKDIR /app
COPY . .
RUN pip install face_recognition
RUN pip install flask

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
