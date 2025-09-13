# Eye Disease Prediction API

A Flask-based REST API that uses deep learning to predict eye diseases from uploaded images.

## 🎯 Features

- **REST API**: Clean JSON-based API endpoints
- **User Management**: Registration and login functionality
- **Image Upload**: Support for multiple image formats (PNG, JPG, JPEG, GIF)
- **AI-Powered Prediction**: Deep learning model for eye disease classification
- **Health Monitoring**: Built-in health check endpoint

## 🔬 Supported Eye Conditions

- **AMD** (Age-related Macular Degeneration)
- **Cataract** - Cloudy areas in the eye's lens
- **Glaucoma** - Optic nerve damage
- **Myopia** - Nearsightedness
- **Normal** - Healthy eyes
- **Non-eye** - Images that don't contain eyes

## 🛠 Technology Stack

### Backend
- **Flask 3.0.3** - Web framework
- **SQLAlchemy** - Database ORM
- **PyTorch 2.4.1** - Machine learning framework
- **Torchvision** - Image processing
- **PIL (Pillow)** - Image manipulation
- **SQLite** - Database

### Machine Learning
- **Custom CNN Model** - ImprovedTinyVGGModel
- **Image Preprocessing** - Torchvision transforms
- **Multi-class Classification** - 6 categories

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python run.py
```

### 3. Access API
The API will be available at: `http://localhost:5000`

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password"
}
```

#### Login User
```http
POST /api/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

### Image Prediction

#### Upload and Predict
```http
POST /api/upload
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "image.jpg",
  "prediction": {
    "condition": "Normal",
    "description": "This is a healthy eye image",
    "confidence": "High"
  }
}
```

#### Get Prediction for Uploaded File
```http
GET /api/predict/{filename}
```

### Monitoring

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Eye Disease Prediction API is running"
}
```

#### API Documentation
```http
GET /
```

## 📁 Project Structure

```
eye-disease-prediction/
├── app.py                 # Main Flask API application
├── model.py              # Neural network model definition
├── utils.py              # Utility functions for image processing
├── run.py                # Application runner script
├── requirements.txt      # Python dependencies
├── models/              # Trained model files
│   └── MultipleEyeDiseaseDetectModel.pth
├── uploads/             # Uploaded images directory
├── testingImages/       # Sample test images
└── instance/           # Database files
    └── database.db
```

## 🧠 Model Information

The API uses a custom CNN architecture:
- **Model**: ImprovedTinyVGGModel
- **Input Shape**: 3 channels (RGB)
- **Hidden Units**: 48
- **Output Classes**: 6
- **Image Size**: 224x224 pixels

### Model Architecture
- Multiple convolutional blocks with BatchNorm and Dropout
- MaxPooling for dimensionality reduction
- Fully connected classifier layers
- ReLU activation functions

## 🔒 Security Features

- **Input Validation**: File type and size validation
- **Secure Filenames**: Using werkzeug.utils.secure_filename
- **SQL Injection Protection**: SQLAlchemy ORM
- **Error Handling**: Comprehensive error responses

## 🧪 Testing

### Using curl

#### Test Health Check
```bash
curl http://localhost:5000/api/health
```

#### Test Registration
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass"}'
```

#### Test Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass"}'
```

#### Test Image Upload
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@path/to/your/image.jpg"
```

### Using Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Register user
user_data = {
    "email": "test@example.com",
    "username": "testuser", 
    "password": "testpass"
}
response = requests.post('http://localhost:5000/api/register', json=user_data)
print(response.json())

# Upload image
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/upload', files=files)
    print(response.json())
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing Model File**
   ```
   Error: Model file not found
   Solution: Ensure MultipleEyeDiseaseDetectModel.pth is in models/ directory
   ```

2. **Database Errors**
   ```
   Error: Database table doesn't exist
   Solution: Delete instance/database.db and restart application
   ```

3. **Upload Issues**
   ```
   Error: File upload fails
   Solution: Ensure uploads/ directory exists and has write permissions
   ```

4. **Dependencies Issues**
   ```
   Error: Module not found
   Solution: Run pip install -r requirements.txt
   ```

## 📊 Performance Notes

- **Model Loading**: Model is loaded on each prediction (consider caching for production)
- **Image Processing**: Images are resized to 224x224 for model input
- **Database**: SQLite is suitable for development; consider PostgreSQL for production
- **File Storage**: Local file storage; consider cloud storage for production

## 🚀 Deployment Considerations

### For Production:
1. **Security**: Change SECRET_KEY, use environment variables
2. **Database**: Migrate to PostgreSQL or MySQL
3. **File Storage**: Use cloud storage (AWS S3, Google Cloud)
4. **Model Serving**: Consider model caching or separate ML service
5. **Web Server**: Use Gunicorn + Nginx
6. **SSL**: Enable HTTPS
7. **Monitoring**: Add logging and monitoring

### Environment Setup:
```bash
# Production environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- PyTorch team for the deep learning framework
- Flask community for the web framework
- Contributors and testers

---

**Last Updated**: January 2025
**Version**: 2.0.0
**Status**: Production Ready API