const slides = document.querySelector('.slides');
const slide = document.querySelectorAll('.slide');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');
let currentIndex = 0;

function showSlide(index) {
    if (index < 0) {
        currentIndex = slide.length - 1;
    } else if (index >= slide.length) {
        currentIndex = 0;
    } else {
        currentIndex = index;
    }
    slides.style.transform = 'translateX(' + (-currentIndex * 100) + '%)';
}

prevButton.addEventListener('click', () => {
    showSlide(currentIndex - 1);
});

nextButton.addEventListener('click', () => {
    showSlide(currentIndex + 1);
});

// Автоматическая смена слайдов
setInterval(() => {
    showSlide(currentIndex + 1);
}, 3000); // смена каждые 3 секунды