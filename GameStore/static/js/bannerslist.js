const bannerImage = document.getElementById('bannerImage');
const bannerTitle = document.getElementById('bannerTitle');
const bannerDesc = document.getElementById('bannerDescription');
const bannerProgress = document.querySelector('.banner-progress');
const games = JSON.parse(document.getElementById('games-data').textContent);
const gameCards = document.querySelectorAll('.game-card');
const bannerDetailBtn = document.getElementById('bannerDetailBtn');


let currentBannerIndex = 0;
let bannerInterval;

function updateBanner(index) {
  const game = games[index];
  if (!game) return;
  
  bannerImage.src = game.background_image || '/static/img/default_banner.jpg';
  bannerTitle.textContent = game.name;
  bannerDesc.textContent = '\u200B';

  bannerDetailBtn.href = `/games/${game.id}/`;
}

function restartProgressAnimation() {
  if (!bannerProgress) return;
  bannerProgress.style.animation = 'none';
  bannerProgress.offsetHeight;
  bannerProgress.style.animation = 'bannerTimer 5s linear';
}

function startBannerRotation() {
  clearInterval(bannerInterval); // Сначала сбрасываем, чтобы не было нескольких таймеров
  bannerInterval = setInterval(() => {
    currentBannerIndex = (currentBannerIndex + 1) % games.length;
    updateBanner(currentBannerIndex);
    restartProgressAnimation();
  }, 5000);
}

// Инициализация баннера
if (games.length > 0) {
  updateBanner(currentBannerIndex);
  startBannerRotation();
}

// Обработка кликов по карточкам
gameCards.forEach((card) => {
  const index = parseInt(card.getAttribute('data-index'));
  card.addEventListener('click', () => {
    currentBannerIndex = index;
    clearInterval(bannerInterval);               // Очищаем текущий таймер
    updateBanner(index);                         // Обновляем баннер
    restartProgressAnimation();                  // Перезапускаем прогресс
    startBannerRotation();                       // Запускаем новый таймер
  });
});
