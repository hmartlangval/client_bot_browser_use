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
        
         # After initialization, check if our event system is properly set up
        # if not hasattr(self, '_events') or not isinstance(self._events, dict):
        #     print("Warning: Event system not properly initialized")
        #     self._events = {}
        # else:
        #     print("Event system properly initialized")
        
    # def on_registered(self):
    #     print("ON REGISTERED EVENT")
    #     if(self.autojoin_channel):
    #         self.emit("join_channel", self.autojoin_channel)
        
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
