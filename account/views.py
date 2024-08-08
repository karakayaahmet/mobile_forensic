from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import LoginUserForm, NewUserForm, UserChangePasswordForm


# Create your views here.
def user_login(request):
    error = None
    if request.user.is_authenticated and 'next' in request.GET:
        return render(request, 'account/login.html', {'error': 'Yetkiniz Yok. Lütfen Giriş Yapınız'})
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Giriş Başarılı')
                nextUrl = request.GET.get('next', 'None')
                if nextUrl == 'None':
                    return redirect('index')
                else:
                    return redirect(nextUrl)
            else:
                return render(request, 'account/login.html', {'form': form})
        else:
            return render(request, 'account/login.html', {'form': form})
    else:
        form = LoginUserForm()
        return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Kayıt Başarılı')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'account/register.html', {'form': form})
    else:
        form = NewUserForm()
        return render(request, 'account/register.html', {'form': form})


def user_logout(request):
    messages.add_message(request, messages.SUCCESS, 'Çıkış Başarılı')
    logout(request)
    return redirect('index')


def change_password(request):
    if request.method == 'POST':
        form = UserChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Şifreniz Değiştirildi')
            return redirect('change_password')
        else:
            return render(request, 'account/change-password.html', {'form': form})

    form = UserChangePasswordForm(request.user)
    return render(request, 'account/change-password.html', {'form': form})