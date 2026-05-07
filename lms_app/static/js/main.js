document.addEventListener("DOMContentLoaded", () => {
    
    // ==========================================
    // 1. DJANGO UYARI MESAJLARINI OTOMATİK GİZLEME
    // ==========================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // 4 saniye bekle
        setTimeout(() => {
            // Yumuşak geçiş için CSS ayarları
            alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            
            // Animasyon bitince elementi sayfadan tamamen sil (0.5 saniye sonra)
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 4000);
    });


    // ==========================================
    // 2. DERS İZLEME EKRANI - YAN MENÜ (MÜFREDAT) AÇ/KAPAT
    // ==========================================
    const sidebarBtn = document.getElementById('toggle-sidebar-btn');
    const sidebar = document.getElementById('curriculum-sidebar');
    
    if (sidebarBtn && sidebar) {
        sidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            
            // Menü durumuna göre buton içeriğini değiştir
            if (sidebar.classList.contains('active')) {
                sidebarBtn.innerHTML = '<i class="fas fa-times"></i> Menüyü Kapat';
            } else {
                sidebarBtn.innerHTML = '<i class="fas fa-bars"></i> Müfredat';
            }
        });
    }


    // ==========================================
    // 3. ŞİFRE GÜVENLİĞİ KONTROLÜ (KAYIT EKRANI)
    // ==========================================
    // Not: Django varsayılan olarak şifre alanlarına 'id_password' veya 'id_password1' IDsini verir.
    const passwordInput = document.getElementById('id_password') || document.getElementById('id_password1');
    const passwordFeedback = document.getElementById('password-feedback'); 
    
    if (passwordInput && passwordFeedback) {
        passwordInput.addEventListener('input', () => {
            const val = passwordInput.value;
            
            if (val.length === 0) {
                passwordFeedback.textContent = "";
            } else if (val.length < 8) {
                passwordFeedback.textContent = "Şifreniz en az 8 karakter olmalıdır.";
                passwordFeedback.style.color = "#dc3545"; // Kırmızı (Tehlike)
            } else {
                passwordFeedback.textContent = "Şifre uzunluğu yeterli.";
                passwordFeedback.style.color = "#198754"; // Yeşil (Güvenli)
            }
        });
    }


    // ==========================================
    // 4. SİLME İŞLEMLERİ İÇİN ONAY PENCERESİ
    // ==========================================
    // HTML'de class="confirm-delete" olan tüm butonlara/linklere uygulanır
    const deleteButtons = document.querySelectorAll('.confirm-delete');
    
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmMessage = btn.getAttribute('data-confirm-msg') || "Bu işlemi geri alamayacaksınız. Silmek istediğinize emin misiniz?";
            
            // Eğer kullanıcı "İptal"e basarsa, e.preventDefault() ile linkin çalışmasını durduruyoruz
            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });


    // ==========================================
    // 5. YUMUŞAK KAYDIRMA (SMOOTH SCROLL)
    // ==========================================
    // Sayfa içi linklere (örn: href="#reviews") tıklandığında aniden atlamak yerine yumuşakça kayar
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });


    // ==========================================
    // 6. OTOMATİK ÇIKIŞ (INACTIVITY TIMER)
    // ==========================================
    // APP_CONFIG objesi base.html'den geliyorsa ve kullanıcı giriş yapmışsa çalışır
    if (typeof APP_CONFIG !== 'undefined' && APP_CONFIG.isAuthenticated) {
        
        const timeoutDuration = 1800 * 1000; // 30 dakika (milisaniye cinsinden)
        let inactivityTimer;

        function resetTimer() {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(() => {
                // Süre dolduğunda HTML'den aldığımız güvenli URL'e yönlendir
                window.location.href = APP_CONFIG.logoutUrl; 
            }, timeoutDuration);
        }

        // Kullanıcının hareketlerini dinle
        window.onload = resetTimer;
        document.onmousemove = resetTimer;
        document.onkeypress = resetTimer;
        document.onscroll = resetTimer;
        document.onclick = resetTimer;
    }

});