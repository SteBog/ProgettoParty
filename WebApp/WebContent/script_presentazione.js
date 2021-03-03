var controller = new ScrollMagic.Controller()
var altezza = window.innerHeight
var larghezza = window.innerWidth

//  Proporzione altezza
function pa(input)
{
    return (input * altezza) / 1000
}

//  Proporzione larghezza
function pl(input)
{
    return (input * larghezza) / 1170
}

function animazione_caricamento()
{
    gsap.from("#titolo_generale", {y: 150, scale: 0.9, opacity: 0.6, duration: 2})
    gsap.from("#testo_generale", {y: 150, scale: 0.9, opacity: 0.6, duration: 2})
    gsap.from("#img1_generale", {y: 15, duration: 1, repeat: -1, yoyo: true, ease: "sine.inOut"})
    gsap.from("#img2_generale", {y: 15, duration: 1, delay: 0.3, repeat: -1, yoyo: true, ease: "sine.inOut"})
    gsap.from("#img3_generale", {y: 15, duration: 1, delay: 0.6, repeat: -1, yoyo: true, ease: "sine.inOut"})
}

var tlGameplay = new TimelineMax()
.to("#img_player1", {x: pl(60), y: pa(100), duration: 0.5}, 0)
.to("#img_player2", {x: pl(-100), y: pa(60), duration: 0.5}, 0)
.to("#img_player1", {x: pl(10), y: pa(130), duration: 0.5}, 0.5)
.to("#img_player2", {x: pl(0), y: pa(127), duration: 0.5}, 0.5)
.from("#testo_spintoni", {y: 50, opacity: 0, duration: 1}, 1)

var animazione_gameplay = new ScrollMagic.Scene({
    triggerElement: "#section_gameplay_spintoni",
    triggerHook: 0,
    duration: "100%"
})
.setPin("#section_gameplay_spintoni .container")
.setTween(tlGameplay)
//.addIndicators({name: "debug"})
.addTo(controller)

var tlPersonaggio = new TimelineMax()
.to("#section_personaggio", {backgroundColor: "#68E8D1", duration: 1})
.from("#img_avatar", {opacity: 0, duration: 1}, 1)
.to("#section_personaggio", {backgroundColor: "#D7E303", duration: 0.1}, 2)
.to("#img_avatar", {backgroundImage: "url('../../Gioco/Immagini/w_p2/Wraith_02_Moving Forward_000.png')", duration: 0.1}, 2)
.to("#section_personaggio", {backgroundColor: "#e944ec", duration: 0.1}, 3)
.to("#img_avatar", {backgroundImage: "url('../../Gioco/Immagini/w_p3/Wraith_03_Moving Forward_000.png')", duration: 0.1}, 3)

var animazione_personaggio = new ScrollMagic.Scene({
    triggerElement: "#section_personaggio",
    triggerHook: 0,
    duration: "100%"
})
.setPin("#section_personaggio")
.setTween(tlPersonaggio)
.addIndicators({name: "debug"})
.addTo(controller)