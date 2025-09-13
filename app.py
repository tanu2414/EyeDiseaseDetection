#!/usr/bin/env python3
"""
Eye Disease Prediction API
A Flask-based REST API for eye disease prediction using deep learning
"""

import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import torch
import numpy as np
from pathlib import Path
from model import ImprovedTinyVGGModel
from utils import load_and_preprocess_image, predict_eye_image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '20241111'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy()
db.init_app(app)

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(90), nullable=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/register", methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        if not all([email, username, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/login", methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and predict eye disease from image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Make prediction
            prediction_result = predict_image_api(filename)
            
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'prediction': prediction_result
            }), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def predict_image_api(filename):
    """Predict eye disease from uploaded image"""
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        MODEL_SAVE_PATH = "models/MultipleEyeDiseaseDetectModel.pth"
        
        if not os.path.exists(MODEL_SAVE_PATH):
            return {'error': 'Model file not found'}
        
        model_info = torch.load(MODEL_SAVE_PATH, map_location=torch.device('cpu'))

        # Instantiate Model
        model = ImprovedTinyVGGModel(
            input_shape=3,
            hidden_units=48,
            output_shape=6).to(device)
        
        data_path = Path("uploads/")
        custom_image_path = data_path / filename
        
        if not custom_image_path.exists():
            return {'error': 'Image file not found'}
        
        # Load and preprocess the image
        custom_image_transformed = load_and_preprocess_image(custom_image_path)

        model.load_state_dict(model_info)
        model.eval()
        
        class_names = np.array(['AMD', 'Cataract', 'Glaucoma', 'Myopia', 'Non-eye', 'Normal'])
        class_descriptions = np.array([
            'Age-related macular degeneration (AMD) is an eye disease that can blur your central vision. It happens when aging causes damage to the macula — the part of the eye that controls sharp, straight-ahead vision.',
            'A cataract is a cloudy area in the eye\'s lens that can cause vision loss. Cataracts are caused by a breakdown of the lens\'s protein, which clumps together and makes the lens cloudy.',
            'Glaucoma is a group of eye diseases that can damage the optic nerve, which transmits visual information from the eye to the brain. This damage can lead to vision loss and blindness if left untreated.',
            'Myopia, also known as nearsightedness or short-sightedness, is a common eye disease that makes it difficult to see far away. It occurs when light from distant objects focuses in front of the retina instead of on it.',
            'No eye was detected in this image',
            'This is a healthy eye image'
        ])
        
        predicted_index = predict_eye_image(model, custom_image_transformed)
        
        return {
            'condition': class_names[predicted_index[0]],
            'description': class_descriptions[predicted_index[0]],
            'confidence': 'High'  # You could add actual confidence scores here
        }
        
    except Exception as e:
        return {'error': f'Prediction failed: {str(e)}'}


@app.route('/api/predict/<filename>', methods=['GET'])
def get_prediction(filename):
    """Get prediction for a specific uploaded file"""
    try:
        prediction_result = predict_image_api(filename)
        return jsonify(prediction_result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Eye Disease Prediction API is running'
    }), 200


@app.route('/', methods=['GET'])
def index():
    """API documentation endpoint"""
    return jsonify({
        'name': 'Eye Disease Prediction API',
        'version': '2.0.0',
        'description': 'REST API for predicting eye diseases from uploaded images',
        'endpoints': {
            'POST /api/register': 'Register a new user',
            'POST /api/login': 'Login user',
            'POST /api/upload': 'Upload image and get prediction',
            'GET /api/predict/<filename>': 'Get prediction for uploaded file',
            'GET /api/health': 'Health check'
        },
        'supported_conditions': [
            'AMD (Age-related Macular Degeneration)',
            'Cataract',
            'Glaucoma', 
            'Myopia',
            'Non-eye',
            'Normal'
        ]
    }), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)