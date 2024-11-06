import os
import subprocess
from django.shortcuts import render
from django.contrib.auth.models import User
import docker
import requests
from rest_framework import generics, status

from backend.settings import BASE_DIR

from .models import Version
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    
    

@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated, ])
def check_for_updates(request:Request):
    try:
        try:
            fnd_version = Version.objects.get(custom_id=1).frontend_version
            bnd_version = Version.objects.get(custom_id=1).backend_version
            current_frontend_version = fnd_version.replace(".", "")
            current_backend_version = bnd_version.replace(".", "")
            
        except Version.DoesNotExist:
            current_frontend_version = "1.0.0"
            current_backend_version = "1.0.0"
            
        frontend_repository_name = "peetahdarius/jenkins-test-frontend"
        backend_repository_name = "peetahdarius/jenkins-test-backend"
        
        frontend_tags_url = f"https://hub.docker.com/v2/repositories/{frontend_repository_name}/tags"
        backend_tags_url = f"https://hub.docker.com/v2/repositories/{backend_repository_name}/tags"
        
        frontend_response = requests.get(frontend_tags_url)
        frontend_tags = frontend_response.json()["results"]
        
        backend_response = requests.get(backend_tags_url)
        backend_tags = backend_response.json()["results"]
        
        new_version = ""
        
        for tag in frontend_tags:
            string_tag_version = tag["name"]
            int_tag_version = string_tag_version.replace(".", "")
            if int_tag_version > current_frontend_version:
                new_version = string_tag_version
                break
        
        for tag in backend_tags:
            string_tag_version = tag["name"]
            int_tag_version = string_tag_version.replace(".", "")
            if int_tag_version > current_backend_version:
                new_version = string_tag_version
                break
            
        if new_version == "":
            return Response({"detail": "You are up to date"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"new_version": new_version, "current_version": current_frontend_version}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"{e}"})
    
    
@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated, ])
def update_system(request:Request):
    update =  request.data.get("update")
    new_version = request.data.get("new_version")
    current_version = request.data.get("current_version")
    
    if not update:
        return Response({"error": "cannot update application"}, status=status.HTTP_400_BAD_REQUEST)
    
    frontend_image_name = f"peetahdarius/jenkins-test-frontend:{current_version}"
    backend_image_name = f"peetahdarius/jenkins-test-backend:{current_version}"
    
    client = docker.DockerClient(base_url='unix://var/run/docker.sock') 
    
    try:
        # pull the new images
        print("pulling both frontend and backend images...")
        client.images.pull(f"peetahdarius/jenkins-test-frontend:{new_version}")
        print("frontend image pulled successfully...")
        client.images.pull(f"peetahdarius/jenkins-test-backend:{new_version}")
        print("backend image pulled successfully...")
        
        # stoping the containers
        print("stopping the present containers")
        for container in client.containers.list():
            if container.image.tags and (
                frontend_image_name in container.image.tags or
                backend_image_name in container.image.tags
            ):
                print(f"Stopping container: {container.name} using image: {container.image.tags}")
                container.stop()
            
        # prune the stopped containers
        client.containers.prune()
        
        # Start the updated containers with docker-compose
        # Start new containers with the updated images
        client.containers.run(
            f"peetahdarius/jenkins-test-frontend:{new_version}",
            name="frontend",
            detach=True,
            network="jenkins-test-network",
            volumes={"frontend_build": {"bind": "/frontend/build"}},
            environment={"ENV_VARS": "$(cat ./frontend/.env | xargs)"}
        )
        
        client.containers.run(
            f"peetahdarius/jenkins-test-backend:{new_version}",
            name="backend",
            detach=True,
            network="jenkins-test-network",
            volumes={"./backend": {"bind": "/backend"}},
            environment={"ENV_VARS": "$(cat ./backend/.env | xargs)"},
            ports={'8000': '8000'}
        )
        
        client.containers.run(
            "nginx:latest",
            name="nginx",
            detach=True,
            network="jenkins-test-network",
            volumes={"frontend_build": {"bind": "/var/www/frontend"}},
            ports={'80': '80'}
        )

        client.containers.run(
            "postgres:15",
            name="postgres_db",
            detach=True,
            network="jenkins-test-network",
            environment={
                "POSTGRES_DB": os.environ.get("DATABASE_NAME"),
                "POSTGRES_USER": os.environ.get("DATABASE_USER"),
                "POSTGRES_PASSWORD": os.environ.get("DATABASE_PASSWORD")
            },
            volumes={"postgres_data": {"bind": "/var/lib/postgresql/data"}},
            ports={'5432': '5432'}
        )
        
        # Clean up unused Docker resources
        client.images.prune()
        
        # Update version in the database (assuming Version model exists)
        version = Version.objects.get(custom_id=1)
        version.frontend_version = new_version
        version.backend_version = new_version
        version.save()
        
        # Clean up unused images and resources
        client.images.prune()
        
        # updating the database
        version = Version.objects.get(custom_id=1)
        version.frontend_version = new_version
        version.backend_version = new_version
        version.save()
        
    except docker.errors.DockerException as e:
        print("Docker operation failed:", e)
        return Response({"error": "Docker operation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except subprocess.CalledProcessError as e:
        print("docker-compose up failed:", e)
        return Response({"error": "docker-compose up failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response({"message": "System updated successfully"}, status=status.HTTP_201_CREATED)