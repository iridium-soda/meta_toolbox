"""
To define roles for the data interperters.
"""
from loguru import logger
import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter
from metagpt.actions import Action, UserRequirement
from metagpt.roles import Role
from metagpt.actions.di.write_analysis_code import CheckData, WriteAnalysisCode
from metagpt.schema import Message
from src.actions import WriteReport

class FbinferCaller(DataInterpreter):
    """
    FbinferCaller is a role that calls the Fbinfer tool to analyze the code and generate a report.
    """
    name: str = "FbinferCaller"
    profile: str = "An agent that calls the Fbinfer tool to analyze the code."
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tools=["Fbinfer"]
        self._watch([UserRequirement])
    
class ReportWriter(Role):
    name:str="ReportWriter"
    profile:str="An agent that writes a report based on the analysis results."
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([WriteReport])
        self._watch([WriteAnalysisCode])
        
    
    