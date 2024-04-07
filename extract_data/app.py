from flask import Flask, render_template, request, redirect, url_for, flash
from data_extration import ExtractPDFData
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = file.filename
            file.save(os.path.join("uploads", filename))
            file_path = os.path.join("uploads", filename)
            
            extracted_data = ExtractPDFData().extract_information(file_path)
            
            mcv_value = extracted_data[0].get("MCV")
            age = extracted_data[0].get("Age")
            gender = extracted_data[0].get("Sex")
            
            anemia_type = ExtractPDFData().identify_anemia_type(mcv_value)
            
            return render_template(
                "home.html", 
                extracted_data=extracted_data, 
                anemia_type=anemia_type, 
                )
        
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)