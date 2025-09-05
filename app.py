import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from model import ImprovedTinyVGGModel
from utils import *
from datetime import datetime

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png',
                      'jpg', 'jpeg', 'gif', 'zip', 'csv', 'png'}

app = Flask(__name__)
db=SQLAlchemy()
db_connect_time = datetime.now().strftime("%Y%m%d")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='20241111'
db.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),nullable=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(90),nullable=False)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('pass')
        type=request.form.get('reqst')
        print(type)
        if type=="r":
            username=request.form.get('username')
            print(email, password, username)
            register=User(email=email,username=username,password=password)
            db.session.add(register)
            db.session.commit()
            return "1"
        elif type=="l":
            login=User.query.filter_by(email=email,password=password).first()
            if login is not None:
                print("Going dash")
                return redirect(url_for('dashboard'))
            else:
                return "-1"#render_template("index.html")

    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        register=User(email=email,username=username,password=password)
        db.session.add(register)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/dashboard',methods=['GET','POST'])
def dashboad():
    return render_template('dashboard.html')

@app.route('/uploads/<name>')
def download_file(name):
    return render_template("success.html", name=name)


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict_image/<name>")
def predict_image(name):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    MODEL_SAVE_PATH = "models/MultipleEyeDiseaseDetectModel.pth"
    model_info = torch.load(MODEL_SAVE_PATH, map_location=torch.device('cpu'))

    # Instantiate Model
    model = ImprovedTinyVGGModel(
        input_shape=3,
        hidden_units=48,
        output_shape=6).to(device)
    
    data_path = Path("uploads/")

    custom_image_path = data_path / name
    
    # Load and preprocess the image
    custom_image_transformed = load_and_preprocess_image(custom_image_path)

    model.load_state_dict(model_info)
    model.eval()
    
    class_names = np.array(['AMD', 'Cataract', 'Glaucoma', 'Myopia', 'Non-eye', 'Normal'])
    class_names_def = np.array([' Age-related macular degeneration (AMD) is an eye disease that can blur your central vision. It happens when aging causes damage to the macula — the part of the eye that controls sharp, straight-ahead vision. The macula is part of the retina (the light-sensitive tissue at the back of the eye)', 
                                'A cataract is a cloudy area in the eye\'s lens that can cause vision loss. Cataracts are caused by a breakdown of the lens\'s protein, which clumps together and makes the lens cloudy. They can affect one or both eyes, and often develop slowly. In the early stages, cataracts may not cause problems, but over time they can grow larger and affect more of the lens, making it harder to see. ', 
                                'Glaucoma is a group of eye diseases that can damage the optic nerve, which transmits visual information from the eye to the brain. This damage can lead to vision loss and blindness if left untreated. Glaucoma is often called the "silent thief of sight" because vision loss usually occurs slowly over many years and can go unnoticed. ', 
                                'Myopia, also known as nearsightedness or short-sightedness, is a common eye disease that makes it difficult to see far away. It occurs when light from distant objects focuses in front of the retina instead of on it, causing close objects to appear normal while distant objects appear blurry. Other symptoms include: Squinting, Eye strain, Headaches, Difficulty seeing a movie or TV screen, and Difficulty seeing a whiteboard in school or while driving. ', 
                                'No Eye was detected in this image', 'This is a healty Eye image'])
    predicted_index = predict_eye_image(model,
                                                        custom_image_transformed)
    print(class_names[predicted_index])
    return render_template("output.html", ed=class_names[predicted_index],edd=class_names_def[predicted_index])

if __name__ == "__main__":
    app.run(debug=True)

