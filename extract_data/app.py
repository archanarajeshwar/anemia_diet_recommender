from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pdfplumber
import re

app = Flask(__name__)

def extract_value(text, keyword):
    pattern = re.compile(r'{}[\s:]+(.+?)(?:\n|$)'.format(keyword), re.IGNORECASE)
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None

def extract_information(pdf_file_path):
    extracted_data = []

    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Example: searching for specific keywords or patterns
            hemoglobin = extract_value(text, "HEMOGLOBIN")[:4]
            sex = extract_value(text, "Sex")
            age = extract_value(text, "Age")[:2]
            mcv = extract_value(text, "Mean Corpuscular Volume")[:4]

            # Append extracted data to list
            extracted_data.append({
                "Hemoglobin": hemoglobin,
                "Sex": sex,
                "Age": age,
                "MCV": mcv,
            })

    return extracted_data



def identify_anemia_type(mcv_value):
    if mcv_value is None:
        return "Data not available"
    mcv_value = float(mcv_value)
    if mcv_value < 80:
        return "Microcytic Anemia"
    elif 80 <= mcv_value <= 100:
        return "Normocytic Anemia"
    else:
        return "Macrocytic Anemia"





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
            
            # Extract data from PDF
            extracted_data = extract_information(file_path)
            
            # Extract MCV value from the first entry
            mcv_value = extracted_data[0].get("MCV")
            
            # Identify anemia type
            anemia_type = identify_anemia_type(mcv_value)
            
            # Render the template with extracted data and anemia type
            return render_template("result.html", extracted_data=extracted_data, anemia_type=anemia_type)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)