
// subtle animations and interactions
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.process-card');

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 200);
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // click interactions
    cards.forEach(card => {
        card.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.service-card');

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // click interactions
    cards.forEach(card => {
        card.addEventListener('click', function () {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Animate stats on scroll
    const statNumbers = document.querySelectorAll('.stat-number');
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const text = target.textContent;
                if (text.includes('+')) {
                    animateNumber(target, 0, parseInt(text), 1000);
                }
            }
        });
    });

    statNumbers.forEach(stat => {
        statsObserver.observe(stat);
    });

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
});



// Add floating animation to contact icons
const contactIcons = document.querySelectorAll('.contact-icon');
contactIcons.forEach((icon, index) => {
    icon.style.animationDelay = `GHC{index * 0.2}s`;
    icon.classList.add('floating-contact-icon');
});



function openQuoteModal() {
            document.getElementById('quoteModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeQuoteModal() {
            document.getElementById('quoteModal').classList.remove('active');
            document.body.style.overflow = 'auto';
            resetForm();
        }

        function closeModal(event) {
            if (event.target === event.currentTarget) {
                closeQuoteModal();
            }
        }

        function toggleService(element) {
            const checkbox = element.querySelector('input[type="checkbox"]');
            checkbox.checked = !checkbox.checked;
            element.classList.toggle('selected', checkbox.checked);
        }

        function selectPriority(element, priority) {
            document.querySelectorAll('.priority-option').forEach(option => {
                option.classList.remove('selected');
            });
            element.classList.add('selected');
            document.getElementById('priority').value = priority;
        }

        function resetForm() {
            document.getElementById('quoteForm').reset();
            document.querySelectorAll('.service-checkbox').forEach(checkbox => {
                checkbox.classList.remove('selected');
            });
            document.querySelectorAll('.priority-option').forEach(option => {
                option.classList.remove('selected');
            });
            document.getElementById('quoteForm').style.display = 'block';
            document.getElementById('successMessage').style.display = 'none';
        }

        // Form submission
        document.getElementById('quoteForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate required services
            const selectedServices = document.querySelectorAll('input[name="services"]:checked');
            if (selectedServices.length === 0) {
                alert('Please select at least one service.');
                return;
            }

            // Simulate form submission
            const formData = new FormData(this);
            
            // Add selected services to form data
            const services = Array.from(selectedServices).map(service => service.value);
            console.log('Form submitted with data:', {
                firstName: formData.get('firstName'),
                lastName: formData.get('lastName'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                company: formData.get('company'),
                industry: formData.get('industry'),
                services: services,
                projectDescription: formData.get('projectDescription'),
                timeline: formData.get('timeline'),
                budget: formData.get('budget'),
                priority: formData.get('priority'),
                additionalInfo: formData.get('additionalInfo')
            });

            // Show success message
            document.getElementById('quoteForm').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';
        });

        // Close modal with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeQuoteModal();
            }
        });