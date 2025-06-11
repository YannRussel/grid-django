from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse

#import pour la configuration de l'oubli du mot de passe 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


user = get_user_model()

def index(request) : 
    return render(request, 'accounts/index.html')

def login_user(request):
    
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        print(f"username reçu : {phone_number}")
        print(f"password reçu : {password}")

        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:  # Seuls les admin accèdent à l'admin
                return redirect('/admin/')
            else:  # Les autres vont sur l'accueil normal
                return redirect('relotagrid:acceuil')
        else:
            print("Échec d'authentification !")
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'accounts/index.html', {'error_message': error_message})

    return render(request, 'accounts/index.html')



def logout_user(request) : 
    logout(request)
    return redirect('accounts:index')


def motdepasse_oublie(request):
    message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            lien = request.build_absolute_uri(reverse('accounts:reset_password', args=[uid, token]))
            send_mail(
                'Réinitialisation de votre mot de passe',
                f'Cliquez sur le lien suivant pour réinitialiser votre mot de passe : {lien}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            message = "Un lien de réinitialisation a été envoyé à votre adresse email."
        except User.DoesNotExist:
            message = "Aucun compte associé à cette adresse email."
    
    return render(request, 'accounts/motdepasse_oublie.html', {'message': message})


def reset_password(request, uidb64, token):
    message = ""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if new_password and new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                message = "Mot de passe réinitialisé avec succès. Vous pouvez maintenant vous connecter."
                return render(request, 'accounts/reset_password.html', {'success': True, 'message': message})
            else:
                message = "Les mots de passe ne correspondent pas ou sont invalides."
        return render(request, 'accounts/reset_password.html', {'token_valid': True, 'message': message})
    else:
        message = "Lien invalide ou expiré."
        return render(request, 'accounts/reset_password.html', {'token_valid': False, 'message': message})

                