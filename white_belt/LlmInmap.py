from WhiteBeltService import WhiteBeltService, Coordinate
from LlmQuery import LlmQuery
import json    # or `import simplejson as json` if on Python < 2.6

class LlmInmap:
    def __init__(self):
        # genai.configure(api_key=os.environ["API_KEY"])
        pass

    def dict_from_llm(self, user_input_inmap):
        llm_query = LlmQuery()

        json_string = llm_query.generate_content(user_input=user_input_inmap)
        print("llm output:")
        print(json_string[7:-3])
        # print(Type())
        dict = json.loads(json_string[7:-3])
        return dict

    def inmap_from_dict(self, input_dict):
        white_belt_service = WhiteBeltService()

        stack_height = 0
        pollutant = "pNO3"
        source_lat = input_dict["source_place"]["coordinates"][0]
        if type(source_lat) == type("string"):
            source_lat = float(source_lat)
        source_lon = input_dict["source_place"]["coordinates"][1]
        if type(source_lon) == type("string"):
            source_lon = float(source_lon)
        receptor_lat = input_dict["receptor_place"]["coordinates"][0]
        if type(receptor_lat) == type("string"):
            receptor_lat = float(receptor_lat)
        receptor_lon = input_dict["receptor_place"]["coordinates"][1]
        if type(receptor_lon) == type("string"):
            receptor_lon = float(receptor_lon)
        reduction_value = float(input_dict["emission_value"].split(" ")[0])
        reduction_value_with_unit = input_dict["emission_value"]
        source_name = input_dict["source_place"]["original_value"]
        receptor_name = input_dict["receptor_place"]["original_value"]

        pollution_change = white_belt_service.calculate(stack_height=stack_height, 
    pollutant=pollutant, source_lat=source_lat, 
    source_lon=source_lon, receptor_lat=receptor_lat, receptor_lon=receptor_lon, reduction_value=reduction_value)
        print_text = f"The {reduction_value_with_unit} of {pollutant} air pollution from {source_name} results in a {pollution_change:.2} µg m-3 increase in PM2.5 concentration at {receptor_name}."
        return print_text
        