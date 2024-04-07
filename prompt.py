import openai
from extract_data.config import api_key
from dataclasses import dataclass

client = openai.OpenAI(api_key=api_key)

@dataclass
class Prompt:
    def __init__(self, extracted_data):
        self.query = f'''{extracted_data}
                    1. GIVE ME SUMMARY OF THE REPORT WITH PERCENTAGE. 
                    2. WHAT TYPE OF ANEMIA DOES THIS PERSON HAS IN DETAIL. 
                    3. GIVE DIETARY RECOMMENDATIONS(3 MEAL PLAN INDIAN FOOD CUISINE WITH PROPER INDIAN NAMES).
                    4. GIVE DAILY ACTIVITY RECOMMENDATION.
                    '''

    def generate_prompt(self):
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": self.query}
        ]
        )
        return completion['content']


if __name__=='__main__':
    completion = Prompt().generate_prompt()
    print(completion.choices[0].message)