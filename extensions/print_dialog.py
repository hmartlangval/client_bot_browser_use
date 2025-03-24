from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller
import os
from datetime import datetime


class PrintDialog:
    def extend(self, controller: Controller) -> Controller:
        @controller.registry.action('Trigger browser print dialog')
        async def trigger_print_dialog(browser: BrowserContext):
            page = await browser.get_current_page()
            
            await page.evaluate("window.print()")
            
            return ActionResult(
                extracted_content=f"Print dialog opened.", 
                include_in_memory=True
            )