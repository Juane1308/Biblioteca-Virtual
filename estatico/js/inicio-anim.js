document.addEventListener("DOMContentLoaded", () => {

    // ============================================================
    // GSAP + ScrollTrigger registrado
    // ============================================================
    gsap.registerPlugin(ScrollTrigger);

    // Config global de GSAP para suavidad
    gsap.defaults({ ease: "power2.out" });


    // ============================================================
    // 1. ANIMACION DE ENTRADA DEL HERO (Timeline GSAP)
    // ============================================================
    const heroTl = gsap.timeline({
        defaults: { ease: "power3.out", duration: 0.8 }
    });

    heroTl
        .from(".hero-badge",         { opacity: 0, y: 25, duration: 0.6 })
        .from(".pl-hero-content h1", { opacity: 0, y: 50, duration: 1, ease: "power4.out" }, "-=0.3")
        .from(".pl-hero-content > p",{ opacity: 0, y: 30, duration: 0.7 }, "-=0.5")
        .from(".hero-search",        { opacity: 0, y: 25, duration: 0.6 }, "-=0.4")
        .from(".hero-actions",       { opacity: 0, y: 25, duration: 0.6 }, "-=0.35")
        .from(".pl-hero-image",      { opacity: 0, x: 80, scale: 0.9, duration: 1.2, ease: "power3.out" }, "-=0.9");


    // ============================================================
    // 2. LIBRO FLOTANTE EN EL HERO (continua)
    // ============================================================
    const heroBook = document.getElementById("heroBook");
    if (heroBook) {
        gsap.to(heroBook, {
            y: -18,
            rotation: 1.5,
            duration: 3.5,
            ease: "sine.inOut",
            yoyo: true,
            repeat: -1
        });
    }


    // ============================================================
    // 3. PARALLAX SUAVE CON GSAP ScrollTrigger (reemplaza vanilla)
    // ============================================================
    const heroContent = document.querySelector('.pl-hero-content');
    const heroImage   = document.querySelector('.pl-hero-image');

    if (heroContent) {
        gsap.to(heroContent, {
            y: 120,
            opacity: 0,
            ease: "none",
            scrollTrigger: {
                trigger: ".pl-hero",
                start: "top top",
                end: "bottom top",
                scrub: 0.8
            }
        });
    }
    if (heroImage) {
        gsap.to(heroImage, {
            y: 60,
            ease: "none",
            scrollTrigger: {
                trigger: ".pl-hero",
                start: "top top",
                end: "bottom top",
                scrub: 0.8
            }
        });
    }


    // ============================================================
    // 4. ESTADISTICAS — Contadores animados con ScrollTrigger
    // ============================================================
    const statNumbers = document.querySelectorAll('.stat-number[data-count]');

    statNumbers.forEach(el => {
        const target = parseInt(el.dataset.count, 10);
        const suffix = '+';

        ScrollTrigger.create({
            trigger: el,
            start: "top 95%",
            once: true,
            onEnter: () => {
                gsap.to({ val: 0 }, {
                    val: target,
                    duration: 2.2,
                    ease: "power2.out",
                    onUpdate: function () {
                        el.textContent = Math.round(this.targets()[0].val).toLocaleString('es-CO') + suffix;
                    }
                });
            }
        });
    });

    // Stats items stagger
    gsap.from(".stat-item", {
        scrollTrigger: {
            trigger: ".pl-stats",
            start: "top 95%",
            once: true
        },
        opacity: 0,
        y: 30,
        duration: 0.7,
        stagger: 0.12,
        ease: "power3.out"
    });


    // ============================================================
    // 5. TEMATICAS — Entrada escalonada suave
    // ============================================================
    gsap.from(".pl-tematica-card", {
        scrollTrigger: {
            trigger: ".pl-tematicas-grid",
            start: "top 95%",
            once: true
        },
        opacity: 0,
        y: 18,
        scale: 0.97,
        duration: 0.3,
        stagger: 0.04,
        ease: "power2.out",
        onComplete: () => {
            document.querySelectorAll('.pl-tematica-card').forEach(c => {
                c.style.opacity  = '';
                c.style.transform = '';
                c.classList.add('card-visible');
            });
        }
    });


    // ============================================================
    // 6. TARJETAS DE LIBROS — Entrada con stagger suave
    // ============================================================
    document.querySelectorAll('.pl-books-grid').forEach(grid => {
        gsap.from(grid.querySelectorAll('.pl-book-card'), {
            scrollTrigger: {
                trigger: grid,
                start: "top 95%",
                once: true
            },
            opacity: 0,
            y: 20,
            scale: 0.98,
            duration: 0.3,
            stagger: 0.05,
            ease: "power2.out",
            onComplete: () => {
                grid.querySelectorAll('.pl-book-card').forEach(c => {
                    c.style.opacity   = '';
                    c.style.transform = '';
                    c.classList.add('card-visible');
                });
            }
        });
    });


    // ============================================================
    // 7. BANNER RECOMENDADO — entrada fluida
    // ============================================================
    const recBanner = document.querySelector(".pl-recomendado-banner");
    if (recBanner) {
        gsap.from(recBanner, {
            scrollTrigger: {
                trigger: recBanner,
                start: "top 95%",
                once: true
            },
            opacity: 0,
            y: 60,
            scale: 0.97,
            duration: 1,
            ease: "power3.out"
        });
    }


    // ============================================================
    // 8. AUTORES DESTACADOS — Entrada escalonada
    // ============================================================
    gsap.from(".pl-autor-card", {
        scrollTrigger: {
            trigger: ".pl-autores-grid",
            start: "top 95%",
            once: true
        },
        opacity: 0,
        y: 20,
        scale: 0.98,
        duration: 0.3,
        stagger: 0.06,
        ease: "power2.out"
    });


    // ============================================================
    // 9. CITA LITERARIA — Entrada cinematica
    // ============================================================
    const citaBanner = document.querySelector(".pl-cita-banner");
    if (citaBanner) {
        const citaTl = gsap.timeline({
            scrollTrigger: {
                trigger: citaBanner,
                start: "top 95%",
                once: true
            }
        });

        citaTl
            .from(citaBanner, { opacity: 0, y: 50, duration: 0.8, ease: "power3.out" })
            .from(".cita-comillas", { opacity: 0, scale: 0.5, duration: 0.5, ease: "back.out(2)" }, "-=0.4")
            .from(".cita-texto", { opacity: 0, y: 20, duration: 0.7, ease: "power2.out" }, "-=0.2")
            .from(".cita-autor", { opacity: 0, x: -20, duration: 0.5, ease: "power2.out" }, "-=0.3");
    }


    // ============================================================
    // 10. TITULOS DE SECCION — fade in suave con scrub parcial
    // ============================================================
    gsap.utils.toArray('.pl-section-title, .pl-section-subtitle, .section-line').forEach(el => {
        gsap.from(el, {
            scrollTrigger: {
                trigger: el,
                start: "top 98%",
                end: "top 80%",
                scrub: 0.5
            },
            opacity: 0,
            y: 25
        });
    });


    // ============================================================
    // 11. TILT 3D EN TARJETAS DE LIBROS (hover suave)
    // ============================================================
    document.querySelectorAll('.pl-book-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect    = card.getBoundingClientRect();
            const x       = e.clientX - rect.left;
            const y       = e.clientY - rect.top;
            const centerX = rect.width  / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / centerY * -4;
            const rotateY = (x - centerX) / centerX * 4;
            gsap.to(card, {
                rotateX,
                rotateY,
                transformPerspective: 1000,
                y: -6,
                duration: 0.4,
                ease: "power2.out"
            });
        });
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                rotateX: 0,
                rotateY: 0,
                y: 0,
                duration: 0.6,
                ease: "elastic.out(1, 0.5)"
            });
        });
    });


    // ============================================================
    // 12. NAVBAR — sombra suave al scroll
    // ============================================================
    const nav = document.querySelector('.dashboard-nav');
    if (nav) {
        ScrollTrigger.create({
            start: "top -10",
            onUpdate: (self) => {
                if (self.progress > 0) {
                    nav.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
                    nav.style.borderBottomColor = 'rgba(56, 189, 248, 0.2)';
                } else {
                    nav.style.boxShadow = 'none';
                    nav.style.borderBottomColor = 'rgba(56, 189, 248, 0.12)';
                }
            }
        });
    }


    // ============================================================
    // 13. SMOOTH SCROLL LINKS
    // ============================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                gsap.to(window, {
                    duration: 1,
                    scrollTo: { y: target, offsetY: 80 },
                    ease: "power3.inOut"
                });
            }
        });
    });

});
