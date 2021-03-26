gsap.registerPlugin(ScrollTrigger);

var tl_presentazione_g1 = gsap.to("#personaggio_uno", {
    scrollTrigger: {
        markers: false,
        trigger: "#sfondo_nuvole_due",
        start: "top center",
        end: "bottom top",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    },
    y: -500,
})
