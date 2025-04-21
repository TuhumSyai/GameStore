document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
  
    searchInput.addEventListener('input', function () {
      const query = this.value.trim();
  
      if (query.length === 0) {
        searchResults.innerHTML = '';
        return;
      }
  
      fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          searchResults.innerHTML = '';
  
          if (data.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'Ничего не найдено';
            searchResults.appendChild(li);
            return;
          }
  
          data.forEach(game => {
            const li = document.createElement('li');
            li.innerHTML = `
              <a href="/games/${game.id}/" style="display: flex; align-items: center; gap: 10px;">
                <img src="${game.background_image}" alt="${game.name}" />
                <span>${game.name}</span>
              </a>
            `;
            searchResults.appendChild(li);
          });
        })
        .catch(error => {
          console.error('Ошибка при поиске:', error);
        });
    });
  
    // Закрытие результатов при клике вне поля
    document.addEventListener('click', function (event) {
      if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
        searchResults.innerHTML = '';
      }
    });
  });

  document.addEventListener("click", function (e) {
    const isClickInside = input.contains(e.target) || results.contains(e.target);
    if (!isClickInside) {
      results.style.display = "none";
    }
  });

  const input = document.getElementById("searchInput");
const results = document.getElementById("searchResults");

input.addEventListener("input", function () {
  const query = this.value.trim();

  if (query === "") {
    results.style.display = "none";
    return;
  }

  // иначе — показать и выполнить поиск
  results.style.display = "block";

  // Здесь можно обновить содержимое UL по результатам
});