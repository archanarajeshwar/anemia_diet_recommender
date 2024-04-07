import logging
import re
import pdfplumber
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

@dataclass
class ExtractPDFData:
    def extract_value(self, text, keyword):
        pattern = re.compile(r'{}[\s:]+(.+?)(?:\n|$)'.format(keyword), re.IGNORECASE)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return None


    def extract_information(self, pdf_file_path):
        extracted_data = []

        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                hemoglobin = ExtractPDFData().extract_value(text, "HEMOGLOBIN")[:4]
                sex = ExtractPDFData().extract_value(text, "Sex")
                age = ExtractPDFData().extract_value(text, "Age")[:2]
                mcv = ExtractPDFData().extract_value(text, "Mean Corpuscular Volume")[:4]
                
                extracted_data.append({
                    "Hemoglobin": hemoglobin,
                    "Sex": sex,
                    "Age": age,
                    "MCV": mcv,
                })
        return extracted_data


    def identify_anemia_type(self, mcv_value):
        if mcv_value is None:
            return "Data not available"
        mcv_value = float(mcv_value)
        if mcv_value < 80:
            return "Microcytic Anemia"
        elif 80 <= mcv_value <= 100:
            return "Normocytic Anemia"
        else:
            return "Macrocytic Anemia"