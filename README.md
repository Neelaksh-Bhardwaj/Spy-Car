# Object Detection Using MobileNet SSD and UDP Communication

This system demonstrates real-time object detection using the MobileNet SSD model along with UDP communication for sending messages. The system consists of two main components:

1. **Object Detection**: Using OpenCV and a pre-trained MobileNet SSD model to detect objects in video frames.
2. **UDP Messaging**: Sending messages (e.g., when a "person" is detected) over a UDP socket to another device. A server is set up to listen for these messages.

## Components Overview

### 1. Object Detection
- **Model**: The MobileNet SSD model is used to identify various objects in real-time, including common objects like "person", "car", "dog", etc. The model is pre-trained on a dataset of common objects.
- **Video Streaming**: The video feed can be from an IP camera or any video stream. For performance optimization, every 5th frame is processed.
- **Detection**: Using the `blobFromImage` function in OpenCV's `cv2.dnn` module, the frame is transformed into a format the model can understand. The model then detects objects, returning confidence scores and bounding box coordinates.
- **UDP Communication**: When a "person" is detected, a UDP message `"Person detected!"` is sent to a remote device at IP address `192.168.3.112` on port `5000`.

### 2. UDP Server
- A UDP server listens for incoming messages on port `5000`. The server prints out received messages along with a timestamp and the sender's address. This server runs in a separate thread to allow concurrent execution with object detection.

## Requirements

To run this project, the following libraries need to be installed:

- **Python** 3.x
- **OpenCV**: For video capture and object detection (`pip install opencv-python`)
- **NumPy**: For numerical computation (`pip install numpy`)

## Files

1. **MobileNetSSD_deploy.prototxt.txt**: Contains the architecture of the MobileNet SSD model.
2. **MobileNetSSD_deploy.caffemodel**: The pre-trained weights file for the MobileNet SSD model.
3. **main.py**: The main Python script that handles object detection and UDP communication.

## Running the Project

### 1. Setting up IP Camera:
If you have an IP camera, replace `'http://192.168.3.244:4747/video'` in the code with your camera's video stream URL.

Additionally, change the `target_address` in the `start_detection()` function to the IP address and port of the device you want to receive messages on (e.g., `192.168.3.112` on port `5000`).

### 2. Running the Script:
Once the dependencies are installed and the configurations are set, run the script with Python:

```bash
python main.py
```

### 3. Starting UDP Server:
The server will automatically listen for incoming messages on port `5000`. If a "person" is detected in the video feed, a message will be sent via UDP to the target device.

### 4. Output Display:
The video stream will be displayed in a window (`cv2.imshow("Frame", frame)`). To stop the detection and close the window, press the `q` key.

## Code Explanation

### Object Detection (`start_detection` function)
- **Video Capture**: Captures the video feed from the camera using `cv2.VideoCapture`.
- **Frame Processing**: Processes every 5th frame for object detection.
- **MobileNet SSD**: The model is loaded using `cv2.dnn.readNetFromCaffe`, and predictions are made with the `net.forward()` method.
- **Bounding Boxes**: For each detected "person" (confidence > 0.3), a bounding box is drawn, and the label with the confidence score is displayed.
- **UDP Messaging**: When a "person" is detected, a UDP message is sent to the remote device.

### UDP Server (`start_server` function)
The server listens on port `5000` for UDP messages. When a message is received, the server prints the timestamp, the message, and the sender's address.

### Multithreading
Both the object detection and UDP server run on separate threads to ensure they do not block each other. The main function spawns two threads: `detection_thread` for object detection and `server_thread` for the UDP server, then waits for both to finish using `join()`.

## Example of Output

### 1. Detection and Message:
When a person is detected in the video stream, the following message is sent via UDP to the target device:

```
Person detected!
```

### 2. Server Output:
The server running on the target device receives the message and prints something like:

```
2024-11-10 12:30:45 - Received message: Person detected! from ('192.168.3.100', 5000)
```

## Troubleshooting

- **No UDP Message**: Ensure the target IP address and port are correct. Check for any firewall or network issues that might be blocking UDP packets.
- **Model Errors**: Verify that the `MobileNetSSD_deploy.prototxt.txt` and `MobileNetSSD_deploy.caffemodel` files are in the correct directory and accessible by the script.
- **Camera Feed**: Make sure the camera feed URL is correct and accessible. You can test the camera URL with a browser or other video capture software.

## Conclusion

This project demonstrates how to integrate real-time object detection with UDP-based communication. It can be adapted to various applications such as monitoring systems, security applications, or robotics by adjusting the object detection model and communication setup.
