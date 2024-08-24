"""
Provides utility functions for working with Docker containers.
"""

import docker
from loguru import logger
import tarfile
import io


class DockerContainerManager:
    """A class to manage Docker containers.

    This class provides methods to perform various operations on Docker containers,
    such as pulling images, running containers, listing containers, starting,
    stopping, and removing containers, as well as removing images.

    Attributes:
        client (docker.DockerClient): The Docker client instance.
    """

    def __init__(self):
        """Initializes the DockerContainerManager with a Docker client."""
        self.client = docker.from_env()

    def pull_image(self, image_name):
        """Pulls a Docker image if not exists.

        Args:
            image_name (str): The name of the Docker image to pull.
            Example:
                image_name = 'mycompany/myapp:1.0'
        Returns:
            Class image: The Docker image object.
            Example:
                <Image 'mycompany/myapp:1.0'>
        """
        if (image := self.search_image_by_name(image_name)) is not None:
            logger.info(f"Image already exists: {image_name}")
            return image

        try:
            image = self.client.images.pull(image_name)
            logger.info(f"Image pulled: {image_name}")
            return image
        except docker.errors.APIError as e:
            logger.error(f"Error pulling image: {e}")
            return None

    def list_all_images(self):
        """Lists all Docker images.

        Returns:
            List[Class image]: A list of all Docker images.

            Example: [<Image 'ubuntu'>, <Image 'nginx'>, ...]
        """
        return self.client.images.list()

    def get_image_by_name(self, image_name):
        """get for a Docker image by name.

        Args:
            image_name (str): The name of the Docker image to search for.
            Example:
                image_name = 'mycompany/myapp:1.0'
        Returns:
            Class image: The Docker image object.
            Example:
                <Image 'mycompany/myapp:1.0'>
        """
        try:
            image = self.client.images.get(image_name)
        except docker.errors.ImageNotFound:
            logger.warning(f"Image not found: {image_name}")
            return None
        except docker.errors.APIError as e:
            logger.error(f"Error searching image: {e}")
            return None
        return image

    def list_all_containers(self):
        """Lists all Docker containers.

        Returns:
            List[Class container]: A list of all Docker containers.

            Example: [<Container 'mycontainer'>, <Container 'nginx'>, ...]
        """
        return self.client.containers.list(all=True)

    def list_all_running_containers(self):
        """Lists all running Docker containers.

        Returns:
            List[Class container]: A list of all running Docker containers.

            Example: [<Container 'mycontainer'>, <Container 'nginx'>, ...]
        """
        return self.client.containers.list()

    def __get_container_by_image_name(self, image_name):
        """get for a Docker container by image name. Keep each image has only one container.
        Args:
            image_name (str): The name of the Docker image to search for.
            Example:
                image_name = 'mycompany/myapp:1.0'
        Returns:
            Class container: The Docker container object.
            Example:
                <Container 'mycontainer'>
        """
        for container in self.list_all_containers():
            if container.image.tags[0] == image_name:
                return container
        logger.warning(f"Container not found for image: {image_name}")
        return None

    def __get_status_of_container_by_image_name(self, image_name):
        """get status for a Docker container by image name.
        Args:
            image_name (str): The name of the Docker image to search for.
            Example:
                image_name = 'mycompany/myapp:1.0'
        Returns:
            str: The status of the Docker container.
            Example:
                'running' or 'exited' or 'created' or 'not existed'
        """
        if (container := self.__get_container_by_image_name(image_name)) is not None:
            return container.status
        else:
            logger.warning(f"Container not found for image: {image_name}")
            return "not existed"

    def start_container_by_image_name(self, image_name):
        """Starts a Docker container by image name. If the existed container is exited, it will be recreate.
        Args:
            str: image_name
        Returns:
            Class container: The Docker container object.
            Example:
                <Container 'mycontainer'>
        """
        # Check if the container already running or exited
        if (container := self.__get_container_by_image_name(image_name)) is not None:
            if container.status == "exited":
                container.start()
                logger.info(f"Container started: {container.name}")
            elif container.status == "running":
                logger.info(f"Container already running: {container.name}")
            else:
                # Recreate and run the container
                container.remove()
                logger.info(f"Ready to start container with image {image_name}")
                container = self.client.containers.run(image_name, detach=True)
            return container

        # Not existed, create and run the container
        try:
            container = self.client.containers.run(image_name,detach=True)
            logger.info(f"Container started: {container.name}")
            return container
        except docker.errors.APIError as e:
            logger.error(f"Error starting container: {e}")
            return None
    def send_file_to_container_by_container(self,container,local_path,target_path)->None:
        """
        Send SINGLE file to the container using tar stream
        
        Args:
            container (Class container): The Docker container object.
            local_path (str): The local path of the file
            target_path (str): The target path
        Returns:
            None
            """
        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            tar.add(local_path, arcname=target_path)
        tar_stream.seek(0)
        container.put_archive(path='/', data=tar_stream)
        logger.info(f"File {local_path} copied to {target_path} in container {container.name}")
        
        
    def exec_command_in_container(self, container, command)->str:
        """Executes a command in a Docker container.

        Args:
            container (Class container): The Docker container object.
            command (str): The command to execute in the container.
            Example:
                command = 'ls'
        Returns:
            str: The output of the command executed in the container.
        """
        if container.status != "running":
            logger.warning(f"Container is not running: {container.name}")
            # Restart
            container.start()
        try:
            exec_command = container.exec_run(command)
            logger.info(f"Command executed in container: {command}")
            return exec_command.output.decode("utf-8")
        except docker.errors.APIError as e:
            logger.error(f"Error executing command in container: {e}")
            return None
