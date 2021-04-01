gsap.registerPlugin(ScrollTrigger);


var tl_presentazione_g1 = gsap.timeline({
    scrollTrigger: {
        markers: false,
        trigger: "#sfondo_nuvole_due",
        start: "top 80%",
        end: "+=1000",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    },
})
.to("#personaggio_uno", {
    y: -500
})
.to("#personaggio_tre", {
    y: -500
})

var tl_presentazione_g1 = gsap.timeline({
    scrollTrigger: {
        markers: false,
        trigger: "#sfondo_nuvole_due",
        start: "top top",
        end: "+=1000",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    },
})
.to("#personaggio_due", {
    y: -500
})
.to("#personaggio_quattro", {
    y: -500
})

var tl_sfondo_presentazione = gsap.to("#section_introduzione", {
    scrollTrigger: {
        markers: false,
        trigger: "#section_introduzione",
        start: "top top",
        end: "+=2160",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    },
    backgroundColor: "#6ad2ff",
})


var tl_presentazione_in_h1 = gsap.timeline({
    scrollTrigger: {
        markers: false,
        trigger: "#sfondo_nuvole_due",
        start: "top center",
        end: "+=3000",
        toggleActions: "restart pauese reverse pause",
        scrub: 0
    }
})
.from("#testo_uno", {
    y: 1000,
}, 0)
.from("#testo_due", {
    opacity: 0,
}, 1)
.to("#testo_uno", {
    y: -500,
}, 2)
.to("#testo_due", {
    opacity: 0,
}, 2)
.to("#section_introduzione", {
    backgroundColor: "white"
}, 3)

var tl_prima_riga = gsap.timeline({
    scrollTrigger: {
        markers: false,
        pin: "#section_minigioco",
        trigger: "#section_minigioco",
        start: "top 50",
        end: "+=2000",
        toggleActions: "restart pause reverse pause",
        scrub: 0,
    }
})
.from(".h_personaggi", {
    opacity: 0,
    y: 150
}, 0)
.from("#prima_riga", {
    x: -1000
}, 0)
.from("#seconda_riga", {
    x: 1000,
    delay: 0
}, 0)

var tl_classifica = gsap.timeline({
    scrollTrigger: {
        markers: true,
        pin: "#classifiche",
        trigger: "#classifiche",
        start: "top top",
        end: "+=2000",
        toggleActions: "restart pause reverse pause",
        scrub: 0
    }
})
.from("#podio_terzo", {
    height: 0
})
.from("#podio_secondo", {
    height: 0
}, 1)
.from("#podio_primo", {
    height: 0
})