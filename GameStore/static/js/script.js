const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const submitBtn = document.getElementById('submit-btn');
const errorText = document.querySelector('.error-message');

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) && email.endsWith('.com');
}

function validateForm() {
  const isEmailValid = isValidEmail(emailInput.value);
  const isPasswordFilled = passwordInput.value.trim() !== '';

  submitBtn.disabled = !(isEmailValid && isPasswordFilled);
  submitBtn.classList.toggle('active', isEmailValid && isPasswordFilled);
}

emailInput.addEventListener('blur', () => {
  errorText.style.display = emailInput.value.trim() === '' ? 'block' : 'none';
});

emailInput.addEventListener('input', validateForm);
passwordInput.addEventListener('input', validateForm);
