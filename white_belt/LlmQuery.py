import google.generativeai as genai
import os
from dotenv import load_dotenv

class LlmQuery:
    def __init__(self):
        # genai.configure(api_key=os.environ["API_KEY"])

        ## Comments: TODO by user:
        ## 1) get your own gemini api key from https://ai.google.dev/gemini-api/docs/api-key
        ## 2) create an .env file under white_belt
        ## 3) write GEMINI_KEY=your_api_key in .env file and save it

        # Get the path to the directory this file is in
        BASEDIR = os.path.abspath(os.path.dirname(__file__))

        # Connect the path with your '.env' file name
        load_dotenv(os.path.join(BASEDIR, '.env'))

        gemini_key = os.getenv("GEMINI_KEY")

        genai.configure(api_key=gemini_key)
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_content(self, user_input):
        system_input = f"assume that you are an input interpreter: you will be given a question like how the emission at place X affects the air pollution at place Y. You are expected to output a dictionary as json format. In this json dictionary, there are three keys, source_place, receptor_place, and emission value. The source_place has the information of place X. The pollution_place has the information of place Y. The emission value has the information of emission. For source_place and receptor_place, each include a dictionary that has three key-value combination. The first key is original_value which is the original input of places. The second key is zipcode which is the geocoded zipcode of the places. The third key is coordinates which is the geocoded coordinates of the places. The format of coordinates is a list of latitude and longitude. For emission key, if the question include emission information such at 1 ton/year or 1 ton, please return the value, otherwise, return 1 ton/year (default). {user_input}"
        response = self.model.generate_content(system_input)
        # print(response.text)
        return response.text