"""
Single unit test for Docker API.

To run: python3 -m tests.test_docker (at root path)
"""

from src.utils.docker import DockerContainerManager

if __name__=="__main__":
    client=DockerContainerManager()
    client.list_all_images()
    client.list_all_containers()
    client.pull_image("iridium191/fbinfer:latest")
    client.start_container_by_image_name("iridium191/fbinfer:latest")