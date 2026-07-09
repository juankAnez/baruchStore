document.addEventListener('DOMContentLoaded', function () {
    // GSAP animations for hero
    gsap.from('.hero-content', {
        opacity: 0,
        y: 60,
        duration: 1,
        ease: 'power3.out'
    });
});