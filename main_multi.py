"""
To create a team to process different works cause DI is unable to finish all the works by itself.
"""

import asyncio
import re
import subprocess

import fire

from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message

async def main():
    idea:str="""Your task is to analysis the given code using the Facebook Infer tool then write a report based on the analysis results in the following format:
    # Report Summary: Analysis of the provided C code using Facebook Infer (fbinfer)
    ## Code Analysis Summary:
    - Code Language: C
    - Code File: test.c
    - Analysis Tool: Facebook Infer (fbinfer)
    - Analysis Status: Success/Failure
    - Any issues found: Yes/No
    ## Code Analysis Details:
    - [Line Number] Issue Type: Issue Description
    ## Recommendations:
    - Recommendation 1
    - Recommendation 2
    [End of Report]
    
    The following is the path of the sourcecode to be analysised:
    """
    investment:float=3.0
    n_round:int=1
    """with open("./test.c","r") as f:
        code=f.read()
    code=re.sub(r'(\\)', r'\\\\', code)
    code = re.sub(r'(\n)', r'\\n', code)
    code = re.sub(r'(\t)', r'\\t', code)
    code = re.sub(r'(\0)', r'\\0', code)
    """
    code_path="./test.c"
    idea+=code_path
    logger.info(f"{idea=}")

    role=CodeAnalyzer()
    await role.run(idea)
    

class CodeAnalyzer(Role):
    name: str = "CodeAnalyzer"
    profile: str = "CodeAnalyzer"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SendFiletoFbinfer,WriteReport])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)
    
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]  # find the most k recent messages
        result = await todo.run(msg.content)
        logger.info(f"{result=}")
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return 
    
class SendFiletoFbinfer(Action):
    name:str="SendFiletoFbinfer"
    profile:str="Extract file with the given path and execute Fbinfer analysis and return results."
    async def run(self,text:str)->str:
        path=text.split("\n")[-1].strip()
        logger.info(f"{path=}")
        
        # A simple way to determine the code language
        if path.endswith(".cpp"):
            code_lang="cpp"
        elif path.endswith(".c"):
            code_lang="c"
        else:
            raise ValueError(f"Code file {path} is not supported")

        result=subprocess.run(["python3","./src/tools/fbinfer/fbinfer.py",path,code_lang],capture_output=True,text=True)
        logger.info(f"{result=}")
        analysis_result=result.stdout
        
        logger.info(f"{analysis_result=}")
        return  analysis_result

class WriteReport(Action):
    PROMPT_TEMPLATE: str = """
    Write a report based on the analysis results in the following format:
    # Report Summary: Analysis of the provided C code using Facebook Infer (fbinfer)
    ## Code Analysis Summary:
    - Code Language: C
    - Code File: test.c
    - Analysis Tool: Facebook Infer (fbinfer)
    - Analysis Status: Success/Failure
    - Any issues found: Yes/No
    ## Code Analysis Details:
    - [Line Number] Issue Type: Issue Description
    ## Recommendations:
    - Recommendation 1
    - Recommendation 2
    [End of Report]
    
    Here is the result of the analysis:
    {result}
    Your report:
    """
    # TODO: More context may be provided in the future
    async def run(self, result: str)->str:
        prompt = self.PROMPT_TEMPLATE.format(result=result)
        logger.info(f"{prompt=}")
        rsp = await self._aask(prompt)

        report_text=rsp # To be filtered
        logger.info(f"{report_text=}")
        return report_text

if __name__=="__main__":
    fire.Fire(main)
    # NOTE: prompt输入需要格式化以便SendFiltoFbinfer从msg中解析出路径
    # NOTE：应该给Fbinfer那边的接口一个文件路径