import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # To Solve import error. It is ugly and may have unknpown impact.
# You may remove it after testing
import uuid
from metagpt.tools.libs.utils.utils_docker import DockerContainerManager # Deploy阶段需要修改这个,开发测试阶段写utils.utils_docker
from loguru import logger
from metagpt.tools.tool_registry import register_tool
import os  

def save_file(code:str,filename:str):
    """
    Save code string to local temp file for transporting
    Args:
        code (string): code string to be saved
        filename (string): the path of the file
    Return:
        None
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(code)
        
def remove_file(filename):
    """Cleanup local temp file
    """
    if os.path.exists(filename):
    # 删除文件
        os.remove(filename)
        logger.info(f"Local file {filename} deleted")
    else:
        logger.warning(f"Local file {filename} not exist")
  
@register_tool(tags=["detect"],include_functions=["__init__","run"])
class Fbinfer:
    """
    Facebook Infer is a static analysis tool developed by Facebook to identify bugs and vulnerabilities in software code. It's a powerful tool that helps developers write more reliable and secure code.
    """
    def __init__(self):
        self.image_name = "iridium191/fbinfer:latest"
        self.docker_client = DockerContainerManager()
        self.container = self.docker_client.start_container_by_image_name(self.image_name)
        logger.info(
        f"Tool fbinfer initializes container: {self.container.name} status: {self.container.status}"
    )
    def run(self,code_lang,code):
        """
        Run the fbinfer container and get result
            Args:
            str: code_lang: The programming language of the code to be analyzed.
            str: code: The code to be analyzed.
        Returns:
            JSON: the analysis report of the code after procceed by middlwares
        Raise:
            None (To be updated)
        """
        if code_lang == "c" or code_lang == "C":
            # Send the code to the container
            # Generate a random file name for the code
            src_file_name=str(uuid.uuid4())+".c" # Local tempfile path. Use uuid to avoid conflict
            target_file_name = "/code.c" # path inside of container file
            logger.debug(f"Code: {code}")
            
            save_file(code,src_file_name)
            
            self.docker_client.send_file_to_container_by_container(self.container,src_file_name,target_file_name)
            
            # Cleanup 
            remove_file(src_file_name)
            
            # Run the analysis
            output = self.docker_client.exec_command_in_container(
                container=self.container, command=f"infer run -- gcc -c {target_file_name}"
            )
        elif code_lang == "cpp":
            # Send the code to the container
            # Generate a random file name for the code
            src_file_name=str(uuid.uuid4())+".cpp" # Local tempfile path. Use uuid to avoid conflict
            target_file_name = "code.cpp"
            save_file(code,src_file_name)
            
            self.docker_client.send_file_to_container_by_container(self.container,src_file_name,target_file_name)
            
            # Cleanup 
            remove_file(src_file_name)
            
            # Run the analysis
            output = self.docker_client.exec_command_in_container(
                container=self.container, command=f"infer run -- g++ -c {target_file_name}"
            )
        else:
            logger.warning(f"Code language {code_lang} is not implemented in fbinfer")
            raise NotImplementedError(
                f"Code language {code_lang} is not implemented in fbinfer"
            )
        return output

if __name__=="__main__":
    """
    Simply an unitest. Dont start the container from here.
    """
    
    """
    infer=Fbinfer()
    with open ("./test.c","r")as code:
        codestring=code.read()
    print(infer.run("c",code=codestring))
    
    """
    
    # Save test
    with open ("./test.c","r")as code:
        codestring=code.read()
    print(codestring)
    save_file(codestring,"./test-1.c")