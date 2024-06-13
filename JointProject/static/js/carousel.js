document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelector('.slides');
    const slideImages = document.querySelectorAll('.slide');
    let currentIndex = 0;

    function showSlide(index) {
        slides.style.transform = `translateX(-${index * 100}%)`;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slideImages.length;
        showSlide(currentIndex);
    }

    // Mostrar la primera imagen inmediatamente
    showSlide(currentIndex);

    // Configurar el intervalo para cambiar las imágenes
    setInterval(nextSlide, 3000); // Cambiar a 3 segundos
});
