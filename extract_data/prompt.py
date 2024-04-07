import openai
from config import api_key

client = openai.OpenAI(api_key=api_key)

class Prompt:
    def generate_prompt(self, extracted_data):
        query = f'''{extracted_data}
                    1. GIVE ME SUMMARY OF THIS ABOVE REPORT. 
                    2. WHAT TYPE OF ANEMIA DOES THIS PERSON HAS AND THE MORPHOLOGY OF WBC IN DETAIL. 
                    3. GIVE DIETARY RECOMMENDATIONS WITH IT'S NUTRITIONAL VALUE (3 MEAL PLAN INDIAN FOOD CUISINE WITH PROPER INDIAN NAMES).
                    4. GIVE DAILY ACTIVITY RECOMMENDATION.
                    '''
                    
                    # I WANT THE INFORMATION IN THE ABOVE FORMAT (i.e 4 POINTS WITH SAME HEADING NAMES)
                    
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ]
        )
        return completion.choices[0].message.content


if __name__=='__main__':
    extracted_data = '''
    Lab No : 86200
    Name : Miss Archana Rajeshwar Age : 20 Yrs Sex : Female
    ( Labelled Sample Received )
    Ref By : HEALTH TREE The Family Clinic
    Dr. Ameya Phansalkar
    COMPLETE BLOOD COUNT
    Test Result Normal Range Units
    HEMOGLOBIN 12.3 12.00 - 15.60 gm/dl
    RED BLOOD CELL 3.90 3.8 - 5.8 mill/cmm
    TOTAL WBC COUNT 10,300 4000 - 11000 /cmm
    Haematocrit 33.5 Low 35 - 47 %
    Mean Corpuscular Volume 85.9 76 - 96 fl
    Mean Corpuscular hemoglobin 31.5 27 - 32 pg
    Mean Corpuscular HGB Conc. 36.7 High 30 -36 gm/dl
    RDW - CV 15.0 11.5 - 16.5
    DIFFERENTIAL COUNT
    Neutrophils 54 40 - 75 %
    Lymphocytes 41 20 - 45 %
    Eosinophils 04 1 - 6 %
    Monocytes 01 2 - 10 %
    Basophils 00 0 - 1 %
    3
    PLATELET COUNT 395 150 - 450 x10 /cmm
    RBC Morphology Normochromic Normocytic
    WBC Morphology Normal
    Blood cell count done on MEDONIC Cell Counter
    '''
    completion = Prompt().generate_prompt(extracted_data)
    print(completion)