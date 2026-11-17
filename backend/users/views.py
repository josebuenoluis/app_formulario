from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# Create your views here.

class UsersView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        pass