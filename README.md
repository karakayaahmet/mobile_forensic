# mobile_forensic
 
# Mobile Forensic Django Project

Bu proje, mobil cihazlardan alınan verileri incelemek ve yönetmek için Django kullanarak oluşturulmuştur. Mobil cihazlardan elde edilen veriler arasında SMS, çağrı geçmişi, konum bilgileri, dosyalar ve daha fazlası bulunmaktadır.

## Özellikler
- Django ile geliştirilmiş kullanıcı dostu bir arayüz.
- Mobil cihazlardan alınan verileri görüntüleme ve yönetme.
- ADB (Android Debug Bridge) kullanarak cihaz bilgilerini çekme.
- Django ORM kullanarak veritabanı yönetimi.

## Kurulum
1. Projeyi klonlayın: `git clone https://github.com/ilker-yilmaz/mobile_forensic`
2. Virtual environment oluşturun: `python -m venv myenv`
3. Virtual environment'ı aktifleştirin:
    - Windows: `myenv\Scripts\activate`
    - Unix veya MacOS: `source myenv/bin/activate`
4. Gerekli bağımlılıkları yükleyin: `pip install -r requirements.txt`
5. Veritabanını oluşturun: `python manage.py migrate`
6. Django sunucuyu başlatın: `python manage.py runserver`

## Katkıda Bulunma
1. Fork yapın (https://github.com/ilker-yilmaz/mobile_forensic/fork)
2. Yeni bir branch oluşturun (git checkout -b feature/branch-adı)
3. Değişiklikleri commit edin (git commit -m 'Yeni bir özellik eklendi')
4. Branch'ı push edin (git push origin feature/branch-adı)
5. Pull Request oluşturun
