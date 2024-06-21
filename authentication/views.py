from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

# from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


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
    

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body) # data containes everything sent by the user
        email = data['email']
        # checking for valid email
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        # checking if username is already in use
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry! email in use, choose another'}, status=409)
        return JsonResponse({'email_valid': True})

    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # get user data
        # validate
        # create user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password)<6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path to view
                # - getting the domain we are on
                # - relative url to Verification
                # - encode uid 
                # - token
                email_subject = 'Activate your account'
                # domain=get_current_site(request).domain
                email_body = 'Test body'

                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request,'Account Succefully Created')
                return render(request, 'authentication/register.html')
                

        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')

    