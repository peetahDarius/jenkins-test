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
    
    frontend_container_name = f"peetahdarius/jenkins-test-frontend:{current_version}"
    backend_container_name = f"peetahdarius/jenkins-test-backend:{current_version}"
    
    client = docker.from_env()
    
    try:
        # stoping the containers
        try:
            frontend_container = client.containers.get(frontend_container_name)
            frontend_container.stop()
            backend_container = client.containers.get(backend_container_name)
            backend_container.stop()
            
        except docker.errors.NotFound as e:
            print(f"Container not found: {e}")
            return Response({"error": "One or more containers not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # prune the stopped containers
        client.containers.prune()
        
        # pull the new images
        client.images.pull(f"peetahdarius/jenkins-test-frontend:{new_version}")
        client.images.pull(f"peetahdarius/jenkins-test-backend:{new_version}")
        
        # Start the updated containers with docker-compose
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        
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