# 🎓 KTÜ LMS (E-Öğrenme Platformu)

Bu proje, eğitmenlerin kurs oluşturup yayınlayabildiği, öğrencilerin ise bu kurslara kayıt olup eğitim alabildiği uçtan uca bir E-Öğrenme (LMS - Learning Management System) platformudur.

Proje, standart Django MVC yapısının ötesine geçerek **Katmanlı Mimari (Layered Architecture)** ve **Dikey Dilimleme (Vertical Slicing)** prensipleriyle geliştirilmiş olup, yüksek performans ve sürdürülebilirlik hedeflenmiştir.

## 🚀 Kullanılan Teknolojiler

* **Backend:** Python, Django 5.0
* **Frontend:** HTML5, CSS3, Bootstrap 5.3, FontAwesome 6.4
* **Veritabanı:** AWS RDS (Microsoft SQL Server)
* **Veritabanı Sürücüsü:** `mssql-django`, `pyodbc`

## 🏗️ Mimari Yapı (Layered Architecture)

Proje, "Fat Controller" (Şişman View) anti-pattern'inden kaçınmak için sorumlulukların ayrıldığı profesyonel bir klasör yapısına sahiptir:

* `models/`: Veritabanı şemalarının ve kısıtlamalarının bulunduğu veri katmanı.
* `selectors/`: `select_related` ve `prefetch_related` kullanılarak **N+1 sorgu problemlerinin çözüldüğü**, veritabanından veri çekme işlemlerinin yapıldığı katman.
* `services/`: (Hazırlık aşamasında) İş mantığının (kayıt olma, ilerleme kaydetme) yürütüleceği katman.
* `forms/`: Veri doğrulama ve kullanıcı arayüzü form bileşenlerinin tanımlandığı katman.
* `views/`: Gelen istekleri (Request) alıp ilgili selector veya formlara yönlendiren ve şablonları (Template) döndüren "Trafik Polisi" katmanı.

## ✨ Şu Ana Kadar Tamamlanan Özellikler

### 1. Kullanıcı ve Yetki Yönetimi
* `CustomUser` modeli ile Özelleştirilmiş Kullanıcı Rolleri (Öğrenci, Eğitmen, Admin).
* Güvenli Kayıt Ol (Register), Giriş Yap (Login) ve Çıkış Yap (Logout) işlemleri.
* Kullanıcı Profil Sayfası ve profil fotoğrafı yükleme/güncelleme (Bootstrap Modal ile).

### 2. Kurs ve İçerik Yönetimi
* Ana sayfada en yeni ve aktif kursların dinamik listelenmesi.
* Tüm Kurslar sayfasında **Arama (Search)** altyapısı (Kurs başlığı ve açıklamasına göre).
* Gelişmiş Slug yapısı ve UUID destekli benzersiz link üretimi.

### 3. Eğitmen Paneli (Dashboard)
* Sadece `instructor` (Eğitmen) ve `admin` rolüne sahip kullanıcıların erişebildiği özel panel.
* Eğitmenlerin kendi oluşturdukları kursları listelemesi ve durumlarını (Yayında/Taslak) görmesi.
* Resim yükleme destekli, detaylı **Yeni Kurs Ekleme** formu.

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

**1. Depoyu Klonlayın ve Klasöre Girin**
```bash
git clone <repository_url>
cd e-ogrenme_kurs

2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin
python -m venv venv
# Windows için:
venv\Scripts\activate
# Mac/Linux için:
source venv/bin/activate

3. Gerekli Paketleri Yükleyin
pip install -r requirements.txt

4. Çevresel Değişkenleri (.env) Ayarlayın
Proje ana dizininde bir .env dosyası oluşturun ve aşağıdaki bilgileri kendi AWS RDS bilgilerinize göre doldurun:
SECRET_KEY=senin_django_gizli_anahtarin
DEBUG=True
DB_HOST=senin_aws_rds_endpoint_adresin
DB_NAME=lms_db
DB_USER=veritabani_kullanici_adin
DB_PASSWORD=veritabani_sifren

5. Veritabanını Hazırlayın ve Migrasyonları Uygulayın
Eğer veritabanı henüz oluşturulmadıysa:
python db_olustur.py

Ardından tabloları oluşturun:
python manage.py makemigrations
python manage.py migrate

6. Projeyi Çalıştırın
python manage.py runserver

Tarayıcınızdan http://127.0.0.1:8000/ adresine giderek projeyi görüntüleyebilirsiniz.


Geliştirici Ekip: Hasan Yücel, Hüseyin Şahin, Muhammet Zahit Aydın
