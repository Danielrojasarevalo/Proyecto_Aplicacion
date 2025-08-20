document.querySelector(".hamburger").addEventListener("click", function () {
    const menu = document.getElementById("mobileMenu");
    menu.style.display = (menu.style.display === "flex") ? "none" : "flex";
});


document.addEventListener('DOMContentLoaded', function() {
    const acordeonHeaders = document.querySelectorAll('.acordeon-header');
    acordeonHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            content.classList.toggle('active');
            header.classList.toggle('active');
        });
    });
});