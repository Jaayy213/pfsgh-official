// Sticky Navbar using Bootstrap classes
const navbar = document.getElementById('mainNavbar');
const topBar = document.querySelector('.top-bar');
const topBarHeight = topBar.offsetHeight;

let lastScrollTop = 0;
let isFixed = false;

window.addEventListener('scroll', function () {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > topBarHeight + 50) {
        if (!isFixed) {
            navbar.classList.add('fixed-top');
            document.body.style.paddingTop = navbar.offsetHeight + 'px';
            isFixed = true;
        }
    } else {
        if (isFixed) {
            navbar.classList.remove('fixed-top');
            document.body.style.paddingTop = '0';
            isFixed = false;
        }
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Scrollspy enhancement
const scrollSpyEl = document.querySelector('[data-bs-spy="scroll"]');
if (scrollSpyEl) {
    const scrollSpy = bootstrap.ScrollSpy.getInstance(scrollSpyEl) || new bootstrap.ScrollSpy(scrollSpyEl);
}

// Smooth scrolling for anchor links with Bootstrap offset
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const navbarHeight = isFixed ? navbar.offsetHeight : 0;
            const offsetTop = target.offsetTop - navbarHeight - 20;

            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });

            // Close mobile menu if open
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                bootstrap.Collapse.getInstance(navbarCollapse)?.hide();
            }
        }
    });
});

//  Carousel with animation reset
const carousel = document.getElementById('heroCarousel');
carousel.addEventListener('slide.bs.carousel', function (e) {
    const activeSlide = e.relatedTarget;
    const title = activeSlide.querySelector('.carousel-title');
    const subtitle = activeSlide.querySelector('.carousel-subtitle');
    const btn = activeSlide.querySelector('.carousel-btn');

    // Reset animations for new slide
    [title, subtitle, btn].forEach(el => {
        if (el) {
            el.style.animation = 'none';
            el.offsetHeight; // Trigger reflow
            el.style.animation = null;
        }
    });
});

// Responsive carousel height adjustment
function adjustCarouselHeight() {
    const carouselEl = document.querySelector('.hero-carousel');
    const windowHeight = window.innerHeight;
    carouselEl.style.minHeight = windowHeight + 'px';
}

adjustCarouselHeight();
window.addEventListener('resize', adjustCarouselHeight);

// Initialize Bootstrap tooltips and popovers if needed
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
