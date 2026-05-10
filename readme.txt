🎉 Uygulama artık `http://127.0.0.1:8000/` adresinde çalışmaktadır. Yönetim paneli için `http://127.0.0.1:800GitHub depona (repository) doğrudan yükleyebileceğin, projeyi inceleyen hocalara veya diğer geliştiricilere "Bu ekip bu işi gerçekten biliyor" dedirtecek, **Markdown (`.md`)** formatında tam kapsamlı ve profesyonel bir `README.md` dosyası hazırladım. 

Aşağıdaki metni kopyalayıp GitHub'daki `README.md` dosyanın içine yapıştırman yeterlidir (Markdown formatında olduğu için GitHub'da ikonlar, kod blokları ve başlıklarla çok şık görünecektir):
```markdown
# 🎓 KTÜ LMS - Gelişmiş E-Öğrenme ve Kurs Yönetim Platformu

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-Secure-green.svg)
![Architecture](https://img.shields.io/badge/Architecture-MVC-orange.svg)
![Deployment](https://img.shields.io/badge/Deployment-AWS_EC2-yellow.svg)

Bu proje, İleri Web Uygulamaları dersi kapsamında **MVC (Model-View-Template)** mimarisi baz alınarak geliştirilmiş kapsamlı bir E-Öğrenme (LMS) ve Kurs Yönetim Sistemidir. Öğrencilerin, eğitmenlerin ve yöneticilerin farklı yetki ve arayüzlerle etkileşime girdiği; e-ticaret, ölçme-değerlendirme, sosyal iletişim ve gelişmiş güvenlik katmanlarını barındıran modern bir web uygulamasıdır.

---

## 🌟 Temel Özellikler

Uygulama, Rol Bazlı Yetkilendirme (Role-Based Access Control) prensibiyle 3 ana kullanıcı tipine hizmet vermektedir:

### 🧑‍🎓 Öğrenci (Student) Özellikleri
*   **Gelişmiş Profil & E-Ticaret:** Kursları sepete ekleme, indirim kuponu kullanma ve güvenli ödeme simülasyonu.
*   **İnteraktif Öğrenme:** Video dersleri (YouTube Embed entegrasyonu) izleme ve ders ilerleme (progress) takibi.
*   **Ölçme ve Değerlendirme:** Kurs sonu Quiz'lerini çözme ve Eğitmenlere ödev (Assignment) teslim etme.
*   **Sosyal Etkileşim:** Diğer kullanıcılarla takipleşme/arkadaş olma, özel mesajlaşma ve kurslara yıldızlı yorum/değerlendirme bırakma.

### 👨‍🏫 Eğitmen (Instructor) Özellikleri
*   **Kurs & Müfredat Yönetimi (CRUD):** Kurs oluşturma, düzenleme, arşivleme. Modül ve ders içeriklerini hiyerarşik olarak yönetme.
*   **Dinamik Kategori Sistemi:** Listede bulunmayan kategoriler için sistem yöneticisine yeni kategori önerme.
*   **Öğrenci Yönetimi:** Öğrenci ödevlerini inceleme, notlandırma ve kursa kayıtlı öğrencilere toplu duyuru (Announcement) gönderme.
*   **Finansal Takip:** Eğitmen paneli (Dashboard) üzerinden toplam öğrenci sayısını, brüt ve komisyon kesilmiş net geliri görüntüleme.

### 🛡️ Admin (Yönetici) Özellikleri
*   **Onay Mekanizması:** Yeni eğitmenlik başvurularını ve taslak aşamasından çıkan kursları inceleme, onaylama veya reddetme.
*   **Sistem Logları:** Platformdaki tüm kritik eylemleri (kurs silme, onaylama vb.) `SystemLog` paneli üzerinden anlık takip etme.

---

## 🔐 Güvenlik Katmanı
Proje, web güvenlik standartlarına (OWASP) uygun olarak aşağıdaki korumalarla donatılmıştır:
*   **Brute-Force Koruması:** Kaba kuvvet saldırılarını engellemek için başarısız giriş denemesi sınırlandırması ve oturum (session) zaman aşımı kontrolü.
*   **Veri Güvenliği:** Parolaların PBKDF2 algoritması ile hashlenmesi, tüm formlarda CSRF token kullanımı ve XSS/SQL Injection önlemleri.
*   **İzole Hata Sayfaları:** Sistem zafiyetlerini ve konfigürasyon detaylarını gizlemek adına projelendirilmiş özel `400`, `403`, `404` ve `500` hata sayfaları.

---

## 🛠️ Kullanılan Teknolojiler
*   **Backend:** Python, Django Framework (MVC Mimari Yapısı)
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, SweetAlert2
*   **Veritabanı:** SQLite / PostgreSQL (12+ İlişkili Tablo)
*   **Medya Yönetimi:** Pillow (Profil ve kurs kapak resimleri için)
*   **Sunucu & Deployment:** Amazon Web Services (AWS) EC2 (Ubuntu t2.micro), Gunicorn & Nginx

---

## 🚀 Kurulum ve Çalıştırma Adımları (Lokal Geliştirme)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla terminalinizde uygulayın:

**1. Repoyu Klonlayın**
git clone https://github.com/KULLANICI_ADIN/REPO_ADIN.git
cd REPO_ADIN

---

# Windows İçin:
python -m venv venv
venv\Scripts\activate

---

2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin
# macOS / Linux İçin:
python3 -m venv venv
source venv/bin/activate

---

3. Bağımlılıkları (Requirements) Yükleyin
pip install -r requirements.txt

---

4. Veritabanı Göçlerini (Migrations) Uygulayın
python manage.py makemigrations
python manage.py migrate

---

5. Yönetici (Admin) Hesabı Oluşturun
python manage.py createsuperuser
(Sizden istenen kullanıcı adı, email ve şifre bilgilerini girin)

---

6. Geliştirme Sunucusunu Başlatın
python manage.py runserver

---

👥 Geliştirici Ekip
Bu proje, aşağıdaki ekip üyeleri tarafından iş bölümü yapılarak geliştirilmiştir:

Hasan Yücel: MVC iskeleti, Veritabanı Mimarisi, E-Ticaret Modülü, Kurs/Müfredat CRUD işlemleri, Sistem Logları.

Muhammet Zahit Aydın: Admin Onay Paneli, Quiz ve Ödev (Assessment) Sistemleri, Sertifika Algoritması, Güvenlik (CSRF/Session) Optimizasyonları.

Hüseyin Şahin: UI/UX Tasarım ve Mobil Uyumluluk, Özel Hata Sayfaları, Mesajlaşma ve Sosyal Etkileşim Modülleri, Şifre Sıfırlama Sistemleri.