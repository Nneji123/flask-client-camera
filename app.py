import base64
import os

import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode="eventlet")


@app.route("/favicon.ico")
def favicon():
    """
    The favicon function serves the favicon.ico file from the static directory.
    
    :return: A favicon
    """
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


def base64_to_image(base64_string):
    """
    The base64_to_image function accepts a base64 encoded string and returns an image.
    The function extracts the base64 binary data from the input string, decodes it, converts 
    the bytes to numpy array, and then decodes the numpy array as an image using OpenCV.
    
    :param base64_string: Pass the base64 encoded image string to the function
    :return: An image
    """
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    """
    The test_connect function is used to test the connection between the client and server.
    It sends a message to the client letting it know that it has successfully connected.
    
    :return: A 'connected' string
    """
    print("Connected")
    emit("my response", {"data": "Connected"})


def capture_face():
    """
    The capture_face function is a generator function that captures frames from the camera, encodes them into
    a JPEG format, and returns the encoded frame. The function also yields each encoded frame as it is captured.

    :return: A generator object that yields the frame by frame data from a camera
    """
    global out, capture, rec_frame, frame
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if success:
            # detect faces
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:
                # draw bounding boxes around the faces
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35),
                                  (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    text = "Capture Face!"
                    cv2.putText(frame, text, (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)
            try:
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            except Exception as e:
                pass
        else:
            pass

    camera.release()

@socketio.on("image")
def receive_image(image):
    """
    The receive_image function takes in an image from the webcam, converts it to grayscale, and then emits
    the processed image back to the client.


    :param image: Pass the image data to the receive_image function
    :return: The image that was received from the client
    """
    # Decode the base64-encoded image data
    image = base64_to_image(image)
    frame = image
    # detect faces
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) > 0:
        # draw bounding boxes around the faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top),
                        (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35),
                        (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            text = "Capture Face!"
            cv2.putText(frame, text, (left + 6, bottom - 6),
            font, 1.0, (255, 255, 255), 1)
    gray = frame
    frame_resized = cv2.resize(gray, (640, 360))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    emit("processed_image", processed_img_data)


@app.route("/")
def index():
    """
    The index function returns the index.html template, which is a landing page for users.
    
    :return: The index
    """
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
