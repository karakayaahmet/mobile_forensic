import subprocess
import json

from django.utils.text import slugify

from .models import Phone
from datetime import datetime


def get_phone_info():
    adb_commands = [
        'adb shell getprop | grep language',
        'adb shell getprop | grep boot_completed',
        'adb shell getprop | grep model',
        'adb shell getprop | grep sdk',
        'adb shell getprop | grep timezone',
        'adb shell getprop | grep serialno',
        'adb shell getprop | grep product.name',
        'adb shell getprop | grep brand',
        'adb shell dumpsys battery | grep level',
        'adb shell getprop | grep -e "model" -e "version.sdk" -e "manufacturer" -e "hardware" -e "platform" -e '
        '"revision" -e "serialno" -e "product.name" -e "brand"'
    ]

    phone_info = {}

    for adb_command in adb_commands:
        result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                # Her bir komutun çıktısını parçala ve phone_info'ya ekle
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    key_value = line.split(':')
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        phone_info[key] = value
            except Exception as e:
                print(f"Hata: {e}")
        else:
            print(f"Hata: ADB komutu başarısız oldu. Çıkış kodu: {result.returncode}")

    # save the information to the database with function if the result is not empty
    if phone_info:
        print(phone_info)
        save_phone_info(phone_info)



    return phone_info


# views.py

# views.py

def save_phone_info(phone_info):
    phone = Phone()
    phone.phone_name = phone_info.get('[ro.product.model]', '')  # 'model' yerine '[ro.product.model]' kullanılıyor
    phone.phone_model = phone_info.get('[ro.product.model]', '')  # 'model' yerine '[ro.product.model]' kullanılıyor
    phone.phone_os = phone_info.get('[ro.product.build.version.sdk]', '')  # 'version.sdk' yerine '[ro.product.build.version.sdk]' kullanılıyor
    phone.phone_cpu = phone_info.get('[ro.hardware]', '')
    phone.phone_ram = "8 GB"
    phone.phone_storage = "128 GB"
    phone.phone_battery = "5000 mAh"
    phone.phone_image = "phone_images/samsung.png"

    # phone_slug'ı oluştur ve benzersiz yap
    phone_slug_candidate = phone_info.get('[ro.product.model]', '')
    base_slug = slugify(phone_slug_candidate)

    # Benzersiz bir slug oluşturana kadar döngü
    suffix = 1
    phone_slug = base_slug  # phone_slug değişkenini tanımlayın ve başlatın
    while Phone.objects.filter(phone_slug=phone_slug).exists():
        phone_slug = f"{base_slug}-{suffix}"
        suffix += 1

    phone.phone_slug = phone_slug

    # if phone slug is exist in the database, then update the phone information
    if Phone.objects.filter(phone_slug=phone_slug).exists():
        phone = Phone.objects.get(phone_slug=phone_slug)

    phone.phone_date = datetime.now()
    phone.phone_isCompleted = True
    phone.phone_isUpdated = True
    phone.phone_version_sdk = phone_info.get('[ro.build.version.sdk]', '')  # 'version.sdk' yerine '[ro.build.version.sdk]' kullanılıyor
    phone.phone_manufacturer = phone_info.get('[ro.product.manufacturer]', '')  # 'manufacturer' yerine '[ro.product.manufacturer]' kullanılıyor
    phone.phone_hardware = phone_info.get('[ro.hardware]', '')
    phone.phone_platform = phone_info.get('[ro.board.platform]', '')
    phone.phone_serial_no = phone_info.get('[ro.boot.serialno]', '')
    phone.phone_product_name = phone_info.get('[ro.product.name]', '')  # 'product.name' yerine '[ro.product.name]' kullanılıyor
    phone.phone_brand = phone_info.get('[ro.product.brand]', '')  # 'brand' yerine '[ro.product.brand]' kullanılıyor
    phone.phone_language = phone_info.get('[persist.sys.language]', '')  # 'language' yerine '[persist.sys.language]' kullanılıyor
    phone.phone_boot_completed = phone_info.get('[sys.boot_completed]', '')  # 'boot_completed' yerine '[sys.boot_completed]' kullanılıyor
    phone.phone_timezone = phone_info.get('[persist.sys.timezone]', '')  # 'timezone' yerine '[persist.sys.timezone]' kullanılıyor
    phone.phone_battery_level = phone_info.get('level', '')
    phone.save()
