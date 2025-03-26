import json
import time
from base_bot.client_base_bot import ClientBaseBot
from address_parser import AddressParser

class PropertyBot(ClientBaseBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def generate_response(self, message):
        
        # sensitive_data = {'x_parcel_number': '13-02S-13E-04969-101060', 'x_address': '1720 HWY 129, LIVE OAK, FL 32064'}
        # sensitive_data = {'x_parcel_number': '1-35-36-35-0010-00000-0190', 'x_address': '2320 NE 54TH TRAIL, OKEECHOBEE, FL 34972'}
        sensitive_data = {'x_parcel_number': '', 'x_property_name': 'ASINI PROPERTIES LLC', 'x_address': '13127 Grassy Lane'}

        # union
        sensitive_data = {
                # 'x_tax_account': '21-06-19-39-000-0141-0', 
                'x_tax_account': '',
                'x_county': 'Union', 
                'x_property_address': '12459 SW 51ST TER LAKE BUTLER 32054',
                'x_house_number': '12459',
                'x_street_name': '51ST TER',
                'x_city': 'LAKE BUTLER',
                'x_zip_code': '32054'
            }
        
        # taylor
        # sensitive_data = {'x_tax_account': 'R06810-000', 'x_county': 'Taylor', 'x_property_address': '1575 EZELL BEACH RD'}
        sensitive_data4 = {'x_tax_account': '', 'x_county': 'Taylor', 'x_property_address': '1575 EZELL BEACH RD'}
   
       
        #Baker
        sensitive_data = {'x_tax_account': '322S22004900800010', 'x_county': 'Baker', 'x_property_address': '362 MINNESOTA AVE E MACCLENNY'}
         
        #Volusia
        sensitive_data = {'x_tax_account': '', 'x_county': 'Volusia', 'x_property_address': '340 COLOMBA RD DEBARY 32713'}
        
        
        #Volusia
        sensitive_data = {'x_tax_account': '', 'x_county': 'volus3ia', 'x_property_address': '340 COLOMBA RD DEBARY 32713'}
        
        
        #Palm Beach
        # sensitive_data = {'x_tax_account': '00-42-43-23-14-015-3470', 'x_county': 'palmbeach', 'x_property_address': '347 NORWICH O WEST PALM BEACH,FL 33417-7973'}
        sensitive_data = {'x_tax_account': '74-42-43-01-07-000-0103', 'x_county': 'palmbeach', 'x_property_address': '127 1ST WAY, WEST PALM BEACH, FL'}
        
       
        
         #Brevard
        sensitive_data = {
            'x_county': 'brevard','x_account_number': '010089000', 'x_property_address': 'STONEWOOD TOWNHOMES LLC, 325 E UNIVERSITY BLVD #81'
        }
        
        ### Refined Prompting with System Prompt -- Starting below
         
        #Wakulla
        # sensitive_data = {'x_account_number': '01-4S-02W-000-01807-002', 'x_county': 'wakulla', 'x_property_address': '239 HARVEY MILL RD CRAWFORDVILLE 32327'}
        sensitive_data = {'x_account_number': '', 'x_county': 'wakulla', 'x_property_address': '239 HARVEY MILL RD CRAWFORDVILLE 32327'}
        
        #Palm Beach
        # sensitive_data = {'x_account_number': '00-42-43-23-14-015-3470', 'x_county': 'palmbeach', 'x_property_address': '347 NORWICH O WEST PALM BEACH,FL 33417-7973'}
        sensitive_data = {'x_account_number': '74-42-43-01-07-000-0103', 'x_county': 'palmbeach', 'x_property_address': '127 1ST WAY, WEST PALM BEACH, FL'}
        # sensitive_data = {'x_account_number': '', 'x_county': 'palmbeach', 'x_property_address': '127 1ST WAY, WEST PALM BEACH, FL'}

        #Baker
        # sensitive_data = {'x_account_number': '322S22004900800010', 'x_county': 'baker', 'x_property_address': '362 MINNESOTA AVE E MACCLENNY'}
        sensitive_data = {'x_account_number': '', 'x_county': 'baker', 'x_property_address': '362 MINNESOTA AVE E MACCLENNY'}
        
        # SYsTEM LOGIC ---- DO Not EDIt below tHIS LINE -----------------------------------------
        
        with open('prompts_system.txt', 'r') as file:
            extend_system_message = file.read()
        
        instructions = self.get_instructions(sensitive_data)
        
        if instructions is None:
            print("instructions is None")
            exit()
        
        print("instructions: ", instructions)
        
        address_parser = AddressParser()
        parsed = address_parser.call_llm_for_address(sensitive_data['x_property_address'])
        try:
            clean_parsed = parsed.replace("```json", "").replace("```", "")
            
            parsed_json = json.loads(clean_parsed)
            sensitive_data['x_house_number'] = parsed_json['x_house_number']
            sensitive_data['x_street_name'] = parsed_json['x_street_name']
            sensitive_data['x_city'] = parsed_json['x_city']
            sensitive_data['x_zip_code'] = parsed_json['x_zip_code']
        except Exception as e:
            print("error: ", e)
            print(parsed)
            exit()
        
        print("sensitive_data: ", sensitive_data)
        
        result = await super().call_agent(instructions, extend_system_message, sensitive_data)
        
        return "Execution is completed!! "
    

bot = PropertyBot(options={
    'bot_name': 'Nelvin Dev',
    'bot_id': 'nd',
}, autojoin_channel='general')



import requests

def call_rest_api():
    data = {
        "content": "@nd hello",
        "sender": "Admin"
    }
    try:
        response = requests.post('http://localhost:3000/api/channels/general/sendMessage', json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the response as JSON
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

call_rest_api()

bot.input_thread.join()