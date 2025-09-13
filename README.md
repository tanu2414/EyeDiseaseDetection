# Eye Disease Prediction System

A Flask-based web application that uses deep learning to predict eye diseases from uploaded images.

## Features

- User authentication (login/register)
- Image upload functionality
- AI-powered eye disease prediction
- Support for multiple eye conditions:
  - AMD (Age-related Macular Degeneration)
  - Cataract
  - Glaucoma
  - Myopia
  - Normal eyes
  - Non-eye images

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd eye-disease-prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Access the application:**
   Open your web browser and go to `http://localhost:5000`

## Project Structure

```
eye-disease-prediction/
├── app.py                 # Main Flask application
├── model.py              # Neural network model definition
├── utils.py              # Utility functions for image processing
├── run.py                # Application runner script
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── index.html       # Login/Register page
│   ├── dashboard.html   # Main dashboard
│   ├── output.html      # Prediction results
│   └── success.html     # Upload success page
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   ├── images/
│   └── vendor/
├── models/              # Trained model files
├── uploads/             # Uploaded images directory
└── testingImages/       # Sample test images
```

## Usage

1. **Register/Login:** Create an account or login with existing credentials
2. **Upload Image:** Navigate to the dashboard and upload an eye image
3. **Get Prediction:** The system will analyze the image and provide a diagnosis
4. **View Results:** See the predicted condition and detailed description

## Model Information

The application uses a custom CNN model (`ImprovedTinyVGGModel`) trained to classify eye conditions. The model can detect:

- **AMD:** Age-related macular degeneration
- **Cataract:** Cloudy areas in the eye's lens
- **Glaucoma:** Optic nerve damage
- **Myopia:** Nearsightedness
- **Normal:** Healthy eyes
- **Non-eye:** Images that don't contain eyes

## Technical Details

- **Backend:** Flask with SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript with Bootstrap
- **Database:** SQLite
- **ML Framework:** PyTorch
- **Image Processing:** PIL, torchvision

## Troubleshooting

If you encounter issues:

1. **Missing model file:** Ensure `models/MultipleEyeDiseaseDetectModel.pth` exists
2. **Static files not loading:** Check that all CSS/JS files are in the correct directories
3. **Database errors:** Delete `instance/database.db` and restart the application
4. **Upload issues:** Ensure the `uploads/` directory exists and has write permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request