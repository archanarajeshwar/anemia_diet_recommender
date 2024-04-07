from flask import Flask, render_template, request, redirect, url_for, flash
from data_extration import ExtractPDFData
from prompt import Prompt
from text_processor import TextProcessor
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
            
<<<<<<< HEAD
            recommendations = Prompt().generate_prompt(extracted_data)
            
            summary, type_of_amemia, diet, daily_activity = TextProcessor().processor(recommendations)
            
            return render_template(
                "home.html", 
                summary = summary, 
                type_of_amemia = type_of_amemia, 
                diet = diet, 
                daily_activity = daily_activity, 
=======
            # Extract MCV value from the first entry
           
            # Render the template with extracted data and anemia type
            return render_template(
                "home.html", 
                extracted_data=extracted_data, 
            
>>>>>>> 735f9a6e027edeacba0169aeaa8d9443bb6e3cba
                )
        
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)