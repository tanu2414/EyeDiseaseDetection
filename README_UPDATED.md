# Eye Disease Prediction System - Updated Documentation

A comprehensive Flask-based web application that uses deep learning to predict eye diseases from uploaded images.

## 🎯 Features

- **User Authentication**: Secure login/register system with SQLite database
- **Image Upload**: Support for multiple image formats (PNG, JPG, JPEG, GIF)
- **AI-Powered Prediction**: Deep learning model for eye disease classification
- **Responsive Design**: Modern UI with Bootstrap and custom CSS
- **Real-time Results**: Instant prediction results with detailed descriptions

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

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript/jQuery** - Interactive functionality
- **Bootstrap 5** - Responsive framework
- **Font Awesome** - Icons
- **Custom CSS** - Enhanced styling

### Machine Learning
- **Custom CNN Model** - ImprovedTinyVGGModel
- **Image Preprocessing** - Torchvision transforms
- **Multi-class Classification** - 6 categories

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (for cloning repository)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd eye-disease-prediction
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Application
```bash
# Option 1: Use the startup script
chmod +x start_app.sh
./start_app.sh

# Option 2: Manual start
python run.py
```

### 4. Access Application
Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
eye-disease-prediction/
├── app.py                 # Main Flask application
├── model.py              # Neural network model definition
├── utils.py              # Utility functions for image processing
├── run.py                # Application runner script
├── requirements.txt      # Python dependencies
├── start_app.sh          # Startup script
├── test_application.py   # Application test suite
├── backend_test.py       # Backend API test suite
├── templates/            # HTML templates
│   ├── index.html       # Login/Register page
│   ├── dashboard.html   # Main dashboard
│   ├── output.html      # Prediction results
│   ├── success.html     # Upload success page
│   └── base.html        # Base template
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   ├── images/         # Image assets
│   ├── fonts/          # Font files
│   └── vendor/         # Third-party libraries
├── models/              # Trained model files
│   └── MultipleEyeDiseaseDetectModel.pth
├── uploads/             # Uploaded images directory
├── testingImages/       # Sample test images
└── instance/           # Database files
    └── database.db
```

## 🧪 Testing

### Run Application Tests
```bash
# Start the Flask server first
python run.py

# In another terminal, run tests
python test_application.py
```

### Run Backend API Tests
```bash
# Ensure server is running, then:
python backend_test.py
```

## 💻 Usage Guide

### 1. User Registration
- Navigate to the home page
- Click "Create your Account"
- Fill in email, username, and password
- Click "Register"

### 2. User Login
- Enter your email and password
- Click "Login"
- You'll be redirected to the dashboard

### 3. Image Upload & Prediction
- On the dashboard, click "Choose File"
- Select an eye image (PNG, JPG, JPEG, GIF)
- Click "Submit"
- View your prediction results

## 🔧 Configuration

### Environment Variables
The application uses the following configuration:
- `SECRET_KEY`: '20241111' (change in production)
- `SQLALCHEMY_DATABASE_URI`: SQLite database
- `UPLOAD_FOLDER`: 'uploads'

### Allowed File Extensions
- Images: PNG, JPG, JPEG, GIF
- Documents: TXT, PDF, ZIP, CSV

## 🧠 Model Information

The application uses a custom CNN architecture:
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
- **Session Management**: Flask sessions

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

3. **Static Files Not Loading**
   ```
   Error: CSS/JS files not found
   Solution: Check static/ directory structure and Flask url_for() paths
   ```

4. **Upload Issues**
   ```
   Error: File upload fails
   Solution: Ensure uploads/ directory exists and has write permissions
   ```

5. **Dependencies Issues**
   ```
   Error: Module not found
   Solution: Run pip install -r requirements.txt
   ```

## 📊 Performance Notes

- **Model Loading**: Model is loaded on each prediction (consider caching for production)
- **Image Processing**: Images are resized to 224x224 for model input
- **Database**: SQLite is suitable for development; consider PostgreSQL for production
- **File Storage**: Local file storage; consider cloud storage for production

## 🔄 Development Workflow

### Adding New Features
1. Create feature branch
2. Implement changes
3. Run test suites
4. Update documentation
5. Submit pull request

### Testing Checklist
- [ ] All unit tests pass
- [ ] Frontend loads correctly
- [ ] User registration/login works
- [ ] File upload functions
- [ ] Model predictions work
- [ ] Error handling works
- [ ] Static files load

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

## 📝 API Endpoints

- `GET /` - Home page (login/register)
- `POST /` - Handle login/register requests
- `GET /dashboard` - User dashboard
- `POST /success` - File upload handler
- `GET /predict_image/<filename>` - Model prediction
- `GET /uploads/<filename>` - File download
- `GET /static/<path>` - Static file serving

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PyTorch team for the deep learning framework
- Flask community for the web framework
- Bootstrap team for the responsive framework
- Contributors and testers

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the test suites for debugging

---

**Last Updated**: January 2025
**Version**: 2.0.0
**Status**: Production Ready