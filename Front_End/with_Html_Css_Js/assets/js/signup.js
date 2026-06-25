// signup.js

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.querySelector("form");

  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      e.preventDefault(); // جلوگیری از رفرش صفحه

      // دریافت مقادیر فیلدها (فرض بر این است که inputها این idها را دارند)
      const fullName = document.getElementById("fullname")?.value || "";
      const email = document.getElementById("email")?.value || "";
      const password = document.getElementById("password")?.value || "";
      const confirmPassword =
        document.getElementById("confirm-password")?.value || "";

      // اعتبارسنجی پایه
      if (!fullName || !email || !password || !confirmPassword) {
        alert("لطفاً تمامی فیلدها را پر کنید.");
        return;
      }

      // بررسی طول رمز عبور
      if (password.length < 8) {
        alert("رمز عبور باید حداقل ۸ کاراکتر باشد.");
        return;
      }

      // بررسی تطابق رمزها
      if (password !== confirmPassword) {
        alert("رمز عبور و تکرار آن با هم مطابقت ندارند!");
        return;
      }

      // شبیه‌سازی ثبت‌نام موفق و انتقال به صفحه ورود
      const submitBtn = signupForm.querySelector(".btn-submit");
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML =
        '<i class="fas fa-circle-notch fa-spin"></i> در حال ایجاد حساب...';
      submitBtn.disabled = true;

      setTimeout(() => {
        alert(
          `ثبت‌نام با موفقیت انجام شد!\nبه سیستم پایش مالی خوش آمدید، ${fullName}.`,
        );
        window.location.href = "login.html"; // انتقال کاربر به صفحه ورود
      }, 1500);
    });
  }
});
