from ultralytics import YOLO
from flask import Flask,jsonify
from flask_socketio import SocketIO
import cv2
import math
import time
import asyncio
import threading
import base64

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Model
model = YOLO("yolov8n.pt")

# Object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# FPS calculation variables
start_time = time.time()
frame_count = 0

def video_stream():
    while True:
        global frame_count,start_time
        success, img = cap.read()
        start_time = time.time()
        results = model(img, stream=True)
        # Coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int values

                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # Class name
                cls = int(box.cls[0])
                class_name = classNames[cls]

                # Object details
                org = (x1, y1 - 10)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.6
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(img, f"{class_name} {confidence:.2f}", org, font, fontScale, color, thickness)

        # Calculate and display FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        cv2.putText(img, f"FPS: {fps:.2f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # # Show webcam feed
        # cv2.imshow('Webcam', img)
        # # Quit if 'q' is pressed
        # if cv2.waitKey(1) == ord('q'):
        #     break

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', img)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        # Send frame over WebSocket
        socketio.emit('video_frame',{'frame':frame_data})

        # Control frame rate
        # await asyncio.sleep(0.04)  # Adjust to match video FPS


#app instance
app=Flask(__name__)
# socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/api/start",methods=['GET'])
def detect_start():
    return jsonify({
        'message': "Start"
    })

@app.route("/api/stop",methods=['GET'])
def detect_stop():
    return jsonify({
        'message': "Stop"
    })

@socketio.on("connect")
def connect(*args, **kwargs):
    # reject all connections to test
    return "Connected"

@socketio.on("disconnect")
def disconnect(*args, **kwargs):
    # reject all connections to test
    return "Disconnected"

if __name__ == "__main__":

    # app.run(debug=True)

    # start_server = websockets.serve(video_stream, "localhost", 1357)
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()

    try:
        # NOTE: Use Thread to solve the issue, there might be a better solution without multiple thread
        threading.Thread(target=video_stream, daemon=True).start()
        socketio.run(app, host='127.0.0.1', port=5000)    
    except KeyboardInterrupt:
        pass

    # Release resources
    cap.release()
    # cv2.destroyAllWindows()







