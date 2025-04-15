# FastAPI Backend - Docker Setup

This guide explains how to pull and run the FastAPI backend Docker image from Docker Hub.

## Prerequisites

- Ensure you have Docker installed on your system. If not, download and install it from [Docker's official website](https://www.docker.com/).

## Steps to Pull and Run the Docker Image

1. **Pull the Docker Image**:
   Open a terminal and run the following command to pull the image from Docker Hub:
   ```bash
   docker pull gaberhassan/fastapi-backend:latest
   ```

2. **Run the Docker Container**:
   After pulling the image, run the container using the following command:
   ```bash
   docker run -d -p 8000:8000 --name fastapi-backend gaberhassan/fastapi-backend:latest
   ```

   - `-d`: Runs the container in detached mode.
   - `-p 8000:8000`: Maps port 8000 of the container to port 8000 on your host machine.
   - `--name fastapi-backend`: Assigns a name to the container.

3. **Access the Application**:
   Once the container is running, you can access the FastAPI backend at:
   ```
   http://localhost:8000
   ```

4. **Stop the Container**:
   To stop the running container, use:
   ```bash
   docker stop fastapi-backend
   ```

5. **Remove the Container**:
   If you want to remove the container, run:
   ```bash
   docker rm fastapi-backend
   ```

6. **Remove the Image**:
   To delete the pulled image from your system, use:
   ```bash
   docker rmi gaberhassan/fastapi-backend:latest
   ```

## Additional Notes

- Ensure port 8000 is not being used by another application on your host machine.
- If you encounter any issues, refer to the Docker logs for debugging:
  ```bash
  docker logs fastapi-backend
  ```
