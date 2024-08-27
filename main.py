from loguru import logger
import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter
from src.utils.update_tools import update_tools
import re

async def main(requirement: str):
    role = DataInterpreter(tools=["Fbinfer"])   # 集成工具
    await role.run(requirement)

if __name__ == "__main__":
    # Update tools to the libs
    update_tools()
    
    # Import after all tools and denpendencies are updated
    from metagpt.tools.libs import fbinfer
    
    # Load the src code
    with open("./test.c","r") as f:
        code=f.read()
        
    # Escape the special characters
    code=re.sub(r'(\\)', r'\\\\', code)
    code = re.sub(r'(\n)', r'\\n', code)
    code = re.sub(r'(\t)', r'\\t', code)
    code = re.sub(r'(\0)', r'\\0', code)
    
    #logger.info(f"Read code from test.c:\n{code}")
    requirement = "使用fbinfer扫描下面的代码:"+code
    asyncio.run(main(requirement))
