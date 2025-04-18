document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("register-form");
  const username = document.getElementById("id_username");
  const email = document.getElementById("id_email");
  const birthdate = document.getElementById("id_birthdate");
  const password = document.getElementById("id_password");
  const password2 = document.getElementById("id_password2");
  const checkbox = form.querySelector('input[name="agree"]');
  const submitBtn = document.getElementById("submit-btn");

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function validateForm() {
    const isUsernameFilled = username.value.trim() !== "";
    const isEmailFilled = email.value.trim() !== "";
    const isEmailValid = isValidEmail(email.value);
    const isBirthdateFilled = birthdate.value !== "";
    const isPasswordFilled = password.value !== "";
    const isPassword2Filled = password2.value !== "";
    const isPasswordsMatch = password.value === password2.value;
    const isCheckboxChecked = checkbox.checked;
  
    const isValid =
      isUsernameFilled &&
      isEmailFilled &&
      isEmailValid &&
      isBirthdateFilled &&
      isPasswordFilled &&
      isPassword2Filled &&
      isPasswordsMatch &&
      isCheckboxChecked;
  
    // Активируем кнопку, если все поля верны
    submitBtn.disabled = !isValid;
    submitBtn.classList.toggle("active", isValid);
  }
  

  form.addEventListener("input", validateForm);
  checkbox.addEventListener("change", validateForm);
});
