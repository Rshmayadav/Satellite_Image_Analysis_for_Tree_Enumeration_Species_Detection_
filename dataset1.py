import os

from flask import Flask, redirect, render_template, request, url_for
from roboflow import Roboflow
from ultralytics import YOLO

app = Flask(__name__)

# Initialize Roboflow and YOLO
rf = Roboflow(api_key="9OgOlLVvRBxFKLFa3IfS")
project = rf.workspace("trees-tvzmk").project("new-tree")
version = project.version(1)
dataset = version.download("yolov8")
model = YOLO("yolov8n.pt")  # Replace with your specific YOLOv8 model if different

# Create a directory for uploaded files if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)

        # Run inference on the uploaded image
        results = model(filepath)

        # Save and return result
        results_image_path = os.path.join('uploads', 'result_' + file.filename)
        results.save(results_image_path)
        
        return render_template('result.html', image_path=results_image_path)

if __name__ == '__main__':
    app.run(debug=True)
