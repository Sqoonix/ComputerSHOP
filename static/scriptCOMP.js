document.addEventListener("DOMContentLoaded", function () {
    // Находим контейнер для сравнения
    const comparisonGrid = document.getElementById('comparison-grid');
    if (!comparisonGrid) {
        console.error("Контейнер для сравнения не найден. Проверьте HTML.");
        return;
    }

    // Загружаем данные из localStorage
    const comparisonList = JSON.parse(localStorage.getItem('comparisonList')) || [];

    if (comparisonList.length === 0) {
        comparisonGrid.innerHTML = '<p>Список для сравнения пуст.</p>';
        return;
    }

    // Генерируем карточки для каждого ПК
    comparisonList.forEach((pcData) => {
        const pcCard = document.createElement('div');
        pcCard.classList.add('pc-card');

        pcCard.innerHTML = `
            <img src="${pcData.image}" alt="${pcData.title}">
            <h3>${pcData.title}</h3>
            <p>${pcData.description}</p>
            <div class="price-container">
                <p class="price">${pcData.price}</p>
            </div>
            <div class="specs">
                ${pcData.specs.map(spec => `<div class="spec">${spec}</div>`).join('')}
            </div>
        `;

        comparisonGrid.appendChild(pcCard);
    });

    // Очистка списка
    const clearComparisonButton = document.querySelector('.btn-clear-comparison');
    if (clearComparisonButton) {
        clearComparisonButton.addEventListener('click', () => {
            localStorage.removeItem('comparisonList');
            comparisonGrid.innerHTML = '<p>Список для сравнения очищен.</p>';
        });
    }
});
