from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import io

app = Flask(__name__)

@app.route('/')
def index():
    # Render a simple upload form in the browser
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # Read the file to an OpenCV image
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # Process the image to detect walls
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

        # Perform edge detection
        edges = cv2.Canny(binary_image, 50, 150, apertureSize=3)

        # Detect lines using Hough Transform and store them in wall_data
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
        wall_data = {'walls': lines.tolist() if lines is not None else []}

        return jsonify(wall_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
