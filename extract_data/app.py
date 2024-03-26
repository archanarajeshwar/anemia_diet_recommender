from flask import Flask, render_template, request, redirect, url_for, flash
from mysql import connector
import pdfplumber
import os
import re

app = Flask(__name__)

def search_food_items(anemia_type, iron_min, iron_max, folate_min, folate_max, vitamin_c_min, vitamin_c_max):
    cnx = connector.connect(user='root', password='adelard',
                                host='localhost',
                                database='recommender')
    cursor = cnx.cursor()
    query = """
    SELECT Food Name FROM recommender.labeled_dataset WHERE Anemia_Type = %s
        AND Iron >= %s AND Iron <= %s
        AND Folate >= %s AND Folate <= %s
        AND VitaminC >= %s AND VitaminC <= %s
    LIMIT 6
    """
            # ORDER BY Food_Name DES;
    cursor.execute(query, (anemia_type, iron_min, iron_max, folate_min, folate_max, vitamin_c_min, vitamin_c_max))
    results = cursor.fetchall()
    cnx.close()
    return results



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
    

def get_anemia_description(anemia_type):
    anemia_types = {
        "Normocytic Anemia": "Normocytic anemia is characterized by red blood cells that are normal in size but insufficient in number or function. It can be caused by various factors such as chronic diseases, kidney failure, or bone marrow disorders.",
        "Microcytic Anemia": "Microcytic anemia occurs when red blood cells are smaller than normal. This can be due to iron deficiency, thalassemia, or other conditions affecting hemoglobin synthesis.",
        "Macrocytic Anemia": "Macrocytic anemia is characterized by larger than normal red blood cells. This can be caused by deficiencies in vitamin B12 or folate, as well as certain medications or underlying health conditions."
    }
    
    if anemia_type in anemia_types:
        return anemia_type, anemia_types[anemia_type]
    else:
        return "Anemia type not found", "Description not available"
    

def get_nutrient_ranges(age, gender):
    age = int(age)
    if age < 14:
        age_group = "1-13 years"
    elif age < 19:
        age_group = "14-18 years"
    else:
        age_group = "19+"
        
    gender = gender.lower()

    iron_range = {"female": {"1-13 years": (7, 8), "14-18 years": (15, 18), "19+": (18, 18)},
                  "male": {"1-13 years": (7, 8), "14-18 years": (11, 15), "19+": (8, 8)}}

    folate_range = {"female": {"1-13 years": (150, 300), "14-18 years": (400, 400), "19+": (400, 400)},
                    "male": {"1-13 years": (150, 300), "14-18 years": (400, 400), "19+": (400, 400)}}

    vitamin_c_range = {"female": {"1-13 years": (15, 45), "14-18 years": (65, 75), "19+": (75, 75)},
                       "male": {"1-13 years": (15, 45), "14-18 years": (75, 90), "19+": (90, 90)}}

    # Get the corresponding nutrient ranges based on age and gender
    if age_group in iron_range[gender]:
        iron_min, iron_max = iron_range[gender][age_group]
    else:
        iron_min, iron_max = iron_range[gender]["19+"]
    
    if age_group in folate_range[gender]:
        folate_min, folate_max = folate_range[gender][age_group]
    else:
        folate_min, folate_max = folate_range[gender]["19+"]
    
    if age_group in vitamin_c_range[gender]:
        vitamin_c_min, vitamin_c_max = vitamin_c_range[gender][age_group]
    else:
        vitamin_c_min, vitamin_c_max = vitamin_c_range[gender]["19+"]

    return iron_min, iron_max, folate_min, folate_max, vitamin_c_min, vitamin_c_max

# iron_min, iron_max, folate_min, folate_max, vitamin_c_min, vitamin_c_max = get_nutrient_ranges(age, gender)



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
            file.save(os.path.join("extract_data\\uploads", filename))
            file_path = os.path.join("extract_data\\uploads", filename)
            
            # Extract data from PDF
            extracted_data = extract_information(file_path)
            
            # Extract MCV value from the first entry
            mcv_value = extracted_data[0].get("MCV")
            age = extracted_data[0].get("Age")
            gender = extracted_data[0].get("Sex")
            
            # Identify anemia type
            anemia_type = identify_anemia_type(mcv_value)
            
            name, description = get_anemia_description(anemia_type)

            iron_min, iron_max, folate_min, folate_max, vitamin_c_min, vitamin_c_max = get_nutrient_ranges(age, gender)
            
            food_items = search_food_items(anemia_type, iron_min, iron_max, folate_min, folate_max, vitamin_c_min, vitamin_c_max)
            
            # Render the template with extracted data and anemia type
            return render_template(
                "home.html", 
                extracted_data=extracted_data, 
                anemia_type=anemia_type, 
                name=name, 
                description=description,
                food_items=food_items
                )
        
    return render_template("upload.html")




if __name__ == "__main__":
    app.run(debug=True)