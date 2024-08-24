from util import DockerContainerManager
from loguru import logger
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
        
"""
TODO: 迁移到单独的目录中
"""       
class fbinfer:
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
        if code_lang == "c":
            # Send the code to the container
            # Generate a random file name for the code
            src_file_name="temp.c" # Local path
            target_file_name = "/code.c" # path inside of container file
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
            src_file_name="temp.cpp" # Local path
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
    with open("test.c","r") as f:
        code=f.read()
    inf=fbinfer()
    print(inf.run("c",code))