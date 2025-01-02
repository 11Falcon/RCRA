from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, flash
import os
import urllib.request
from werkzeug.utils import secure_filename
from ConceptNet import model, conceptNet

# Define upload folder and allowed extensions
UPLOAD_FOLDER = './uploads/images/'  # Ensure consistent path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.secret_key = "falcon"  # Needed for flash messages

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to validate file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@app.route('/home')
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No image selected for uploading!')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        image_url = url_for('uploaded_image', filename = filename)
        objects = model.detect_objects(image_url)

        raw_data = conceptNet.fetch_raw_conceptnet_data(objects[0])
        
        # Extract and print relationships
        relationships = conceptNet.extract_relationships(raw_data)
        output = []
        if relationships:
            print(f"Relationships for '{objects[0]}':")
            for rel in relationships:
                output.append(rel)
        else:
            output.append(f"No relationships found for '{objects[0]}'.")
        return render_template('main.html', image_url=image_url, objects=objects, output=output)
    else:
        flash("Allowed image types are - png, jpg, jpeg, gif")
        return redirect(request.url)

@app.route('/uploaded/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
