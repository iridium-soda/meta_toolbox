from loguru import logger
from metagpt.tools.libs import fbinfer
import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter
from src.utils.update_tools import update_tools

async def main(requirement: str):
    role = DataInterpreter(tools=["Fbinfer"])   # 集成工具
    await role.run(requirement)

if __name__ == "__main__":
    # Update tools to the libs
    update_tools()

    # Open the src code
    with open("./test.c","r") as f:
        code=f.read()
    logger.info(f"Read code from test.c:\n{code}")
    requirement = "使用fbinfer扫描下面的代码,分析代码存在的漏洞:"+code
    asyncio.run(main(requirement))
