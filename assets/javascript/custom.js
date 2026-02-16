/* Custom Site Logic for TJ LaGrow's Portfolio */

document.addEventListener('DOMContentLoaded', function () {

    // -------------------------------------------------------
    // 1. Reveal on Scroll (IntersectionObserver)
    // -------------------------------------------------------
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) e.target.classList.add('show');
        });
    }, { threshold: 0.15 });

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));


    // -------------------------------------------------------
    // 2. Stat Counter Animation
    // -------------------------------------------------------
    const stats = document.querySelectorAll('.stat .num');
    if (stats.length > 0) {
        function countUp(el, to) {
            const dur = 1200,
                start = performance.now(),
                from = 0;

            function tick(t) {
                const p = Math.min((t - start) / dur, 1);
                // Ease out sine
                const ease = 0.5 - Math.cos(Math.PI * p) / 2;
                el.textContent = Math.floor(from + (to - from) * ease).toLocaleString();
                if (p < 1) requestAnimationFrame(tick);
            }
            requestAnimationFrame(tick);
        }

        const statsObs = new IntersectionObserver((entries, obs) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    const to = parseInt(e.target.getAttribute('data-count'), 10);
                    if (!isNaN(to)) {
                        countUp(e.target, to);
                        obs.unobserve(e.target);
                    }
                }
            });
        }, { threshold: 0.6 });

        stats.forEach(s => statsObs.observe(s));
    }


    // -------------------------------------------------------
    // 3. Publication Search & Filters (if present)
    // -------------------------------------------------------
    const pubSearch = document.getElementById('pubSearch');
    if (pubSearch) {
        const items = Array.prototype.slice.call(document.querySelectorAll('.pub-item'));

        pubSearch.addEventListener('input', function () {
            const q = (this.value || '').toLowerCase().trim();
            items.forEach(function (li) {
                const hay = li.getAttribute('data-search').toLowerCase();
                li.style.display = hay.indexOf(q) !== -1 ? '' : 'none';
            });
        });

        // Expand/Collapse controls
        const expandAll = document.getElementById('expandAll');
        const collapseAll = document.getElementById('collapseAll');

        if (expandAll) {
            expandAll.addEventListener('click', () => {
                document.querySelectorAll('#pubList details').forEach(d => d.open = true);
            });
        }
        if (collapseAll) {
            collapseAll.addEventListener('click', () => {
                document.querySelectorAll('#pubList details').forEach(d => d.open = false);
            });
        }
    }


    // -------------------------------------------------------
    // 4. Copy BibTeX Helper
    // -------------------------------------------------------
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.copy-bib');
        if (!btn) return;
        e.preventDefault();
        const bib = btn.getAttribute('data-bib');
        if (navigator.clipboard) {
            navigator.clipboard.writeText(bib).then(function () {
                const originalText = btn.textContent;
                btn.textContent = 'Copied!';
                setTimeout(function () {
                    btn.textContent = originalText;
                }, 1500);
            });
        }
    });

    // -------------------------------------------------------
    // 5. Interactive Carousel: Click to Advance
    // -------------------------------------------------------
    const carousel = document.getElementById('heroCarousel');

    if (carousel) {
        // Robust Click to Advance
        carousel.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            let bsCarousel = bootstrap.Carousel.getInstance(carousel);
            if (!bsCarousel) {
                bsCarousel = new bootstrap.Carousel(carousel);
            }
            bsCarousel.next();
        });

        carousel.style.cursor = 'pointer';
    }

    // -------------------------------------------------------
    // 6. Typing Animation (Homepage Hero)
    // -------------------------------------------------------
    const typeTarget = document.getElementById('auto-type-text');
    if (typeTarget) {
        const textToType = "Building systems that learn, teaching at scale, and exploring the brain.";
        let i = 0;

        function typeWriter() {
            if (i < textToType.length) {
                typeTarget.innerHTML += textToType.charAt(i);
                i++;
                setTimeout(typeWriter, 50); // Speed in ms
            }
        }

        // Start after a short delay
        setTimeout(typeWriter, 800);
    }

    // -------------------------------------------------------
    // 7. Randomize Parallax Background
    // -------------------------------------------------------
    const parallaxBg = document.querySelector('.parallax-bg');
    if (parallaxBg) {
        const images = [
            'ramon_y_cajal.png',
            'ramon_y_cajal_1.jpg',
            'ramon_y_cajal_2.jpg',
            'ramon_y_cajal_3.png'
        ];
        const randomImage = images[Math.floor(Math.random() * images.length)];

        // Deep Teal Theme Color: #042f2e -> rgb(4, 47, 46)
        const gradient = 'linear-gradient(180deg, rgba(4, 47, 46, 0.85) 0%, rgba(4, 47, 46, 0.6) 100%)';
        const url = `url('/assets/images/${randomImage}')`;

        parallaxBg.style.backgroundImage = `${gradient}, ${url}`;
    }

});
