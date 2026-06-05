// login.js

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector("form");
  const forgotPassLink = document.querySelector(".forgot-password");

  // مدیریت فرم ورود
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const email = document.querySelector('input[type="email"]').value;
      const password = document.querySelector('input[type="password"]').value;
      const rememberMe = document.querySelector(
        'input[type="checkbox"]',
      )?.checked;

      if (!email || !password) {
        alert("لطفاً ایمیل و رمز عبور را وارد کنید.");
        return;
      }

      // شبیه‌سازی ورود
      const submitBtn = loginForm.querySelector(".btn-submit");
      submitBtn.innerHTML = "در حال احراز هویت...";
      submitBtn.disabled = true;

      setTimeout(() => {
        // در دنیای واقعی اینجا توکن دریافت می‌شود
        if (rememberMe) {
          console.log("Token will be saved in LocalStorage");
        } else {
          console.log("Token will be saved in SessionStorage");
        }

        // انتقال به صفحه اول پنل (تراکنش‌ها یا داشبورد)
        window.location.href = "transactions.html";
      }, 1000);
    });
  }

  // مدیریت فراموشی رمز عبور
  if (forgotPassLink) {
    forgotPassLink.addEventListener("click", (e) => {
      e.preventDefault();
      const email = prompt(
        "لطفاً ایمیل خود را برای بازیابی رمز عبور وارد کنید:",
      );
      if (email) {
        alert(`لینک بازیابی رمز عبور به ${email} ارسال شد.`);
      }
    });
  }
});
