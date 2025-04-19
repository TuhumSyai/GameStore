// --------------- RAWG API + БАННЕР + ПОИСК ---------------

const API_KEY         = '2b27fe820d7a4aac84a82ad564f939f3';
const sidebar         = document.getElementById('randomGames');
const bannerImage     = document.getElementById('bannerImage');
const bannerTitle     = document.getElementById('bannerTitle');
const bannerDesc      = document.getElementById('bannerDescription');
const bannerProgress  = document.querySelector('.banner-progress');
const searchInput     = document.getElementById('searchInput');
const searchResults   = document.getElementById('searchResults');

let currentBannerIndex = 0;
let bannerGames        = [];
let bannerInterval;

// Обновить баннер
function updateBanner(game) {
  if (!game) return;
  bannerImage.src            = game.background_image;
  bannerTitle.textContent    = game.name;
  bannerDesc.textContent     = `🔥 ${game.name} — ${game.released || 'Без даты релиза'}`;
}

// Перезапуск анимации прогресса
function restartProgressAnimation() {
  if (!bannerProgress) return;
  bannerProgress.style.animation = 'none';
  bannerProgress.offsetHeight;
  bannerProgress.style.animation = 'bannerTimer 5s linear';
}

// Старт автопрокрутки баннера
function startBannerRotation() {
  clearInterval(bannerInterval);
  restartProgressAnimation();
  bannerInterval = setInterval(() => {
    currentBannerIndex = (currentBannerIndex + 1) % bannerGames.length;
    updateBanner(bannerGames[currentBannerIndex]);
    restartProgressAnimation();
  }, 5000);
}

// Поиск игр при вводе
async function searchGames(query) {
  if (!query) {
    searchResults.style.display = 'none';
    return;
  }

  try {
    const res  = await fetch(
      `https://api.rawg.io/api/games?key=${API_KEY}&search=${encodeURIComponent(query)}&page_size=8`
    );
    const data = await res.json();
    const games = data.results || [];

    // Построим список
    searchResults.innerHTML = games.map(g => `
      <li data-id="${g.id}">
        <img src="${g.background_image}" alt="${g.name}" />
        <span>${g.name}</span>
      </li>
    `).join('');
    searchResults.style.display = 'block';

    // По клику обновляем баннер
    searchResults.querySelectorAll('li[data-id]').forEach(li => {
      li.addEventListener('click', () => {
        const id = li.dataset.id;
        const game = games.find(x => x.id == id);
        if (game) {
          bannerGames = [game];
          currentBannerIndex = 0;
          updateBanner(game);
          restartProgressAnimation();
        }
        searchResults.style.display = 'none';
        searchInput.value = '';
      });
    });

  } catch (err) {
    console.error('Ошибка при поиске:', err);
  }
}

// Загрузка списка случайных игр
async function loadRandomGames() {
  if (!sidebar) return;
  try {
    const res  = await fetch(
      `https://api.rawg.io/api/games?key=${API_KEY}&page_size=40`
    );
    const data = await res.json();
    const all  = (data.results || []).filter(g => g.background_image);

    const random = [];
    const used   = new Set();
    while (random.length < 6 && used.size < all.length) {
      const i = Math.floor(Math.random() * all.length);
      if (!used.has(i)) {
        used.add(i);
        random.push(all[i]);
      }
    }

    sidebar.innerHTML = '';
    bannerGames = [...random];

    random.forEach((g, idx) => {
      const div = document.createElement('div');
      div.className = 'game-card';
      div.innerHTML = `
        <img src="${g.background_image}" alt="${g.name}" />
        <span>${g.name}</span>
      `;
      div.addEventListener('click', () => {
        currentBannerIndex = idx;
        updateBanner(g);
        startBannerRotation();
      });
      sidebar.appendChild(div);
    });

    updateBanner(bannerGames[0]);
    startBannerRotation();

  } catch (err) {
    sidebar.innerHTML = '<span style="color:red">Ошибка загрузки игр</span>';
    console.error('Ошибка при получении игр:', err);
  }
}

// Инициализируем
loadRandomGames();

// Подключаем поиск
if (searchInput) {
  searchInput.addEventListener('input', e => {
    const v = e.target.value.trim();
    if (v.length >= 2) searchGames(v);
    else searchResults.style.display = 'none';
  });
  // Скрываем при клике вне
  document.addEventListener('click', e => {
    if (!searchResults.contains(e.target) && e.target !== searchInput) {
      searchResults.style.display = 'none';
    }
  });
}
