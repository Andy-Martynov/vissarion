from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.db.models import Count
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from django.contrib.auth.models import User
from account.models import Profile

import random

# _________________________________________________ MAIL _______________________

def mail_to(request, user_id=None, subj='Vissarion mail', html='', text=''):
    if user_id:
        user = User.objects.filter(id=user_id).first()
        if user:
            sent = send_mail(
            subj,
            text,
            'andymartynovmail@gmail.com',
            [user.email],
            fail_silently=False,
            html_message = html,
            )
            return 200, sent
        return 404, f'user {user_id} not found'
    return 400, 'bad request, no user ID'

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "registration/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "registration/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        user.is_active = False
        user.save()

        Profile.objects.create(user=user)
        token = random.randint(0, 1000000)*1000+user.id
        user.profile.token = token
        user.profile.save()

        url = 'http://vissarion.pythonanywhere.com/account/confirm/'+str(token)

        html = '''\
<div>
<p>Подтверждение адреса email</p>
<br>
<p><a href="''' + url + '''"><button style="color: #ffffff; background-color: #000066; align: center;">Подтверждение регистрации</button></a></p>
<br>
<p>Спасибо!</p>
</div>'''

        sent = send_mail(
        f'Регистрация {username} {email}',
        '',
        'andymartynovmail@gmail.com',
        [email],
        fail_silently=False,
        html_message = html,
        )

        url = request.session['who_registred']
        request.session['who_registred'] = ''

        logout(request)
        if sent == 0 :
            messages.info(request, f'failed send confirmation email to {email}', extra_tags='alert-danger')
        else :
            messages.info(request, f'Confirmation email has been sent to {email}', extra_tags='alert-success')

        return HttpResponseRedirect(url)
    else:
        request.session['who_registred'] = request.META.get('HTTP_REFERER')
        return render(request, "registration/register.html")

def confirm_email(request, token) :
    id = token % 1000
    user = User.objects.filter(id=id).first()
    if user :
        if user.profile.token == token :
            user.profile.token = 0
            user.profile.save()
            user.is_active = True
            user.save()
            send_mail(
            f'{user.username} {user.email} registred',
            '',
            'andymartynovmail@gmail.com',
            ['lee624768@gmail.com'],
            fail_silently=False,
            )
            return HttpResponse('Email confirmed, thanks!')
        return HttpResponse('400 invalid token')
    return HttpResponse(f'401, user id {id} not found {user}')

