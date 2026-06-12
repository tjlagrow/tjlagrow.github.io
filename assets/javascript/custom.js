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
    // -------------------------------------------------------
    // 7. Randomize Parallax Background (Body Root)
    // -------------------------------------------------------
    const images = [
        'ramon_y_cajal.png',
        'ramon_y_cajal_1.jpg',
        'ramon_y_cajal_2.jpg',
        'ramon_y_cajal_3.png'
    ];
    // Random selection
    const randomImage = images[Math.floor(Math.random() * images.length)];

    // Deep Teal Theme Color: #042f2e -> rgb(4, 47, 46) 
    // We apply this directly to the body to ensure correct stacking context
    const gradient = 'linear-gradient(180deg, rgba(4, 47, 46, 0.85) 0%, rgba(4, 47, 46, 0.6) 100%)';
    const url = `url('/assets/images/${randomImage}')`;

    // Apply to body
    document.body.style.backgroundImage = `${gradient}, ${url}`;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center';
    document.body.style.backgroundRepeat = 'no-repeat';
    document.body.style.backgroundAttachment = 'fixed';

    // -------------------------------------------------------
    // 8. Pizza Canvas Physics Engine & Trail (Same as README.html)
    // -------------------------------------------------------
    const canvas = document.getElementById('pizza-canvas');
    const pizzaNavItem = document.getElementById('pizza-nav-item');
    const pizzaToggleBtn = document.getElementById('pizza-toggle-btn');
    const pizzaStatusDot = document.getElementById('pizza-status-dot');
    
    let ctx = null;
    if (canvas) {
        ctx = canvas.getContext('2d');
    }

    function isPCWithMouse() {
        const isMobileOrTabletUA = /Mobi|Android|iPhone|iPad|iPod|Windows Phone|webOS/i.test(navigator.userAgent);
        const hasFinePointer = window.matchMedia('(pointer: fine)').matches;
        return hasFinePointer && !isMobileOrTabletUA;
    }

    let particles = [];
    let lastMouseX = 0;
    let lastMouseY = 0;
    let lastSpawnTime = 0;
    let physicsEngineActive = false;
    let pizzaTrailEnabled = false;

    function resizeCanvas() {
        if (canvas) {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
    }

    function spawnPizza(startX, startY, isRain = false) {
        // Randomly select pizza/topping elements
        const items = ['🍕', '🍕', '🍅', '🍄', '🧀', '🇮🇹'];
        const text = items[Math.floor(Math.random() * items.length)];
        
        particles.push({
            text: text,
            x: startX,
            y: startY,
            vx: isRain ? (Math.random() - 0.5) * 5 : (Math.random() - 0.5) * 2.5,
            vy: isRain ? (1 + Math.random() * 3) : (-1.2 - Math.random() * 1.5), // float up if trail, fall if rain
            state: isRain ? 'fall' : 'hover',
            life: 0,
            // Hover duration before crumbling (40 to 80 frames)
            hoverDuration: isRain ? 0 : (40 + Math.random() * 40),
            rotation: Math.random() * Math.PI * 2,
            rotSpeed: (Math.random() - 0.5) * 0.1,
            size: isRain ? (14 + Math.random() * 12) : 22,
            puddleDuration: 120 + Math.random() * 80
        });
    }

    function triggerPizzaRainstorm() {
        const screenWidth = window.innerWidth;
        for (let i = 0; i < 40; i++) {
            setTimeout(() => {
                const randomX = Math.random() * screenWidth;
                spawnPizza(randomX, -20, true);
                if (!physicsEngineActive) {
                    physicsEngineActive = true;
                    frameUpdate();
                }
            }, i * 80);
        }
    }

    function frameUpdate() {
        if (!ctx || (!pizzaTrailEnabled && particles.length === 0)) {
            if (ctx && canvas) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
            physicsEngineActive = false;
            return;
        }
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const screenHeight = canvas.height;
        
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.life++;
            
            if (p.state === 'hover') {
                p.x += p.vx * 0.4;
                p.y += p.vy * 0.4;
                p.vx *= 0.95;
                p.vy *= 0.95;
                
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rotation);
                ctx.font = `${p.size}px serif`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(p.text, 0, 0);
                ctx.restore();
                
                if (p.life > p.hoverDuration) {
                    p.state = 'fall';
                    p.vx = (Math.random() - 0.5) * 4;
                    p.vy = 1 + Math.random() * 2;
                }
            } 
            else if (p.state === 'fall') {
                p.vy += 0.22;
                p.x += p.vx;
                p.y += p.vy;
                p.rotation += p.rotSpeed;
                
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rotation);
                ctx.font = `${p.size}px serif`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(p.text, 0, 0);
                ctx.restore();
                
                if (p.y >= screenHeight - 16) {
                    p.state = 'puddle';
                    p.y = screenHeight - 8;
                    p.life = 0;
                }
            } 
            else if (p.state === 'puddle') {
                const progress = p.life / p.puddleDuration;
                const scale = Math.max(0, 1 - progress);
                const opacity = Math.max(0, 1 - progress);
                
                ctx.save();
                ctx.globalAlpha = opacity;
                ctx.fillStyle = '#b91c1c'; // Tomato red
                
                ctx.beginPath();
                const radiusX = 12 * scale;
                const radiusY = 4 * scale;
                ctx.ellipse(p.x, p.y, radiusX, radiusY, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
                
                if (p.life >= p.puddleDuration) {
                    particles.splice(i, 1);
                }
            }
        }
        
        requestAnimationFrame(frameUpdate);
    }

    function handleMouseMove(e) {
        if (!pizzaTrailEnabled) return;
        const now = Date.now();
        const dist = Math.hypot(e.clientX - lastMouseX, e.clientY - lastMouseY);
        if (now - lastSpawnTime > 35 && dist > 15) {
            spawnPizza(e.clientX, e.clientY, false);
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            lastSpawnTime = now;
            
            if (!physicsEngineActive) {
                physicsEngineActive = true;
                frameUpdate();
            }
        }
    }

    function enablePizzaTrail() {
        pizzaTrailEnabled = true;
        localStorage.setItem('pizza-trail-enabled', 'true');
        if (pizzaStatusDot) {
            pizzaStatusDot.style.backgroundColor = '#2dd4bf';
            pizzaStatusDot.style.boxShadow = '0 0 8px #2dd4bf';
        }
        if (pizzaToggleBtn) {
            pizzaToggleBtn.style.borderColor = 'rgba(45, 212, 191, 0.4)';
            pizzaToggleBtn.style.color = '#2dd4bf';
            pizzaToggleBtn.style.background = 'rgba(45, 212, 191, 0.05)';
        }
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        window.addEventListener('mousemove', handleMouseMove);
        
        if (!physicsEngineActive) {
            physicsEngineActive = true;
            frameUpdate();
        }
    }

    function disablePizzaTrail() {
        pizzaTrailEnabled = false;
        localStorage.setItem('pizza-trail-enabled', 'false');
        if (pizzaStatusDot) {
            pizzaStatusDot.style.backgroundColor = '#64748b';
            pizzaStatusDot.style.boxShadow = 'none';
        }
        if (pizzaToggleBtn) {
            pizzaToggleBtn.style.borderColor = 'rgba(255, 255, 255, 0.15)';
            pizzaToggleBtn.style.color = 'rgba(255, 255, 255, 0.8)';
            pizzaToggleBtn.style.background = 'rgba(255, 255, 255, 0.03)';
        }
        
        window.removeEventListener('resize', resizeCanvas);
        window.removeEventListener('mousemove', handleMouseMove);
    }

    if (pizzaNavItem && pizzaToggleBtn) {
        if (isPCWithMouse()) {
            pizzaNavItem.style.setProperty('display', 'flex', 'important');
            
            const savedPref = localStorage.getItem('pizza-trail-enabled');
            if (savedPref === 'true') {
                enablePizzaTrail();
            }
            
            pizzaToggleBtn.addEventListener('click', function () {
                if (pizzaTrailEnabled) {
                    disablePizzaTrail();
                } else {
                    enablePizzaTrail();
                }
            });
        }
    }

    // Wire up clicking the celebration element in the footer to start a rainstorm
    const celebrationEl = document.querySelector('.celebration');
    if (celebrationEl) {
        celebrationEl.style.cursor = 'pointer';
        celebrationEl.title = 'Click for a pizza rainstorm!';
        celebrationEl.addEventListener('click', function() {
            triggerPizzaRainstorm();
        });
    }

});
