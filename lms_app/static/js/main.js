document.addEventListener("DOMContentLoaded", () => {

    /* =========================================
       1. GENEL SİSTEM SCRİPTLERİ
       ========================================= */

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

/* =========================================
    2. CHECKOUT (ÖDEME) ÖZEL SCRİPTLERİ
   ========================================= */
// Tooltip tetikleyici (Bootstrap bağımlı)
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // 1. İSİM ALANI: Sadece harf girilebilir, sayıları otomatik siler
    const cardNameInput = document.getElementById('cardName');
    if (cardNameInput) {
        cardNameInput.addEventListener('input', function () {
            this.value = this.value.replace(/[0-9]/g, '');
        });
    }

    // 2. KART NUMARASI: Sadece sayı ve otomatik boşluk
    const cardNumberInput = document.getElementById('cardNumber');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function () {
            let value = this.value.replace(/\D/g, '');
            let formattedValue = value.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
            this.value = formattedValue;
        });
    }

    // 3. SON KULLANMA TARİHİ: Sadece sayı ve otomatik Slash
    const cardExpiryInput = document.getElementById('cardExpiry');
    if (cardExpiryInput) {
        cardExpiryInput.addEventListener('input', function (e) {
            let value = this.value.replace(/\D/g, '');

            if (e.inputType === 'deleteContentBackward') {
                this.value = value;
                return;
            }

            if (value.length > 2) {
                this.value = value.substring(0, 2) + '/' + value.substring(2, 4);
            } else {
                this.value = value;
            }
        });
    }

    // 4. CVV ALANI: Sadece sayı
    const cardCvvInput = document.getElementById('cardCvv');
    if (cardCvvInput) {
        cardCvvInput.addEventListener('input', function () {
            this.value = this.value.replace(/\D/g, '');
        });
    }

    // 5. OTP VE FORM SUBMIT
    const checkoutForm = document.getElementById('checkoutForm');
    const otpModalElement = document.getElementById('otpModal');

    if (checkoutForm && otpModalElement) {
        // Bootstrap Modal objesini oluştur
        let otpModal;
        if (typeof bootstrap !== 'undefined') {
            otpModal = new bootstrap.Modal(otpModalElement);
        }

        let otpInterval;

        checkoutForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (otpModal) {
                otpModal.show();
            }
            startOtpTimer();
        });

        const otpInputs = document.querySelectorAll('.otp-inputs input');
        otpInputs.forEach((input, index) => {
            input.addEventListener('input', function() {
                this.value = this.value.replace(/\D/g, '');
                if (this.value.length === 1 && index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            });
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Backspace' && !this.value && index > 0) {
                    otpInputs[index - 1].focus();
                }
            });
        });

        const verifyOtpBtn = document.getElementById('verifyOtpBtn');
        if (verifyOtpBtn) {
            verifyOtpBtn.addEventListener('click', function() {
                verifyOtpBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>İşleniyor...';
                verifyOtpBtn.disabled = true;

                setTimeout(() => {
                    checkoutForm.submit();
                }, 1500);
            });
        }

        function startOtpTimer() {
            clearInterval(otpInterval);
            let time = 180;
            const timerDisplay = document.getElementById('otpTimer');

            if (timerDisplay) {
                otpInterval = setInterval(() => {
                    let minutes = Math.floor(time / 60);
                    let seconds = time % 60;
                    timerDisplay.textContent = `0${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
                    time--;

                    if (time < 0) {
                        clearInterval(otpInterval);
                        timerDisplay.textContent = "Süre doldu!";
                        if (verifyOtpBtn) verifyOtpBtn.disabled = true;
                    }
                }, 1000);
            }
        }
    }
});