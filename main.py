
import cv2
import numpy as np
import socket
from datetime import datetime
import threading

# Load the pre-trained model and class labels
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

class_labels = [
    "background", "aeroplane", "bicycle", "bird", "boat", 
    "bottle", "bus", "car", "cat", "chair", 
    "cow", "dining table", "dog", "horse", "motorbike", 
    "person", "potted plant", "sheep", "sofa", "train", "tv monitor",
    "computer", "keyboard", "mouse"
]

# Set up socket connection for sending messages
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
target_address = ('192.168.3.112', 5000)  # Replace with the target device's IP

def start_detection():
    # Open video stream
    cap = cv2.VideoCapture('http://192.168.3.244:4747/video')

    # Set a lower resolution for processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame_counter += 1
        if frame_counter % 5 != 0:  # Process every 5th frame
            continue

        # Prepare image for the model
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.3:  # Confidence threshold
                idx = int(detections[0, 0, i, 1])
                label = class_labels[idx]
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw bounding box and label
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                text = f"{label}: {confidence:.2f}"
                cv2.putText(frame, text, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Send message if person is detected
                if label == "person":
                    message = "Person detected!"
                    sock.sendto(message.encode(), target_address)

        cv2.imshow("Frame", frame)

        # Check for user input to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

def start_server():
    # Set up the server to listen for incoming UDP messages
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 5000)  # Listen on all interfaces on port 5000
    server_socket.bind(server_address)

    print("Waiting for messages...")

    while True:
        data, address = server_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
        print(f"{timestamp} - Received message: {data.decode()} from {address}")

# Create and start threads for detection and server
detection_thread = threading.Thread(target=start_detection)
server_thread = threading.Thread(target=start_server)

detection_thread.start()
server_thread.start()

# Join threads to the main thread
detection_thread.join()
server_thread.join()
