gsap.registerPlugin(ScrollTrigger);

var tl_presentazione_g1 = gsap.to("#personaggio_uno", {
    scrollTrigger: {
        markers: true,
        trigger: "#sfondo_nuvole_due",
        start: "top center",
        end: "bottom top",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    },
    y: -500,
})

var tl_presentazione_g3 = gsap.to("#personaggio_tre", {
    scrollTrigger: {
        markers: true,
        trigger: "#sfondo_nuvole_due",
        start: "20% center",
        end: "bottom top",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    },
    y: -500,
})