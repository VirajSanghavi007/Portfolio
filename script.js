// n8n skill tag expand/collapse
function toggleN8nProjects() {
    document.getElementById('n8nProjects').classList.toggle('open');
    document.getElementById('n8nTag').classList.toggle('active');
}

// Python skill tag expand/collapse
function togglePythonProjects() {
    document.getElementById('pythonProjects').classList.toggle('open');
    document.getElementById('pythonTag').classList.toggle('active');
}

// Internship projects expand/collapse
function toggleInternshipProjects() {
    const panel = document.getElementById('internPanel');
    const isOpen = panel.style.maxHeight && panel.style.maxHeight !== '0px';
    panel.style.maxHeight = isOpen ? '0px' : panel.scrollHeight + 'px';
    const btn = document.querySelector('[onclick="toggleInternshipProjects()"]');
    const arrow = btn.querySelector('.internship-arrow');
    if (arrow) arrow.style.transform = isOpen ? '' : 'rotate(180deg)';
}

// Video fallback: show emoji icon if demo video fails to load
document.querySelectorAll('.project-demo').forEach(v => {
    v.addEventListener('error', () => { v.style.display = 'none'; }, true);
});

// Theme toggle
const themeToggle = document.getElementById('themeToggle');
if (localStorage.getItem('theme') === 'light') document.documentElement.dataset.theme = 'light';
themeToggle.addEventListener('click', () => {
    const isLight = document.documentElement.dataset.theme === 'light';
    if (isLight) { delete document.documentElement.dataset.theme; localStorage.removeItem('theme'); }
    else { document.documentElement.dataset.theme = 'light'; localStorage.setItem('theme', 'light'); }
});

// Hamburger menu
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');
const menuOverlay = document.getElementById('menuOverlay');
function closeMenu() { hamburger.classList.remove('open'); navLinks.classList.remove('open'); menuOverlay.classList.remove('open'); }
hamburger.addEventListener('click', () => {
    const open = hamburger.classList.toggle('open');
    navLinks.classList.toggle('open', open);
    menuOverlay.classList.toggle('open', open);
});
menuOverlay.addEventListener('click', closeMenu);
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));

// Navbar: add frosted-glass blur when page is scrolled
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
}, { passive: true });

// Scroll-triggered fade-in using IntersectionObserver
const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

document.querySelectorAll('.fade-in').forEach(el => io.observe(el));

// Typing animation for the hero tagline
const phrases = [
    'ML / AI Engineer',
    'Building in Finance, Logistics, Speech',
    'Third Year CE at DJ Sanghavi',
    'Deep Learning Practitioner',
];
let pi = 0, ci = 0, deleting = false;
const typedEl = document.getElementById('typed-text');

(function type() {
    const phrase = phrases[pi];
    typedEl.textContent = deleting ? phrase.slice(0, --ci) : phrase.slice(0, ++ci);

    if (!deleting && ci === phrase.length) {
        setTimeout(() => { deleting = true; type(); }, 2200);
        return;
    }
    if (deleting && ci === 0) {
        deleting = false;
        pi = (pi + 1) % phrases.length;
    }
    setTimeout(type, deleting ? 38 : 72);
})();

// Hero parallax on mouse move
const hero = document.querySelector('.hero');
const orb1 = document.querySelector('.hero-orb-1');
const orb2 = document.querySelector('.hero-orb-2');
const dots = document.querySelector('.hero-dots');

if (hero && orb1 && orb2 && dots) {
    hero.addEventListener('mousemove', (e) => {
        if (window.innerWidth < 600) return;
        const rect = hero.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width * 2 - 1;
        const y = (e.clientY - rect.top) / rect.height * 2 - 1;
        orb1.style.transform = `translate(${x * 20}px, ${y * 20}px)`;
        orb2.style.transform = `translate(${x * -15}px, ${y * -15}px)`;
        dots.style.transform = `translate(${x * 8}px, ${y * 8}px)`;
    });
    hero.addEventListener('mouseleave', () => {
        orb1.style.transform = '';
        orb2.style.transform = '';
        dots.style.transform = '';
    });
}

// Animated stat counters
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        counterObserver.unobserve(el);
        const target = parseInt(el.dataset.target, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 1500;
        const start = performance.now();
        (function tick(now) {
            const t = Math.min((now - start) / duration, 1);
            const ease = 1 - Math.pow(1 - t, 3);
            el.textContent = Math.round(ease * target) + suffix;
            if (t < 1) requestAnimationFrame(tick);
        })(start);
    });
}, { threshold: 0.3 });

document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

// Project writeup expand / collapse
function toggleWriteup(btn) {
    const card    = btn.closest('.project-card');
    const writeup = card.querySelector('.project-writeup');
    const isOpen  = writeup.classList.contains('open');

    document.querySelectorAll('.project-writeup.open').forEach(w => w.classList.remove('open'));
    document.querySelectorAll('.writeup-toggle.open').forEach(b => b.classList.remove('open'));

    if (!isOpen) {
        writeup.classList.add('open');
        btn.classList.add('open');
        setTimeout(() => writeup.scrollIntoView({ behavior:'smooth', block:'nearest' }), 50);
    }
}
