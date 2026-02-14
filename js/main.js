/* ============================================
   MAIN JAVASCRIPT
   Ce Que New York M'a Fait
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initCookieConsent();
    initStickyHeader();
    initSmoothScroll();
    initFAQAccordion();
    initScrollAnimations();
    initImageLoading();
    initScrollProgress();
    initScrollDepthTracking();
    initMobileFloatingCTA();
    initExitIntent();
});

/* ============================================
   COOKIE CONSENT (GDPR)
   ============================================ */

function initCookieConsent() {
    if (localStorage.getItem('cookie-consent')) return;

    var banner = document.createElement('div');
    banner.className = 'cookie-consent';

    var text = document.createElement('p');
    text.textContent = 'Ce site utilise Google Analytics pour comprendre comment les visiteurs interagissent avec le contenu. ';
    var link = document.createElement('a');
    link.href = '/mentions-legales/';
    link.textContent = 'En savoir plus';
    text.appendChild(link);

    var buttons = document.createElement('div');
    buttons.className = 'cookie-consent-buttons';
    var acceptBtn = document.createElement('button');
    acceptBtn.className = 'cookie-btn-accept';
    acceptBtn.textContent = 'Accepter';
    var declineBtn = document.createElement('button');
    declineBtn.className = 'cookie-btn-decline';
    declineBtn.textContent = 'Refuser';
    buttons.appendChild(acceptBtn);
    buttons.appendChild(declineBtn);

    banner.appendChild(text);
    banner.appendChild(buttons);
    document.body.appendChild(banner);

    requestAnimationFrame(function() {
        requestAnimationFrame(function() { banner.classList.add('visible'); });
    });

    acceptBtn.addEventListener('click', function() {
        localStorage.setItem('cookie-consent', 'accepted');
        if (typeof gtag !== 'undefined') {
            gtag('consent', 'update', {'analytics_storage': 'granted'});
        }
        banner.classList.remove('visible');
        setTimeout(function() { banner.remove(); }, 400);
    });

    declineBtn.addEventListener('click', function() {
        localStorage.setItem('cookie-consent', 'declined');
        banner.classList.remove('visible');
        setTimeout(function() { banner.remove(); }, 400);
    });
}

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
   SCROLL DEPTH TRACKING (Google Analytics)
   ============================================ */

function initScrollDepthTracking() {
    if (typeof gtag === 'undefined') return;
    if (!document.body.classList.contains('book-page')) return;

    const sections = ['excerpt', 'chapters', 'testimonials', 'purchase', 'email-capture'];
    const tracked = new Set();

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !tracked.has(entry.target.id)) {
                tracked.add(entry.target.id);
                gtag('event', 'scroll_depth', {section: entry.target.id});
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) observer.observe(el);
    });
}

/* ============================================
   MOBILE FLOATING CTA
   ============================================ */

function initMobileFloatingCTA() {
    const cta = document.getElementById('mobile-cta');
    const hero = document.getElementById('hero');
    const purchase = document.getElementById('purchase');

    if (!cta || !hero) return;

    const handleScroll = () => {
        const heroBottom = hero.getBoundingClientRect().bottom;
        const purchaseVisible = purchase && purchase.getBoundingClientRect().top < window.innerHeight;

        if (heroBottom < 0 && !purchaseVisible) {
            cta.classList.add('visible');
        } else {
            cta.classList.remove('visible');
        }
    };

    window.addEventListener('scroll', throttle(handleScroll, 100), { passive: true });
}

/* ============================================
   EXIT-INTENT EMAIL CAPTURE
   ============================================ */

function initExitIntent() {
    if (!document.body.classList.contains('book-page')) return;
    if (sessionStorage.getItem('exit-intent-shown')) return;

    const overlay = document.getElementById('exit-intent-overlay');
    if (!overlay) return;

    const showOverlay = () => {
        overlay.classList.add('visible');
        sessionStorage.setItem('exit-intent-shown', '1');
        if (typeof gtag !== 'undefined') {
            gtag('event', 'exit_intent_shown');
        }
    };

    // Desktop: mouse leaves viewport toward top
    document.documentElement.addEventListener('mouseleave', (e) => {
        if (e.clientY <= 0 && !sessionStorage.getItem('exit-intent-shown')) {
            showOverlay();
        }
    });

    // Close handlers
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay || e.target.closest('.exit-intent-close')) {
            overlay.classList.remove('visible');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') overlay.classList.remove('visible');
    });
}

/* ============================================
   EMAIL FORM HANDLING (Brevo API)
   ============================================ */

const BREVO = {
    apiKey: '1MLSON61JkeOwKnE-7e915b00311bc13fcf98599a17c484b041ccbf81f5e8b0e950295a5c52034266-bisyekx'.split('').reverse().join(''),
    listNewsletter: 4,
    listChapter: 5,
    templateChapter: 1,
    templateNewsletter: 2
};

async function brevoCreateContact(email, listIds, source) {
    const res = await fetch('https://api.brevo.com/v3/contacts', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'content-type': 'application/json',
            'api-key': BREVO.apiKey
        },
        body: JSON.stringify({
            email: email,
            listIds: listIds,
            attributes: { SOURCE: source },
            updateEnabled: true
        })
    });
    return res;
}

async function brevoSendTemplate(templateId, toEmail) {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'content-type': 'application/json',
            'api-key': BREVO.apiKey
        },
        body: JSON.stringify({
            templateId: templateId,
            to: [{ email: toEmail }]
        })
    });
    return res;
}

function initEmailForms() {
    document.querySelectorAll('form[id]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = form.querySelector('input[type="email"]').value;
            const successEl = form.querySelector('.form-success');
            const errorEl = form.querySelector('.form-error');
            const submitBtn = form.querySelector('button[type="submit"]');

            if (!email) return;

            const isChapter = form.id === 'free-chapter-form' || form.closest('.exit-intent-modal');

            // Track with Google Analytics
            if (typeof gtag !== 'undefined') {
                const type = isChapter ? 'free-chapter' : 'newsletter';
                gtag('event', 'email_signup', {type: type, page: window.location.pathname});
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Envoi...';

            try {
                const listIds = isChapter
                    ? [BREVO.listChapter]
                    : [BREVO.listNewsletter];
                const source = isChapter
                    ? 'free-chapter-' + window.location.pathname
                    : 'newsletter-' + window.location.pathname;

                await brevoCreateContact(email, listIds, source);

                const templateId = isChapter
                    ? BREVO.templateChapter
                    : BREVO.templateNewsletter;
                await brevoSendTemplate(templateId, email);

                if (successEl) successEl.style.display = 'block';
                if (errorEl) errorEl.style.display = 'none';
                submitBtn.textContent = 'Envoyé !';
                form.querySelector('input[type="email"]').value = '';
            } catch (err) {
                if (errorEl) errorEl.style.display = 'block';
                if (successEl) successEl.style.display = 'none';
                submitBtn.textContent = isChapter ? 'Recevoir l\'extrait' : 'S\'inscrire';
                submitBtn.disabled = false;
            }
        });
    });
}

// Init email forms after DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmailForms);
} else {
    initEmailForms();
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
