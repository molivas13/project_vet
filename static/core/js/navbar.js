(function () {
    const navbar = document.getElementById('mainNavbar');
    if (!navbar) return;

    const OFFSET = 80;
    const ON = 'navbar-scrolled';
    const OFF = 'navbar-transparent';

    function update() {
        if (window.scrollY > OFFSET) {
            navbar.classList.add(ON);
            navbar.classList.remove(OFF);
        } else {
            navbar.classList.remove(ON);
            navbar.classList.add(OFF);
        }
    }

    update();
    window.addEventListener('scroll', update, { passive: true });
})();
