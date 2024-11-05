import os
import subprocess
from django.shortcuts import render
from django.contrib.auth.models import User
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
    print(new_version)
    if not update:
        return Response({"error": "cannot update application"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        update_script_url = "update.sh"
        subprocess.run([update_script_url, new_version ], check=True)
        
    except subprocess.CalledProcessError as e:
        print("Script failed with return code:", e.returncode)
        
    return Response(status=status.HTTP_201_CREATED)