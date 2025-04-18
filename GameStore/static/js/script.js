document.addEventListener('DOMContentLoaded', () => {
  const usernameInput = document.getElementById('id_username');
  const passwordInput = document.getElementById('id_password');
  const submitBtn = document.getElementById('submit-btn');
  const errorText = document.querySelector('.error-message');
  const loginForm = document.getElementById('login-form');

  if (!usernameInput || !passwordInput || !submitBtn || !loginForm) return;

  function validateForm() {
    const isUsernameFilled = usernameInput.value.trim() !== '';
    const isPasswordFilled = passwordInput.value.trim() !== '';

    submitBtn.disabled = !(isUsernameFilled && isPasswordFilled);
    submitBtn.classList.toggle('active', isUsernameFilled && isPasswordFilled);
  }

  usernameInput.addEventListener('input', validateForm);
  passwordInput.addEventListener('input', validateForm);

  usernameInput.addEventListener('blur', () => {
    const value = usernameInput.value.trim();
    if (value === '') {
      errorText.textContent = 'Поле обязательно для заполнения';
      errorText.style.display = 'block';
    } else {
      errorText.style.display = 'none';
    }
  });

  loginForm.addEventListener('submit', function (e) {
    if (submitBtn.disabled) {
      e.preventDefault();
    }
  });
});
