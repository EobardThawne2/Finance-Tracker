/**
 * Finance Tracker - ULTRA JavaScript Animations Pack
 * NO RESTRICTIONS MODE - Maximum animations enabled
 */

// ==================== Animation Configuration ====================
const CONFIG = {
    enableCursorEffects: true,
    enableParticles: true,
    enableMatrixRain: true,
    enableFloatingOrbs: true,
    enableSoundEffects: false, // Set to true if you want sounds
    enableConfetti: true,
    particleCount: 50,
    cursorTrailLength: 20,
    animationIntensity: 1.0 // 0.5 = subtle, 1.0 = normal, 2.0 = intense
};

// ==================== Cursor Effects ====================

// Cursor trail effect
class CursorTrail {
    constructor() {
        this.trails = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.init();
    }

    init() {
        for (let i = 0; i < CONFIG.cursorTrailLength; i++) {
            const trail = document.createElement('div');
            trail.className = 'cursor-trail-dot';
            trail.style.cssText = `
                position: fixed;
                width: ${12 - i * 0.5}px;
                height: ${12 - i * 0.5}px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(94, 106, 210, ${0.8 - i * 0.03}) 0%, transparent 70%);
                pointer-events: none;
                z-index: 10000;
                transition: transform 0.1s ease;
                transform: translate(-50%, -50%);
            `;
            document.body.appendChild(trail);
            this.trails.push({ element: trail, x: 0, y: 0 });
        }

        document.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });

        this.animate();
    }

    animate() {
        let x = this.mouseX;
        let y = this.mouseY;

        this.trails.forEach((trail, index) => {
            trail.x += (x - trail.x) * (0.3 - index * 0.01);
            trail.y += (y - trail.y) * (0.3 - index * 0.01);
            trail.element.style.left = trail.x + 'px';
            trail.element.style.top = trail.y + 'px';
            x = trail.x;
            y = trail.y;
        });

        requestAnimationFrame(() => this.animate());
    }
}

// Magnetic cursor effect
class MagneticCursor {
    constructor() {
        this.cursor = document.createElement('div');
        this.cursorInner = document.createElement('div');
        this.init();
    }

    init() {
        this.cursor.className = 'magnetic-cursor';
        this.cursor.style.cssText = `
            position: fixed;
            width: 40px;
            height: 40px;
            border: 2px solid rgba(94, 106, 210, 0.5);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10001;
            transform: translate(-50%, -50%);
            transition: width 0.3s, height 0.3s, border-color 0.3s;
            mix-blend-mode: difference;
        `;

        this.cursorInner.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: var(--primary);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10002;
            transform: translate(-50%, -50%);
        `;

        document.body.appendChild(this.cursor);
        document.body.appendChild(this.cursorInner);

        let cursorX = 0, cursorY = 0;
        let innerX = 0, innerY = 0;

        document.addEventListener('mousemove', (e) => {
            cursorX = e.clientX;
            cursorY = e.clientY;
        });

        const animate = () => {
            innerX += (cursorX - innerX) * 0.2;
            innerY += (cursorY - innerY) * 0.2;
            
            this.cursor.style.left = innerX + 'px';
            this.cursor.style.top = innerY + 'px';
            this.cursorInner.style.left = cursorX + 'px';
            this.cursorInner.style.top = cursorY + 'px';

            requestAnimationFrame(animate);
        };
        animate();

        // Hover effects
        document.querySelectorAll('a, button, .btn, .card, input, select').forEach(el => {
            el.addEventListener('mouseenter', () => {
                this.cursor.style.width = '60px';
                this.cursor.style.height = '60px';
                this.cursor.style.borderColor = 'rgba(94, 106, 210, 0.8)';
            });
            el.addEventListener('mouseleave', () => {
                this.cursor.style.width = '40px';
                this.cursor.style.height = '40px';
                this.cursor.style.borderColor = 'rgba(94, 106, 210, 0.5)';
            });
        });
    }
}

// ==================== Background Effects ====================

// Matrix rain effect
class MatrixRain {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.init();
    }

    init() {
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.03;
        `;
        document.body.appendChild(this.canvas);

        this.resize();
        window.addEventListener('resize', () => this.resize());

        this.columns = Math.floor(this.canvas.width / 20);
        this.drops = Array(this.columns).fill(1);
        this.chars = '₹$€£¥₿01'.split('');

        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    animate() {
        this.ctx.fillStyle = 'rgba(10, 10, 11, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = '#5E6AD2';
        this.ctx.font = '15px monospace';

        for (let i = 0; i < this.drops.length; i++) {
            const char = this.chars[Math.floor(Math.random() * this.chars.length)];
            this.ctx.fillText(char, i * 20, this.drops[i] * 20);

            if (this.drops[i] * 20 > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
            this.drops[i]++;
        }

        requestAnimationFrame(() => this.animate());
    }
}

// Floating orbs
class FloatingOrbs {
    constructor() {
        this.orbs = [];
        this.init();
    }

    init() {
        for (let i = 0; i < 5; i++) {
            const orb = document.createElement('div');
            orb.className = 'floating-orb';
            orb.style.cssText = `
                position: fixed;
                width: ${200 + Math.random() * 300}px;
                height: ${200 + Math.random() * 300}px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(94, 106, 210, 0.1) 0%, transparent 70%);
                pointer-events: none;
                z-index: -1;
                filter: blur(40px);
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            document.body.appendChild(orb);
            this.orbs.push({
                element: orb,
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5
            });
        }
        this.animate();
    }

    animate() {
        this.orbs.forEach(orb => {
            orb.x += orb.vx;
            orb.y += orb.vy;

            if (orb.x < -200 || orb.x > window.innerWidth + 200) orb.vx *= -1;
            if (orb.y < -200 || orb.y > window.innerHeight + 200) orb.vy *= -1;

            orb.element.style.left = orb.x + 'px';
            orb.element.style.top = orb.y + 'px';
        });

        requestAnimationFrame(() => this.animate());
    }
}

// ==================== Particle Systems ====================

// Explosion particles
class ParticleExplosion {
    static create(x, y, count = 30) {
        const colors = ['#5E6AD2', '#4ADE80', '#60A5FA', '#FBBF24', '#F87171'];
        
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            const size = Math.random() * 10 + 5;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const angle = (Math.PI * 2 * i) / count;
            const velocity = Math.random() * 200 + 100;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;

            particle.style.cssText = `
                position: fixed;
                left: ${x}px;
                top: ${y}px;
                width: ${size}px;
                height: ${size}px;
                background: ${color};
                border-radius: 50%;
                pointer-events: none;
                z-index: 10000;
            `;

            document.body.appendChild(particle);

            let posX = x, posY = y;
            let velocityX = vx, velocityY = vy;
            let opacity = 1;

            const animate = () => {
                velocityY += 5; // gravity
                posX += velocityX * 0.02;
                posY += velocityY * 0.02;
                opacity -= 0.02;

                particle.style.left = posX + 'px';
                particle.style.top = posY + 'px';
                particle.style.opacity = opacity;

                if (opacity > 0) {
                    requestAnimationFrame(animate);
                } else {
                    particle.remove();
                }
            };
            animate();
        }
    }
}

// Confetti
class Confetti {
    static fire(duration = 3000) {
        const colors = ['#5E6AD2', '#4ADE80', '#60A5FA', '#FBBF24', '#F87171', '#EC4899'];
        const end = Date.now() + duration;

        const frame = () => {
            const particle = document.createElement('div');
            const color = colors[Math.floor(Math.random() * colors.length)];
            const size = Math.random() * 10 + 5;
            const x = Math.random() * window.innerWidth;

            particle.style.cssText = `
                position: fixed;
                left: ${x}px;
                top: -20px;
                width: ${size}px;
                height: ${size * 0.4}px;
                background: ${color};
                pointer-events: none;
                z-index: 10000;
                transform: rotate(${Math.random() * 360}deg);
            `;

            document.body.appendChild(particle);

            let y = -20;
            let rotation = Math.random() * 360;
            let rotationSpeed = Math.random() * 10 - 5;
            let swayX = x;
            let swaySpeed = Math.random() * 2 - 1;

            const fall = () => {
                y += 3 + Math.random() * 2;
                rotation += rotationSpeed;
                swayX += Math.sin(y * 0.02) * swaySpeed;

                particle.style.top = y + 'px';
                particle.style.left = swayX + 'px';
                particle.style.transform = `rotate(${rotation}deg)`;

                if (y < window.innerHeight + 20) {
                    requestAnimationFrame(fall);
                } else {
                    particle.remove();
                }
            };
            fall();

            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        };

        frame();
    }
}

// ==================== Interactive Effects ====================

// Ripple on click anywhere
class GlobalRipple {
    constructor() {
        document.addEventListener('click', (e) => {
            this.createRipple(e.clientX, e.clientY);
        });
    }

    createRipple(x, y) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(94, 106, 210, 0.3) 0%, transparent 70%);
            pointer-events: none;
            z-index: 9999;
            transform: translate(-50%, -50%);
        `;

        document.body.appendChild(ripple);

        let size = 0;
        let opacity = 0.5;

        const expand = () => {
            size += 15;
            opacity -= 0.01;

            ripple.style.width = size + 'px';
            ripple.style.height = size + 'px';
            ripple.style.opacity = opacity;

            if (opacity > 0 && size < 500) {
                requestAnimationFrame(expand);
            } else {
                ripple.remove();
            }
        };
        expand();
    }
}

// Text scramble effect
class TextScramble {
    constructor(element) {
        this.element = element;
        this.chars = '!<>-_\\/[]{}—=+*^?#________';
        this.originalText = element.textContent;
    }

    scramble() {
        const length = this.originalText.length;
        let iteration = 0;

        const interval = setInterval(() => {
            this.element.textContent = this.originalText
                .split('')
                .map((char, index) => {
                    if (index < iteration) {
                        return this.originalText[index];
                    }
                    return this.chars[Math.floor(Math.random() * this.chars.length)];
                })
                .join('');

            if (iteration >= length) {
                clearInterval(interval);
            }

            iteration += 1 / 3;
        }, 30);
    }
}

// Tilt 3D effect enhanced
class Tilt3D {
    constructor(elements) {
        elements.forEach(el => {
            el.addEventListener('mousemove', (e) => this.onMouseMove(e, el));
            el.addEventListener('mouseleave', (e) => this.onMouseLeave(e, el));
        });
    }

    onMouseMove(e, el) {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        el.style.transform = `
            perspective(1000px) 
            rotateX(${rotateX}deg) 
            rotateY(${rotateY}deg) 
            scale3d(1.05, 1.05, 1.05)
        `;

        // Add shine effect
        const shine = el.querySelector('.card-shine') || this.createShine(el);
        shine.style.background = `
            radial-gradient(
                circle at ${x}px ${y}px,
                rgba(255, 255, 255, 0.1) 0%,
                transparent 50%
            )
        `;
    }

    onMouseLeave(e, el) {
        el.style.transform = '';
        const shine = el.querySelector('.card-shine');
        if (shine) shine.style.background = 'transparent';
    }

    createShine(el) {
        const shine = document.createElement('div');
        shine.className = 'card-shine';
        shine.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            border-radius: inherit;
        `;
        el.style.position = 'relative';
        el.appendChild(shine);
        return shine;
    }
}

// Magnetic buttons enhanced
class MagneticButtons {
    constructor() {
        document.querySelectorAll('.btn-primary, .btn-large').forEach(btn => {
            btn.addEventListener('mousemove', (e) => this.onMouseMove(e, btn));
            btn.addEventListener('mouseleave', (e) => this.onMouseLeave(e, btn));
            btn.addEventListener('click', (e) => this.onClick(e, btn));
        });
    }

    onMouseMove(e, btn) {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        btn.style.boxShadow = `
            ${-x * 0.1}px ${-y * 0.1}px 20px rgba(94, 106, 210, 0.3),
            0 10px 40px rgba(0, 0, 0, 0.3)
        `;
    }

    onMouseLeave(e, btn) {
        btn.style.transform = '';
        btn.style.boxShadow = '';
    }

    onClick(e, btn) {
        ParticleExplosion.create(e.clientX, e.clientY, 20);
    }
}

// ==================== Scroll Animations ====================

// Parallax sections
class ParallaxScroll {
    constructor() {
        this.elements = document.querySelectorAll('[data-parallax]');
        window.addEventListener('scroll', () => this.onScroll());
    }

    onScroll() {
        const scrolled = window.pageYOffset;

        this.elements.forEach(el => {
            const speed = el.dataset.parallax || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });

        // Parallax background
        document.body.style.backgroundPositionY = scrolled * 0.5 + 'px';
    }
}

// Reveal on scroll
class ScrollReveal {
    constructor() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    this.observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.card, .stat-card, .chart-container, .expense-item, .feature-card').forEach(el => {
            el.classList.add('reveal-on-scroll');
            this.observer.observe(el);
        });
    }
}

// ==================== Number Animations ====================

// Animated counter with easing
class AnimatedCounter {
    constructor() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateValue(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.stat-value, .prediction-value').forEach(el => {
            observer.observe(el);
        });
    }

    animateValue(element) {
        const text = element.textContent;
        const matches = text.match(/[\d,]+/);
        if (!matches) return;

        const target = parseInt(matches[0].replace(/,/g, ''));
        const prefix = text.substring(0, text.indexOf(matches[0]));
        const suffix = text.substring(text.indexOf(matches[0]) + matches[0].length);

        let start = 0;
        const duration = 2000;
        const startTime = performance.now();

        const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutExpo(progress);
            const current = Math.floor(easedProgress * target);

            element.textContent = prefix + current.toLocaleString('en-IN') + suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        };

        requestAnimationFrame(update);
    }
}

// ==================== Form Animations ====================

// Floating labels
class FloatingLabels {
    constructor() {
        document.querySelectorAll('.form-group input, .form-group select, .form-group textarea').forEach(input => {
            input.addEventListener('focus', () => this.onFocus(input));
            input.addEventListener('blur', () => this.onBlur(input));
            
            // Initial check
            if (input.value) {
                input.parentElement.classList.add('has-value');
            }
        });
    }

    onFocus(input) {
        input.parentElement.classList.add('focused');
    }

    onBlur(input) {
        input.parentElement.classList.remove('focused');
        if (input.value) {
            input.parentElement.classList.add('has-value');
        } else {
            input.parentElement.classList.remove('has-value');
        }
    }
}

// Input validation shake
class ValidationShake {
    static shake(element) {
        element.classList.add('shake');
        setTimeout(() => element.classList.remove('shake'), 500);
    }
}

// ==================== Page Transitions ====================

class PageTransitions {
    constructor() {
        // Fade in on load
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease';
        
        window.addEventListener('load', () => {
            document.body.style.opacity = '1';
        });

        // Fade out on navigation
        document.querySelectorAll('a[href]').forEach(link => {
            if (link.hostname === window.location.hostname && !link.hasAttribute('data-no-transition')) {
                link.addEventListener('click', (e) => {
                    if (!e.ctrlKey && !e.metaKey) {
                        e.preventDefault();
                        document.body.style.opacity = '0';
                        setTimeout(() => {
                            window.location = link.href;
                        }, 300);
                    }
                });
            }
        });
    }
}

// ==================== Sound Effects (Optional) ====================

class SoundEffects {
    constructor() {
        this.sounds = {};
        if (!CONFIG.enableSoundEffects) return;
        
        // Create audio context on user interaction
        document.addEventListener('click', () => this.init(), { once: true });
    }

    init() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }

    play(type) {
        if (!this.ctx) return;
        
        const oscillator = this.ctx.createOscillator();
        const gainNode = this.ctx.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.ctx.destination);
        
        switch(type) {
            case 'click':
                oscillator.frequency.value = 800;
                gainNode.gain.value = 0.1;
                break;
            case 'hover':
                oscillator.frequency.value = 600;
                gainNode.gain.value = 0.05;
                break;
            case 'success':
                oscillator.frequency.value = 1000;
                gainNode.gain.value = 0.1;
                break;
        }
        
        oscillator.start();
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);
        oscillator.stop(this.ctx.currentTime + 0.1);
    }
}

// ==================== Easter Eggs ====================

class EasterEggs {
    constructor() {
        // Konami Code: ↑ ↑ ↓ ↓ ← → ← → B A
        this.konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
        this.konamiIndex = 0;
        
        document.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            const expectedKey = this.konamiCode[this.konamiIndex].toLowerCase();
            
            if (key === expectedKey) {
                this.konamiIndex++;
                console.log(`🎮 Konami progress: ${this.konamiIndex}/${this.konamiCode.length}`);
                
                if (this.konamiIndex === this.konamiCode.length) {
                    console.log('🎉 KONAMI CODE ACTIVATED!');
                    this.activateKonami();
                    this.konamiIndex = 0;
                }
            } else {
                if (this.konamiIndex > 0) {
                    console.log('🎮 Konami reset');
                }
                this.konamiIndex = 0;
            }
        });
        
        console.log('🎮 Konami Code listener ready! Press: ↑↑↓↓←→←→BA');
    }

    activateKonami() {
        // Fire confetti
        Confetti.fire(5000);
        
        // Rainbow body animation
        document.body.style.animation = 'colorCycle 2s linear infinite';
        
        // Add screen shake
        document.body.style.transform = 'translateX(5px)';
        setTimeout(() => document.body.style.transform = 'translateX(-5px)', 50);
        setTimeout(() => document.body.style.transform = 'translateX(5px)', 100);
        setTimeout(() => document.body.style.transform = 'translateX(-5px)', 150);
        setTimeout(() => document.body.style.transform = '', 200);
        
        // Show celebration message
        const celebration = document.createElement('div');
        celebration.innerHTML = '🎉 KONAMI CODE ACTIVATED! 🎉';
        celebration.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 32px;
            font-weight: bold;
            color: white;
            text-shadow: 0 0 20px var(--primary), 0 0 40px var(--primary);
            z-index: 99999;
            animation: zoomInBounce 0.5s ease-out;
            pointer-events: none;
        `;
        document.body.appendChild(celebration);
        
        setTimeout(() => {
            celebration.style.opacity = '0';
            celebration.style.transition = 'opacity 0.5s';
            setTimeout(() => celebration.remove(), 500);
        }, 3000);
        
        setTimeout(() => {
            document.body.style.animation = '';
        }, 5000);
    }
}

// ==================== Original Functions ====================

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Confirm before delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Format currency
function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format number
function formatNumber(num) {
    return new Intl.NumberFormat('en-IN').format(num);
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Toggle mobile menu
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Form validation helper
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');
            ValidationShake.shake(field);
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

// Currency conversion preview
async function previewConversion(amount, fromCurrency, targetElement) {
    if (!amount || fromCurrency === 'INR') {
        targetElement.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/convert?amount=${amount}&from=${fromCurrency}&to=INR`);
        const data = await response.json();
        
        if (data.success) {
            targetElement.textContent = formatCurrency(data.converted, 'INR');
            targetElement.style.display = 'block';
        }
    } catch (error) {
        console.error('Conversion error:', error);
    }
}

// Debounce function
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

// Print functionality
function printPage() {
    window.print();
}

// Export data
function exportData(format) {
    alert(`Export to ${format} - Feature coming soon!`);
}

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            tooltip.style.left = rect.left + (rect.width - tooltip.offsetWidth) / 2 + 'px';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(t => t.remove());
        });
    });
}

// ==================== Initialize Everything ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Finance Tracker ULTRA Animations initializing...');

    // Core effects
    initTooltips();
    new ScrollReveal();
    new AnimatedCounter();
    new FloatingLabels();
    new PageTransitions();
    new EasterEggs();

    // Cursor effects (disabled - can be intensive)
    // if (CONFIG.enableCursorEffects) {
    //     new CursorTrail();
    //     new MagneticCursor();
    // }

    // Background effects
    if (CONFIG.enableMatrixRain) {
        new MatrixRain();
    }
    if (CONFIG.enableFloatingOrbs) {
        new FloatingOrbs();
    }

    // Interactive effects
    new GlobalRipple();
    new MagneticButtons();
    new Tilt3D(document.querySelectorAll('.card, .stat-card, .feature-card'));

    // Text effects on headings
    document.querySelectorAll('.hero-content h1, .page-header h1').forEach(el => {
        const scrambler = new TextScramble(el);
        el.addEventListener('mouseenter', () => scrambler.scramble());
    });

    // Sound effects
    if (CONFIG.enableSoundEffects) {
        const sounds = new SoundEffects();
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', () => sounds.play('click'));
            btn.addEventListener('mouseenter', () => sounds.play('hover'));
        });
    }

    // Success confetti on form submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (e) => {
            if (CONFIG.enableConfetti && validateForm(form)) {
                Confetti.fire(1000);
            }
        });
    });

    // Add reveal class styles
    const style = document.createElement('style');
    style.textContent = `
        .reveal-on-scroll {
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .reveal-on-scroll.revealed {
            opacity: 1;
            transform: translateY(0);
        }
        .shake {
            animation: shake 0.5s ease-in-out;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);

    console.log('✨ Finance Tracker ULTRA Animations loaded!');
    console.log('🎮 Try the Konami code for a surprise! ↑↑↓↓←→←→BA');
});
