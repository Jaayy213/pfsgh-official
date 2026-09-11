document.addEventListener('DOMContentLoaded', function () {
    // -----------------------------------------------------------------
    // 1. Sticky Navbar Logic
    // -----------------------------------------------------------------
    const navbar = document.getElementById('mainNavbar');
    const topBar = document.querySelector('.top-bar');

    if (navbar) {
        const topBarHeight = topBar ? topBar.offsetHeight : 0;
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
        });
    }

    // -----------------------------------------------------------------
    // 2. Scrollspy & Tooltips Initialization
    // -----------------------------------------------------------------
    if (typeof bootstrap !== 'undefined') {
        const scrollSpyEl = document.querySelector('[data-bs-spy="scroll"]');
        if (scrollSpyEl) {
            bootstrap.ScrollSpy.getInstance(scrollSpyEl) || new bootstrap.ScrollSpy(scrollSpyEl);
        }

        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        [...tooltipTriggerList].forEach(el => new bootstrap.Tooltip(el));

        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        [...popoverTriggerList].forEach(el => new bootstrap.Popover(el));
    }

    // -----------------------------------------------------------------
    // 3. Smooth Scroll for Internal Anchors
    // -----------------------------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (!href || href === '#' || href === '#quote') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const isFixed = navbar && navbar.classList.contains('fixed-top');
                const navbarHeight = isFixed ? navbar.offsetHeight : 0;
                const offsetTop = target.offsetTop - navbarHeight - 20;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });

                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse && navbarCollapse.classList.contains('show') && typeof bootstrap !== 'undefined') {
                    bootstrap.Collapse.getInstance(navbarCollapse)?.hide();
                }
            }
        });
    });

    // -----------------------------------------------------------------
    // 4. Hero Carousel Animations Reset & Auto-Height
    // -----------------------------------------------------------------
    const carousel = document.getElementById('heroCarousel');
    if (carousel) {
        carousel.addEventListener('slide.bs.carousel', function (e) {
            const activeSlide = e.relatedTarget;
            if (activeSlide) {
                const title = activeSlide.querySelector('.carousel-title');
                const subtitle = activeSlide.querySelector('.carousel-subtitle');
                const btn = activeSlide.querySelector('.carousel-btn');

                [title, subtitle, btn].forEach(el => {
                    if (el) {
                        el.style.animation = 'none';
                        el.offsetHeight; // Trigger reflow
                        el.style.animation = '';
                    }
                });
            }
        });

        function adjustCarouselHeight() {
            const windowHeight = window.innerHeight;
            carousel.style.minHeight = windowHeight + 'px';
        }

        adjustCarouselHeight();
        window.addEventListener('resize', adjustCarouselHeight);
    }

    // -----------------------------------------------------------------
    // 5. Scroll to Top Button
    // -----------------------------------------------------------------
    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (scrollToTopBtn) {
        window.addEventListener('scroll', function () {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.classList.add('show');
            } else {
                scrollToTopBtn.classList.remove('show');
            }
        });

        scrollToTopBtn.addEventListener('click', function () {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // -----------------------------------------------------------------
    // 6. Process Cards Animation
    // -----------------------------------------------------------------
    const processCards = document.querySelectorAll('.process-card');
    if (processCards.length > 0) {
        const processObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 200);
                }
            });
        }, { threshold: 0.1 });

        processCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease';
            processObserver.observe(card);

            card.addEventListener('click', function () {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }

    // -----------------------------------------------------------------
    // 7. Service Cards Animation
    // -----------------------------------------------------------------
    const serviceCards = document.querySelectorAll('.service-item, .service-card');
    if (serviceCards.length > 0) {
        const serviceObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateX(0)';
                    }, index * 100);
                    serviceObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        serviceCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateX(-18px)';
            card.style.transition = 'opacity 0.55s ease, transform 0.55s ease';
            serviceObserver.observe(card);

            card.addEventListener('click', function () {
                if (!this.classList.contains('service-card')) return;
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }

    // -----------------------------------------------------------------
    // 8. Stat Counter Animation
    // -----------------------------------------------------------------
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length > 0) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const text = target.textContent;
                    if (text.includes('+')) {
                        animateNumber(target, 0, parseInt(text, 10), 1000);
                    }
                    statsObserver.unobserve(target);
                }
            });
        });

        statNumbers.forEach(stat => statsObserver.observe(stat));

        function animateNumber(element, start, end, duration) {
            let startTime = null;
            const step = (timestamp) => {
                if (!startTime) startTime = timestamp;
                const progress = Math.min((timestamp - startTime) / duration, 1);
                const value = Math.floor(progress * (end - start) + start);
                element.textContent = value + '+';
                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            };
            requestAnimationFrame(step);
        }
    }

    // -----------------------------------------------------------------
    // 9. About Page Card Animations
    // -----------------------------------------------------------------
    const cards = document.querySelectorAll('.card-custom');
    const values = document.querySelectorAll('.value-item');
    if (cards.length > 0 || values.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const delay = entry.target.dataset.delay || 0;
                    setTimeout(() => {
                        entry.target.classList.add('animate-in');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        cards.forEach(card => observer.observe(card));
        values.forEach(value => observer.observe(value));
    }

    // -----------------------------------------------------------------
    // 10. Quote Modal Handling & AJAX Form Submission
    // -----------------------------------------------------------------
    const modalEl = document.getElementById('quoteModal');
    if (modalEl) {
        if (window.location.hash === '#quote') {
            openQuoteModal();
        }

        modalEl.addEventListener('hidden.bs.modal', function () {
            resetForm();
        });
    }

    const quoteForm = document.getElementById('quoteForm');
    if (quoteForm) {
        quoteForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const selectedServices = document.querySelectorAll('input[name="services"]:checked');
            if (selectedServices.length === 0) {
                alert('Please select at least one service.');
                return;
            }

            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.disabled = true;

            fetch('/quotes/submit/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    quoteForm.style.display = 'none';
                    const successMsg = document.getElementById('successMessage');
                    if (successMsg) {
                        successMsg.style.display = 'block';
                    }
                } else {
                    alert('Submission failed. Please check your inputs and try again.');
                }
            })
            .catch(error => {
                console.error('Error submitting quote:', error);
                alert('An unexpected error occurred. Please try again.');
            })
            .finally(() => {
                if (submitBtn) submitBtn.disabled = false;
            });
        });
    }

    // -----------------------------------------------------------------
    // 11. Video Modal Click Handling
    // -----------------------------------------------------------------
    const closeBtn = document.querySelector(".close-btn");
    if (closeBtn) {
        closeBtn.onclick = closeModal;
    }

    window.addEventListener('click', function(event) {
        const modal = document.getElementById("videoModal");
        if (modal && event.target === modal) {
            closeModal();
        }
    });
});

// ---------------------------------------------------------------------
// Global Functions (Modal Controls & Video Player)
// ---------------------------------------------------------------------
let bsQuoteModal = null;

function getModalInstance() {
    const modalEl = document.getElementById('quoteModal');
    if (!modalEl) return null;
    if (!bsQuoteModal && typeof bootstrap !== 'undefined') {
        bsQuoteModal = bootstrap.Modal.getOrCreateInstance(modalEl);
    }
    return bsQuoteModal;
}

function openQuoteModal() {
    const modal = getModalInstance();
    if (modal) {
        modal.show();
    } else {
        const modalEl = document.getElementById('quoteModal');
        if (modalEl) modalEl.style.display = 'block';
    }
}

function closeQuoteModal() {
    const modal = getModalInstance();
    if (modal) {
        modal.hide();
    } else {
        const modalEl = document.getElementById('quoteModal');
        if (modalEl) modalEl.style.display = 'none';
    }
    resetForm();
}

function toggleService(element) {
    if (!element) return;
    const checkbox = element.querySelector('input[type="checkbox"]');
    if (checkbox) {
        // Handle event propagation if clicked directly on checkbox vs container
        if (event.target !== checkbox) {
            checkbox.checked = !checkbox.checked;
        }
        element.classList.toggle('selected', checkbox.checked);
        element.classList.toggle('active', checkbox.checked);
    }
}

function selectPriority(element, priority) {
    if (!element) return;
    document.querySelectorAll('.priority-option').forEach(option => {
        option.classList.remove('selected', 'active');
    });
    element.classList.add('selected', 'active');
    const priorityInput = document.getElementById('priority');
    if (priorityInput) priorityInput.value = priority;
}

function resetForm() {
    const form = document.getElementById('quoteForm');
    const successMsg = document.getElementById('successMessage');

    if (form) {
        form.reset();
        form.style.display = 'block';
    }
    if (successMsg) {
        successMsg.style.display = 'none';
    }

    document.querySelectorAll('.service-checkbox, .service-selection .selected, .service-selection .active').forEach(el => {
        el.classList.remove('selected', 'active');
    });
    document.querySelectorAll('.priority-option').forEach(option => {
        option.classList.remove('selected', 'active');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Video Player Functions
const videoMap = {
    'video1': './images/pronto.mp4',
    'video2': './images/docVid.mp4',
    'video3': './images/pronto.mp4'
};

function playVideo(videoId) {
    const modal = document.getElementById("videoModal");
    const videoPlayer = document.getElementById("modalVideoPlayer");
    const videoSrc = videoMap[videoId];
    
    if (modal && videoPlayer && videoSrc) {
        videoPlayer.src = videoSrc;
        modal.style.display = "block";
        videoPlayer.play();
    }
}

function closeModal() {
    const modal = document.getElementById("videoModal");
    const videoPlayer = document.getElementById("modalVideoPlayer");
    if (modal) modal.style.display = "none";
    if (videoPlayer) {
        videoPlayer.pause();
        videoPlayer.src = "";
    }
}