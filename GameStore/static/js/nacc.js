const daySelect = document.getElementById('day');
const monthSelect = document.getElementById('month');
const yearSelect = document.getElementById('year');
const continueBtn = document.getElementById('continue-btn');

// Заполнение дней
for (let i = 1; i <= 31; i++) {
  const opt = document.createElement('option');
  opt.value = i;
  opt.textContent = i;
  daySelect.appendChild(opt);
}

// Заполнение годов (от 2024 к 1905)
const currentYear = new Date().getFullYear();
for (let i = currentYear; i >= 1905; i--) {
  const opt = document.createElement('option');
  opt.value = i;
  opt.textContent = i;
  yearSelect.appendChild(opt);
}

// Проверка заполненности
function validateDOB() {
  const valid = daySelect.value && monthSelect.value && yearSelect.value;
  continueBtn.disabled = !valid;
  continueBtn.classList.toggle('active', valid);
}

[daySelect, monthSelect, yearSelect].forEach(select => {
  select.addEventListener('change', validateDOB);
});


