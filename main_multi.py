"""
To create a team to process different works cause DI is unable to finish all the works by itself.
"""

import asyncio
import typer
from metagpt.logs import logger
from metagpt.team import Team
from src.utils.update_tools import update_tools
from src.roles import FbinferCaller, ReportWriter
import re 

async def main():
    idea:str="""Your task is to analysis the given code using the Facebook Infer tool and write a report based on the analysis results in the following format:
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
    
    The following is the code to be analysised:
    """
    investment:float=3.0
    n_round:int=1
    with open("./test.c","r") as f:
        code=f.read()
    code=re.sub(r'(\\)', r'\\\\', code)
    code = re.sub(r'(\n)', r'\\n', code)
    code = re.sub(r'(\t)', r'\\t', code)
    code = re.sub(r'(\0)', r'\\0', code)
    
    idea+=code
    logger.info(idea)
    team = Team()
    team.hire(
        [
            FbinferCaller(),
            ReportWriter()
        ]
    )
    team.invest(investment=investment)
    team.run_project(idea)
    await team.run(n_round=n_round)

if __name__=="__main__":
    # Update and register tools
    update_tools()
    from metagpt.tools.libs import fbinfer
    
    asyncio.run(main())