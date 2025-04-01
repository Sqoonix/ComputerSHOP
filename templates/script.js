document.addEventListener("DOMContentLoaded", () => {
    const comparisonButtons = document.querySelectorAll(".btn-details");

    comparisonButtons.forEach(button => {
        button.addEventListener("click", function () {
            const pcCard = this.closest(".pc-card");

            const pcData = {
                name: pcCard.querySelector("h3").textContent,
                image: pcCard.querySelector("img").src,
                price: pcCard.querySelector(".price").textContent,
                specs: Array.from(pcCard.querySelectorAll(".spec")).map(spec => spec.textContent.trim())
            };

            let comparisonList = JSON.parse(localStorage.getItem("comparisonList")) || [];

            if (!comparisonList.some(pc => pc.name === pcData.name)) {
                comparisonList.push(pcData);
                localStorage.setItem("comparisonList", JSON.stringify(comparisonList));
                alert(`${pcData.name} добавлен в сравнение!`);
            } else {
                alert(`${pcData.name} уже есть в списке сравнения!`);
            }
        });
    });
});
