import os
import sys
import asyncio

from extensions.chromium_extension import ChromiumExtension
from property_automation.client_bot_browser_use.extensions.print_dialog import CustomPrint
from extensions.pdf_save_extension import PDFExtension

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserContextConfig, Controller
from dotenv import load_dotenv

from browser_use.browser.browser import Browser, BrowserConfig

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set')

"""
Perform file prep process
"""

# Create downloads folder in current directory.
downloads_path = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(downloads_path):  
    os.makedirs(downloads_path, exist_ok=True)

browser = ChromiumExtension.extend_browser(
    download_dir=downloads_path,
    pdf_save_directory=downloads_path,
    headless=False
)

controller = Controller()
# pdf_extension = PDFExtension(default_output_dir=downloads_path)
# pdf_extension.extend(controller)
    
printer = CustomPrint()
printer.extend(controller)
llm = ChatOpenAI(model='gpt-4o')

sensitive_data = {'x_parcel_number': '13-02S-13E-04969-101060', 'x_address': '1720 HWY 129, LIVE OAK, FL 32064'}

task = """
1. Navigate to URL: https://google.co.in
2. Trigger the browser print dialog using Custom Print
   - The system will attempt to select "Microsoft Print to PDF" from the printer options
   - The file will be automatically saved as Account_<x_parcel_number>_<timestamp>.pdf
"""

extend_system_message = (
	'REMEMBER the most important RULE: Strictly do not do anything else apart from the instructions. If any instruction conditions fail, you must immediately restart the task from the beginning.'
)

agent = Agent(
	task=task,
	llm=llm,
    browser=browser,
    controller=controller,
	extend_system_message=extend_system_message,
	sensitive_data=sensitive_data,
)


async def main():
	result = await agent.run();

	print('automation process completed');
 
 

    


if __name__ == "__main__":
	asyncio.run(main())
