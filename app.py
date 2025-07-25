from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
import urllib.request
from io import BytesIO

app = Flask(__name__)

# Define model path and remote URL
MODEL_PATH = "model/cnn_model.keras"
REMOTE_MODEL_URL = "https://huggingface.co/VictoryUdofia/deepfake-model/resolve/main/cnn_model.keras"

# Download the model from Hugging Face if it doesn't exist locally
if not os.path.exists(MODEL_PATH):
    os.makedirs("model", exist_ok=True)
    print("Downloading model from Hugging Face Gubb...")
    urllib.request.urlretrieve(REMOTE_MODEL_URL, MODEL_PATH)
    print("Download complete.")

# Load the model after ensuring it's downloaded
model = load_model(MODEL_PATH)
target_size = (224, 224)


def preprocess_image_from_bytes(file_bytes):
    # Convert file bytes to numpy array
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image format")

    img = cv2.resize(img, target_size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)  # Shape: (1, 224, 224, 3)
    return img


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No image selected"}), 400

    try:
        image_bytes = file.read()
        img = preprocess_image_from_bytes(image_bytes)
        prediction = model.predict(img)[0][0]
        label = "Fake" if prediction >= 0.5 else "Real"

        return jsonify({"label": label, "confidence": round(float(prediction), 2)})

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/ping")
def ping():
    return "pong", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
