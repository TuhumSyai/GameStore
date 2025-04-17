document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const birthdate = document.getElementById("birthdate");
    const password = document.getElementById("password");
    const password2 = document.getElementById("password2");
    const checkbox = form.querySelector('input[name="agree"]');
    const submitBtn = document.getElementById("submit-btn");
  
    function validateForm() {
      const isFilled =
        username.value.trim() &&
        email.value.trim() &&
        birthdate.value &&
        password.value &&
        password2.value;
  
      const isPasswordsMatch = password.value === password2.value;
      const isCheckboxChecked = checkbox.checked;
  
      if (isFilled && isPasswordsMatch && isCheckboxChecked) {
        submitBtn.disabled = false;
        submitBtn.classList.add("active");
      } else {
        submitBtn.disabled = true;
        submitBtn.classList.remove("active");
      }
    }
  
    form.addEventListener("input", validateForm);
    checkbox.addEventListener("change", validateForm);
  });