from loguru import logger
import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter
from src.utils.update_tools import update_tools

if __name__=="__main__":
    update_tools()
    