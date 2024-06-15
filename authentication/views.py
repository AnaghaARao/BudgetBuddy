from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body) # data containes everything sent by the user
        username = data['username']
        # checking for alnum only username
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alpha-numeric characters'}, status=400)
        # checking if username is already in use
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry! username in use, choose another'}, status=409)
        return JsonResponse({'username_valid': True})

    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    