"""
To define customized actions for the data interperters.
"""
from metagpt.actions import Action

class WriteReport(Action):
    """
    Write the report base on the analysis of tools.
    """
    PROMPT_TEMPLATE:str="""
    Here is the analysis result from the tools: {instruction}
    Write the report base on the analysis result from tools. You must write it in the standard JSON format and without any other content. Your report:
    """
    
    name:str="WriteReport"
    
    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        return rsp # No filter for now
    
    