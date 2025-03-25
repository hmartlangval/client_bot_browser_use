from base_bot.client_base_bot import ClientBaseBot

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

        extend_system_message = (
            'REMEMBER the most important RULE: Strictly do not do anything else apart from the instructions. If any instruction conditions fail, you must immediately restart the task from the beginning.'
        )

        result = await super().call_agent(task, extend_system_message, sensitive_data)
        
        print("execution done: ", result)
        return "Execution is completed!! Nelvin"
    

bot = PropertyBot(options={
    'bot_name': 'Test Bot',
    'bot_id': 't',
}, autojoin_channel='general')


bot.input_thread.join()