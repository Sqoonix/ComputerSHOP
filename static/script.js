document.addEventListener("DOMContentLoaded", () => {
    const comparisonButtons = document.querySelectorAll(".btn-details");
    const compareBadge = document.querySelector(".compare-badge"); // Получаем элемент счетчика

    // Функция для обновления счетчика
    function updateComparisonCount() {
        const comparisonList = JSON.parse(localStorage.getItem("comparisonList")) || [];
        if (compareBadge) {
            if (comparisonList.length > 0) {
                compareBadge.textContent = comparisonList.length; // Set count to compareBadge
                compareBadge.style.display = "inline-flex"; // Make the badge visible
            } else {
                compareBadge.style.display = "none"; // Hide the badge if there are no items
            }
        }
    }

    // Вызов функции для первоначальной установки счетчика
    updateComparisonCount();

    // Функция для создания и отображения уведомления
    function showNotification(message) {
        // Найдем все текущие уведомления и закроем их
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => {
            notification.style.opacity = "0"; // Плавное исчезновение
            setTimeout(() => {
                notification.remove(); // Удаляем уведомление из DOM
            }, 500); // Задержка перед удалением
        });

        // Создаем новое уведомление
        const notification = document.createElement("div");
        notification.classList.add("notification");
        notification.textContent = message;

        // Добавляем уведомление в DOM
        document.body.appendChild(notification);

        // Через 1 секунду скрыть уведомление
        setTimeout(() => {
            notification.style.opacity = "0"; // Плавное исчезновение
            setTimeout(() => {
                notification.remove(); // Удаляем уведомление из DOM
            }, 500); // Задержка перед удалением
        }, 1000); // Уведомление исчезает через 3 секунды
    }


    comparisonButtons.forEach(button => {
        button.addEventListener("click", function () {
            const pcCard = this.closest(".pc-card");

            // Извлекаем данные о ПК
            const pcData = {
                name: pcCard.querySelector("h3").textContent,
                image: pcCard.querySelector("img").src,
                price: pcCard.querySelector(".price").textContent,
                specs: Array.from(pcCard.querySelectorAll(".spec")).map(spec => spec.textContent.trim())
            };

            // Получаем текущий список сравнений из localStorage
            let comparisonList = JSON.parse(localStorage.getItem("comparisonList")) || [];

            // Избегаем дубликатов
            if (!comparisonList.some(pc => pc.name === pcData.name)) {
                comparisonList.push(pcData);
                localStorage.setItem("comparisonList", JSON.stringify(comparisonList));

                // Показываем уведомление, что ПК добавлен в сравнение
                showNotification(`${pcData.name} добавлен в сравнение!`);
            } else {
                showNotification(`${pcData.name} уже есть в списке сравнения!`);
            }

            // Обновляем счетчик после добавления
            updateComparisonCount();
        });
    });
});
