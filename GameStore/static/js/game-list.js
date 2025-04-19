const API_KEY       = 'b27fe820d7a4aac84a82ad564f939f3';
const sortSelect    = document.getElementById('sortSelect');
const genreFilters  = document.getElementById('genreFilters');
const resetBtn      = document.getElementById('resetFilters');
const gamesGrid     = document.getElementById('gamesGrid');

// 1) Загрузка жанров и отрисовка чекбоксов
async function loadGenres() {
  try {
    const res  = await fetch(`https://api.rawg.io/api/genres?key=${API_KEY}`);
    const data = await res.json();
    genreFilters.innerHTML = (data.results || [])
      .map(g => `<label><input type="checkbox" value="${g.slug}" /> ${g.name}</label>`)
      .join('');
  } catch (err) {
    console.error('Не удалось загрузить жанры', err);
  }
}

// 2) Загрузка игр с применением фильтров
async function loadFilteredGames() {
  let url = `https://api.rawg.io/api/games?key=${API_KEY}&page_size=20`;
  const ordering = sortSelect.value;
  const checked  = Array.from(
    genreFilters.querySelectorAll('input:checked'),
    cb => cb.value
  ).join(',');

  if (ordering) url += `&ordering=${ordering}`;
  if (checked)  url += `&genres=${checked}`;

  try {
    const res  = await fetch(url);
    const data = await res.json();
    const games= data.results || [];

    gamesGrid.innerHTML = games.map(game => `
      <div class="catalog-card" data-id="${game.id}">
        <img src="${game.background_image}" alt="${game.name}" />
        <div class="info">
          <h4>${game.name}</h4>
          <p>${game.released || '—'}</p>
        </div>
      </div>
    `).join('');

    // Можно добавить клик по карточке:
    document.querySelectorAll('.catalog-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = card.dataset.id;
        // TODO: открыть страницу игры или переключить баннер
        console.log('Clicked game ID:', id);
      });
    });

  } catch (err) {
    console.error('Ошибка при загрузке игр:', err);
  }
}

// 3) Слушатели фильтров
sortSelect.addEventListener('change', loadFilteredGames);
genreFilters.addEventListener('change', loadFilteredGames);
resetBtn.addEventListener('click', () => {
  sortSelect.value = 'added';
  genreFilters.querySelectorAll('input').forEach(cb => cb.checked = false);
  loadFilteredGames();
});

// 4) Инициализация
loadGenres().then(loadFilteredGames);
