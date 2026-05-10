document.addEventListener("DOMContentLoaded", () => {

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 4000);
    });

    const sidebarBtn = document.getElementById('toggle-sidebar-btn');
    const sidebar = document.getElementById('curriculum-sidebar');
    
    if (sidebarBtn && sidebar) {
        sidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');

            if (sidebar.classList.contains('active')) {
                sidebarBtn.innerHTML = '<i class="fas fa-times"></i> Menüyü Kapat';
            } else {
                sidebarBtn.innerHTML = '<i class="fas fa-bars"></i> Müfredat';
            }
        });
    }

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

    if (typeof APP_CONFIG !== 'undefined' && APP_CONFIG.isAuthenticated) {
        
        const timeoutDuration = 1800 * 1000;
        let inactivityTimer;

        function resetTimer() {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(() => {
                window.location.href = APP_CONFIG.logoutUrl;
            }, timeoutDuration);
        }

        window.onload = resetTimer;
        document.onmousemove = resetTimer;
        document.onkeypress = resetTimer;
        document.onscroll = resetTimer;
        document.onclick = resetTimer;
    }

});