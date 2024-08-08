import shutil
from django.shortcuts import render
from mobile_forensic import settings
from .models import Device
import subprocess
import os
from datetime import datetime
from django.http import HttpResponse


def pull_all_device_data(request, device_id):
    device = Device.objects.get(device_id=device_id)
    model = run_adb_command(f'adb -s {device.device_id} shell getprop ro.product.model').strip()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # device-pull dizinine kaydet
    device_pull_directory = f"device-pull/{device.device_id}"
    os.makedirs(device_pull_directory, exist_ok=True)
    result = run_adb_command(f'adb -s {device.device_id} pull /sdcard/ {device_pull_directory}/sdcard-{timestamp}/')

    # MEDIA_ROOT altına kaydet
    media_directory = os.path.join(settings.MEDIA_ROOT, device.device_id)
    os.makedirs(media_directory, exist_ok=True)
    # Dosyaları device-pull'dan MEDIA_ROOT'a kopyala
    shutil.copytree(f"{device_pull_directory}/sdcard-{timestamp}/", f"{media_directory}/sdcard-{timestamp}/")

    return render(request, 'adb_toolkit/device_detail.html', {'device': device, 'output': result})


def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.stderr:
            return 'Error: ' + result.stderr
        return result.stdout
    except Exception as e:
        return str(e)


def list_devices(request):
    result = subprocess.run(["C://ProgramData//platform-tools//adb", 'devices'], capture_output=True, text=True)
    devices = result.stdout.splitlines()[1:-1]  # İlk satır başlık, son satır boş
    device_ids = [line.split('\t')[0] for line in devices if line.strip()]  # Cihaz ID'leri

    # Veritabanında olmayan cihazları ekle ve veritabanındaki cihazları güncelle
    existing_devices = {device.device_id: device for device in Device.objects.all()}
    for device_id in device_ids:
        if device_id in existing_devices:
            del existing_devices[device_id]
        else:
            Device.objects.get_or_create(device_id=device_id)

    # Eğer cihaz artık bağlı değilse, listelemeden çıkar
    Device.objects.filter(device_id__in=existing_devices).delete()

    return render(request, 'adb_toolkit/list_live_devices.html', {'devices': Device.objects.all()})


def device_detail(request, device_id):
    device = Device.objects.get(device_id=device_id)
    if 'get_info' in request.POST:
        output = run_adb_command(f'adb -s {device.device_id} shell getprop')
    elif 'take_screenshot' in request.POST:
        output = run_adb_command(f'adb -s {device.device_id} shell screencap -p /sdcard/screenshot.png')
        if "Error" not in output:
            output += run_adb_command(f'adb -s {device.device_id} pull /sdcard/screenshot.png .')
    elif 'pull_all_data' in request.POST:
        return pull_all_device_data(request, device_id)
    else:
        output = None
    return render(request, 'adb_toolkit/device_detail.html', {'device': device, 'output': output})



def list_device_files(request, device_id):
    base_dir = f'device-pull/{device_id}'  # Directory specific to the device
    file_tree = {
        'photos': [],
        'videos': [],
        'apks': [],
        'others': []
    }

    for root, dirs, files in os.walk(base_dir):
        for name in files:
            file_path = os.path.join(root, name)
            relative_path = os.path.relpath(file_path, base_dir)
            
            # Determine the icon based on the file extension
            if relative_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                icon = "fa-regular fa-image"
                file_tree['photos'].append({'name': relative_path, 'icon': icon})
            elif relative_path.lower().endswith(('.mp4', '.mkv')):
                icon = "fa-solid fa-clapperboard"
                file_tree['videos'].append({'name': relative_path, 'icon': icon})
            elif relative_path.lower().endswith('.apk'):
                icon = "fa-brands fa-android"
                file_tree['apks'].append({'name': relative_path, 'icon': icon})
            else:
                icon = "fas fa-exclamation-triangle"
                file_tree['others'].append({'name': relative_path, 'icon': icon})

    context = {
        'device_id': device_id,
        'file_tree': file_tree
    }

    return render(request, 'adb_toolkit/device_files.html', context)


# def file_details(request, device_id):
#     file_path = request.GET.get('file')
#     full_path = f'device-pull/{device_id}/{file_path}'

#     # ExifTool ile dosya bilgilerini al
#     exif_data = subprocess.run(['exiftool', full_path], capture_output=True, text=True).stdout

#     # Dosya içeriğini gösterme (eğer görüntü veya metin dosyası ise)
#     if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
#         content = (f'<img style="max-width: 25%; height: auto; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" '
#                    f'src="/media/{device_id}/{file_path}" alt="Image preview">')
#     else:
#         content = '<p>Dosya önizlemesi mevcut değil.</p>'

#     return HttpResponse(f'{content}<pre>{exif_data}</pre>')




# from django.conf import settings
# from django.shortcuts import get_object_or_404

# def file_details(request, device_id):
#     file_path = request.GET.get('file')
#     full_path = os.path.join(settings.MEDIA_ROOT, device_id, file_path)
    
#     # ExifTool ile dosya bilgilerini al
#     exif_data = subprocess.run(['exiftool', full_path], capture_output=True, text=True).stdout

#     # Dosya içeriğini gösterme (eğer görüntü veya metin dosyası ise)
#     if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
#         media_url = os.path.join(settings.MEDIA_URL, device_id, file_path)
#         content = (f'<img style="max-width: 25%; height: auto; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" '
#                    f'src="{media_url}" alt="Image preview">')
#     else:
#         content = '<p>Dosya önizlemesi mevcut değil.</p>'

#     return HttpResponse(f'{content}<pre>{exif_data}</pre>')





# def file_details(request, device_id):
#     file_path = request.GET.get('file')
#     full_path = f'device-pull/{device_id}/{file_path}'
    
#     try:
#         result = subprocess.run(['exiftool', full_path], capture_output=True, text=True, check=True)
#         exif_data = result.stdout
#     except subprocess.CalledProcessError as e:
#         exif_data = f"Hata oluştu: {e.stderr}"

#     # Dosya içeriğini gösterme (eğer görüntü veya metin dosyası ise)
#     if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
#         content = (f'<img style="max-width: 25%; height: auto; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" '
#                    f'src="/media/{device_id}/{file_path}" alt="Image preview">')
#     else:
#         content = f"<pre>{exif_data}</pre>"

#     return HttpResponse(content)

from django.conf import settings
from django.http import HttpResponse
import os
import subprocess

def file_details(request, device_id):
    file_path = request.GET.get('file')
    
    # Dosya yolunu parçalarına ayır
    parts = file_path.split('DCIMCamera')
    if len(parts) > 1:
        file_path = os.path.join(parts[0], 'DCIM', 'Camera', '' + parts[1])
    
    full_path = os.path.join(settings.MEDIA_ROOT, device_id, file_path)
    
    # Dosyanın var olup olmadığını kontrol edin
    if not os.path.exists(full_path):
        return HttpResponse(f'Dosya bulunamadı: {full_path}')
    
    # ExifTool ile dosya bilgilerini al
    exif_data = subprocess.run(['exiftool', full_path], capture_output=True, text=True).stdout
    
    # Dosya içeriğini gösterme (eğer görüntü veya metin dosyası ise)
    if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        media_url = os.path.join(settings.MEDIA_URL, device_id, file_path)
        content = (f'<img style="max-width: 25%; height: auto; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" '
                   f'src="{media_url}" alt="Image preview">')
    else:
        content = '<p>Dosya önizlemesi mevcut değil.</p>'
    
    return HttpResponse(f'{content}<pre>{exif_data}</pre>')
