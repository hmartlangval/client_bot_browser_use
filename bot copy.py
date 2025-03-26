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

        task = """
        1. Navigate to URL: https://www.okeechobeepa.com/gis/
        2. if you see a popup to agree the terms and conditions, click on agree
        3. Type in the parcel number
        4. Click on the search button
        5. From the result, click on the parce id that matches the parcel number
        6. Final screen will have the property details, print the page as PDF
        7. Wait for 3 minutes
        """
        
        task = """
        search by parcel id: 
        1. navigate
        2. type parcel id
        3. click the first item
        
        serach by address:
        
        1. Navigate to URL: https://county-taxes.net/fl-pasco/property-tax
        2. Search for address using the x_address.
        3. From the list of dropdown suggestions, click on the address that is most similar to the x_address. Note that the address options may have (or omit) additional information like unit number, zip code, etc not in x_address, but you must click on the address that is most similar to the x_address. 
        4. If you do not see matching result in the top 5 suggestions, refine the search using short notations. Example Ln instead of Lane, St instead of Street, etc. Repeat this for maximum 3 times with different combinations. On each attempt, make sure to clear the input field and start again.
        5. Only if match is found, Click on the search button. If not match found, stop the task.
        6. From result click on the View button that matches the x_property_name
        7. Results shows the information of Real Estate parcel account details and annly reports in a list
        8. Click on the PDF download link that associated for Annual year 2024
        9. Wait for 3 minutes
        """

        standard_task = """
        1. Navigate to URL based on x_county.
        2. Fill search form using x_tax_account if available, otherwise check for Single Field Form Filling Guidelines. Else, fill using respective inputs like x_house_number and x_street_name. if fields are available.
        3. Click on the search button.
        4. From the result, click on link that associates to x_property_address and x_tax_account.
        5. Click on print bill/receipt button. This will download the PDF file.
        6. Move all downloaded PDF files to the "downloads" folder
        7. End task.
        """
        
        task = f"""
        I have a standard task to do as below:  
        
        Instructions:
        {standard_task}
        
        # Navigate to the following URL based on x_county:
        #     "Taylor": "https://taylor.floridatax.us/AccountSearch?s=pt",
        #     "Pasco": "https://county-taxes.net/fl-pasco/property-tax",
        #     "Union": "https://www.unioncountytc.com/Property/SearchSelect?Accept=true&ClearData=True",
        #     "Wakulla": "https://www.wakullacountytaxcollector.com/Property/SearchSelect?Accept=true&ClearData=True",
        #     "Volusia": "https://county-taxes.net/vctaxcollector/property-tax"
        #     "Baker": "https://www.bakertaxcollector.com/Property/SearchSelect?Accept=true&ClearData=True"
            
            

        Customization for the task Only if applicable:
        For Union County:
        1. Fill search form Tax Year as 2024
        2. If x_tax_account is not available, then fill the house number and street name in the search form
        
        For Wakulla County:
        1. Fill search form Tax Year as 2024
        2. If x_tax_account is not available, then fill the house number and street name in the search form
        
        For Baker County:
        1. Fill search form Tax Year as 2024
        2. If x_tax_account is not available, then fill the house number and street name in the search form
        
        For Volusia County:
        1. Fill x_house_number and x_street_name in the search form. wait for result. Repeat single field form filling guidelines.
        """
        
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
       
        #Wakulla
        sensitive_data = {'x_tax_account': '01-4S-02W-000-01807-002', 'x_county': 'Wakulla', 'x_property_address': '239 HARVEY MILL RD CRAWFORDVILLE 32327'}
       
        #Baker
        sensitive_data = {'x_tax_account': '322S22004900800010', 'x_county': 'Baker', 'x_property_address': '362 MINNESOTA AVE E MACCLENNY'}
         
        #Volusia
        sensitive_data = {'x_tax_account': '', 'x_county': 'Volusia', 'x_property_address': '340 COLOMBA RD DEBARY 32713'}
        
        
        #Volusia
        sensitive_data = {'x_tax_account': '', 'x_county': 'volus3ia', 'x_property_address': '340 COLOMBA RD DEBARY 32713'}
        
        
        
        # SYsTEM LOGIC ---- DO Not EDIt below tHIS LINE -----------------------------------------
        
        extend_system_message = (
            """REMEMBER the most important RULE: 
            - Strictly do not do anything else apart from the instructions. 
            - If any instruction conditions fail, you must immediately restart the task from the beginning.
            - If you have a x_tax_account, then search by tax account number.
            - Search by x_property_address only if x_tax_account is not available.
            - Strictly fill only the data expected by the input fields. Read the placeholder or title text of the input fields to understand what to fill. For example: if address is 12459 SW 51ST TER, then fill only 12459 for house number, 52ST TER Lake for street address, etc.
            
            *Single Field Form Filling Guidelines:*
            - First filling x_house_number and x_street_name and wait until suggestions to load. Do not proceed before suggestions are loaded.
            - If top 5 suggestions don't have matching address, then fill the form with blank/empty value. wait for 1 second. Then retart by adding city in the search. And so on till a match is found in the top 5 suggestions.
            - Some address search may use short notations for street name. Example: instead of 51ST TER, it may use 51ST T.
            - Max retry should be 5 times.
            """
        )
        
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