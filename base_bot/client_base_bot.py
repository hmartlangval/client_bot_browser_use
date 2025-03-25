import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserContextConfig, Controller

from browser_use.browser.browser import Browser, BrowserConfig
from extensions.chromium_extension import ChromiumExtension
from extensions.pdf_save_extension import PDFExtension

from base_bot import BaseBot

class ClientBaseBot(BaseBot):
        
    def __init__(self, options=None, autojoin_channel=None, *args, **kwargs):
        
        super().__init__(options, *args, **kwargs)
        
        self.autojoin_channel = autojoin_channel
        
        self.llm = ChatOpenAI(model='gpt-4o')
        self.controller = Controller()

        downloads_path = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(downloads_path):  
            os.makedirs(downloads_path, exist_ok=True)

        pdf_extension = PDFExtension(default_output_dir=downloads_path)
        pdf_extension.extend(self.controller)
        
        with open('prompts.txt', 'r') as f:
            prompt_data = {}
            current_county = None

            for line in f:
                line = line.strip()
                
                if line.startswith("#"):
                    continue                
                if line.startswith(">>County:"):
                    current_county = line.replace('>>County:', '').strip()
                    prompt_data[current_county] = {}
                elif line.startswith(">>URL:"):
                    url = line.replace('>>URL:', '').strip()
                    prompt_data[current_county]['url'] = url
                elif line.startswith(">>INSTRUCTIONS:"):
                    instructions = []
                    continue
                elif line.startswith(">>County:") or line == "":
                    if current_county and instructions:
                        prompt_data[current_county]['instructions'] = "\n".join(instructions)
                    instructions = []
                else:
                    instructions.append(line.strip())

            if current_county and instructions:
                prompt_data[current_county]['instructions'] = "\n".join(instructions)

            # prompt_json = json.dumps(prompt_data, indent=4)
            # print(prompt_json)
            
            self.prompt_json = prompt_data
            # print(self.prompt_json)
        #     print("Warning: Event system not properly initialized")
        #     self._events = {}
        # else:
        #     print("Event system properly initialized")
        
    # def on_registered(self):
    #     print("ON REGISTERED EVENT")
    #     if(self.autojoin_channel):
    #         self.emit("join_channel", self.autojoin_channel)
    
    def get_instructions(self, sensitive_data):
        county = sensitive_data.get('x_county')
        if county:
            prompt_data = self.prompt_json.get(county, {})
            navigate_url = prompt_data.get('url', '')
            instructions = prompt_data.get('instructions', '')
        else:
            instructions = ''
            
        if not instructions or not navigate_url:
            return None
            
        instructions = f"""
        Navigate to the following URL: {navigate_url}
        {instructions}
        """
        
        return instructions
        
    async def call_agent(self, task, extend_system_message=None, sensitive_data=None):
        
        browser = ChromiumExtension.extend_browser(headless=False)
        
        agent = Agent(
            task=task,
            llm=self.llm,
            browser=browser,
            controller=self.controller,
            extend_system_message=extend_system_message,
            sensitive_data=sensitive_data,
        )
        
        result = await agent.run()
        return result
