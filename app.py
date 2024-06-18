from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Function to generate frames from the RTSP stream
def generate_frames():
    cap = cv2.VideoCapture('rtsp://admin:admin@123@103.99.13.188:80/cam/realmonitor?channel=1&subtype=0')  # Replace with your RTSP stream URL
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to serve the live video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
