from django.shortcuts import render
from django.contrib.auth.models import User
import requests
from rest_framework import generics, status

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
@permission_classes([AllowAny, ])
def check_for_updates(request:Request):
    try:
        frontend_repository_name = "peetahdarius/jenkins-test-frontend"
        backend_repository_name = "peetahdarius/jenkins-test-backend"
        
        frontend_tags_url = f"https://hub.docker.com/v2/repositories/{frontend_repository_name}/tags"
        backend_tags_url = f"https://hub.docker.com/v2/repositories/{backend_repository_name}/tags"
        
        frontend_response = requests.get(frontend_tags_url)
        frontend_tags = frontend_response.json()["results"]
        
        backend_response = requests.get(backend_tags_url)
        backend_tags = backend_response.json()["results"]
        
        curent_frontend_version = Version.objects.get(custom_id=1).frontend_version.replace(".", "")
        curent_backend_version = Version.objects.get(custom_id=1).backend_version.replace(".", "")
        
        new_version = None
        
        for tag in frontend_tags:
            string_tag_version = tag["name"]
            int_tag_version = string_tag_version.replace(".", "")
            if int_tag_version > curent_frontend_version:
                new_version = string_tag_version
        
        for tag in backend_tags:
            string_tag_version = tag["name"]
            int_tag_version = string_tag_version.replace(".", "")
            if int_tag_version > curent_backend_version:
                new_version = string_tag_version
        
        if new_version is None:
            return Response({"detail": "You are up to date"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": f"You are using version {curent_frontend_version}.A new update v.{new_version} is found"})
    except Exception as e:
        return Response({"error": f"{e}"})