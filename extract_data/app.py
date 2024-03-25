from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pdfplumber
import re

app = Flask(__name__)
app.secret_key = "secret"  # Secret key for flash messages

def extract_data_from_pdf(pdf_file):
    # Define regular expressions for pattern matching
    age_sex_pattern = r"Age : (\d+) Yrs Sex : (\w+)"
    hemoglobin_pattern = r"H[ae]moglobin (\d+\.\d+)"
    mcv_pattern = r"(MCV|M\.C\.V|Mean\sCorpuscular\sVolume) (\d+\.\d+)"
    mean_corp_hgb_conc_pattern = r"Mean Corpuscular HGB Conc\. (\d+\.\d+)"

    # Initialize dictionary to store extracted data
    extracted_data = {}

    # Open the PDF file
    with pdfplumber.open(pdf_file) as pdf:
        # Extract text from each page
        for page in pdf.pages:
            text = page.extract_text()

            # Extract fields using regular expressions
            age_sex_match = re.search(age_sex_pattern, text)
            hemoglobin_match = re.search(hemoglobin_pattern, text)
            mcv_match = re.search(mcv_pattern, text)
            mean_corp_hgb_conc_match = re.search(mean_corp_hgb_conc_pattern, text)

            # Store extracted fields in the dictionary
            if age_sex_match:
                extracted_data["Age"] = age_sex_match.group(1)
                extracted_data["Sex"] = age_sex_match.group(2)

            if hemoglobin_match:
                extracted_data["Hemoglobin"] = hemoglobin_match.group(1)

            if mcv_match:
                extracted_data["Mean Corpuscular Volume"] = mcv_match.group(2)

            if mean_corp_hgb_conc_match:
                extracted_data["Mean Corpuscular HGB Conc."] = mean_corp_hgb_conc_match.group(1)

    return extracted_data

def identify_anemia_type(mcv_value):
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
            extracted_data = extract_data_from_pdf(file_path)
            
            # Extract MCV value
            mcv_value = float(extracted_data.get("Mean Corpuscular Volume", "0"))
            
            # Identify anemia type
            anemia_type = identify_anemia_type(mcv_value)
            
            # Save extracted data or use for further processing
            # For now, just print the extracted data and anemia type
            print("Extracted Data:")
            print(extracted_data)
            print("Anemia Type:", anemia_type)
            
            # Render the template with extracted data and anemia type
            return render_template("result.html", extracted_data=extracted_data, anemia_type=anemia_type)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
