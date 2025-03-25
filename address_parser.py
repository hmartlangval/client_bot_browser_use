import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class AddressParser:
    def __init__(self):
        pass
    
    def parse_address(self, address):
        pass

    def call_llm_for_address(self, address):
        
        llm = ChatOpenAI(model='gpt-4o')
        
        prompt = f"Extract the following address into a structured JSON format: {address}\n\n" \
                    f"Output format:\n" \
                    f"{{\n" \
                    f"  'x_house_number': '',\n" \
                    f"  'x_street_name': '',\n" \
                    f"  'x_direction': '',\n" \
                    f"  'x_city': '',\n" \
                    f"  'x_state': '',\n" \
                    f"  'x_zip_code': ''\n" \
                    f"}}\n\n" \
                    f"If you can't find matching value, return empty string \"\"."

        response = llm.invoke(prompt)

        try:
            result = response.content
            return result if result else ""
        except (KeyError, IndexError):
            return ""

    # Example usage
    # address = "12459 SW 51ST TER LAKE BUTLER 32054"
    # parsed_address = call_llm_for_address(address)
    # print(parsed_address)
    # pass