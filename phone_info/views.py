import os
import subprocess

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import PhoneCreateForm, PhoneEditForm
from .utils import get_phone_info
from .models import Phone, Category, Device
import random
from ckeditor.fields import RichTextField

@login_required()
def index(request):
    phones_db = Phone.objects.filter(phone_isHome=True)
    categories = Category.objects.all()

    context = {
        'phones': phones_db,
        'categories': categories
    }

    return render(request, 'phone_info/index.html', context)


@login_required()
def get_phone_by_category(request, slug):
    phones = Phone.objects.filter(categories__slug=slug, phone_isCompleted=True).order_by('phone_date')
    category = Category.objects.all()
    paginator = Paginator(phones, 3)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)
    context = {
        'page_obj': page_obj,
        'categories': category,
        'selected_category': slug
    }

    return render(request, 'phone_info/list.html', context)


@login_required()
def details(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    context = {
        'phone': phone
    }
    return render(request, 'phone_info/details.html', context)


@login_required()
def phone_info_view(request):
    phone_info = get_phone_info()

    context = {
        'phone_info': phone_info,
    }

    return render(request, 'phone_info/phone_info.html', context)


@login_required()
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        phones = Phone.objects.filter(phone_isCompleted=True, phone_name__contains=q).order_by('phone_date')
        category = Category.objects.all()
    else:
        return redirect('/phone')
    context = {
        'phones': phones,
        'categories': category,
    }

    return render(request, 'phone_info/search.html', context)


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def create_phone(request):
    if request.method == 'POST':
        form = PhoneCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/phone')
    else:
        form = PhoneCreateForm()
    return render(request, 'phone_info/create_phone.html', {'form': form})


@login_required()
def phone_list(request):
    phones = Phone.objects.all()
    return render(request, 'phone_info/phone-list.html', {
        'phones': phones
    })


@login_required()
def phone_edit(request, id):
    phone = get_object_or_404(Phone, pk=id)
    form = PhoneEditForm(request.POST or None, request.FILES or None, instance=phone)
    if request.method == 'POST':
        form = PhoneEditForm(request.POST, request.FILES, instance=phone)
        form.save()
        return redirect('phone_list')
    else:
        form = PhoneEditForm(instance=phone)

    return render(request, 'phone_info/edit_phone.html', {
        'form': form
    })


@login_required()
def phone_delete(request, id):
    phone = get_object_or_404(Phone, pk=id)
    if request.method == 'POST':
        phone.delete()
        return redirect('phone_list')


def list_devices(request):
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = result.stdout.splitlines()[1:-1]  # İlk satır başlık, son satır boş
    devices = [line.split('\t')[0] for line in devices if line.strip()]  # Cihaz ID'leri

    # Veritabanında olmayan cihazları ekle
    for device_id in devices:
        Device.objects.get_or_create(device_id=device_id)

    return render(request, 'list_devices.html', {'devices': Device.objects.all()})

def device_detail(request, device_id):
    device = Device.objects.get(device_id=device_id)
    # Cihaz detay komutları burada çalıştırılabilir
    return render(request, 'device_detail.html', {'device': device})