/* ============================================
   MAIN JAVASCRIPT
   Ce Que New York M'a Fait
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initStickyHeader();
    initSmoothScroll();
    initFAQAccordion();
    initScrollAnimations();
    initImageLoading();
    initScrollProgress();
});

/* ============================================
   STICKY HEADER
   ============================================ */

function initStickyHeader() {
    const header = document.getElementById('sticky-header');
    const hero = document.getElementById('hero');

    if (!header || !hero) return;

    const heroHeight = hero.offsetHeight;

    const handleScroll = () => {
        const scrollY = window.scrollY;

        if (scrollY > heroHeight - 100) {
            header.classList.add('visible');
        } else {
            header.classList.remove('visible');
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
}

/* ============================================
   SMOOTH SCROLL
   ============================================ */

function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');

            if (href === '#') return;

            const target = document.querySelector(href);

            if (target) {
                e.preventDefault();

                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* ============================================
   FAQ ACCORDION
   ============================================ */

function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');

        if (!question || !answer) return;

        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Close all other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-question')?.setAttribute('aria-expanded', 'false');
                }
            });

            // Toggle current item
            if (isActive) {
                item.classList.remove('active');
                question.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('active');
                question.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

/* ============================================
   SCROLL ANIMATIONS
   ============================================ */

function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');

                // Optionally unobserve after animation
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe fade-in elements
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-slow, .stagger-children');
    fadeElements.forEach(el => observer.observe(el));

    // Add fade-in class to sections automatically
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const content = section.querySelector('.container, .warning-content, .author-content, .final-cta-content');
        if (content && !content.classList.contains('fade-in')) {
            content.classList.add('fade-in');
            observer.observe(content);
        }
    });

    // Observe pull quotes
    const pullQuotes = document.querySelectorAll('.pull-quote');
    pullQuotes.forEach(quote => {
        if (!quote.classList.contains('fade-in')) {
            quote.classList.add('fade-in');
            observer.observe(quote);
        }
    });

    // Observe chapter items with stagger
    const chaptersGrid = document.querySelector('.chapters-grid');
    if (chaptersGrid) {
        chaptersGrid.classList.add('stagger-children');
        observer.observe(chaptersGrid);
    }

    // Observe testimonial cards
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    testimonialCards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.transitionDelay = `${index * 0.15}s`;
        observer.observe(card);
    });
}

/* ============================================
   IMAGE LOADING
   ============================================ */

function initImageLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');

    images.forEach(img => {
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', () => {
                img.classList.add('loaded');
            });
        }
    });

    // Mark eager images as loaded immediately
    const eagerImages = document.querySelectorAll('img[loading="eager"], img:not([loading])');
    eagerImages.forEach(img => {
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', () => {
                img.classList.add('loaded');
            });
        }
    });
}

/* ============================================
   SCROLL PROGRESS
   ============================================ */

function initScrollProgress() {
    // Create scroll progress element
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    document.body.prepend(progressBar);

    const updateProgress = () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollTop / docHeight;

        progressBar.style.transform = `scaleX(${progress})`;
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
}

/* ============================================
   PURCHASE BUTTON PLACEHOLDER
   ============================================ */

// This will be replaced with actual PayHip integration
document.querySelectorAll('[data-purchase="true"]').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();

        // Placeholder behavior - scroll to show the book is coming soon
        // Replace this with PayHip checkout URL when ready
        alert('Le livre sera bientôt disponible ! Revenez nous voir.');

        // Future implementation:
        // window.location.href = 'https://payhip.com/b/XXXXX';
    });
});

/* ============================================
   PARALLAX EFFECT (Subtle)
   ============================================ */

function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax-slow');

    if (parallaxElements.length === 0) return;

    const handleParallax = () => {
        const scrollY = window.scrollY;

        parallaxElements.forEach(el => {
            const speed = el.dataset.parallaxSpeed || 0.5;
            const yPos = -(scrollY * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
    };

    window.addEventListener('scroll', handleParallax, { passive: true });
}

/* ============================================
   UTILITY: Debounce
   ============================================ */

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/* ============================================
   UTILITY: Throttle
   ============================================ */

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
