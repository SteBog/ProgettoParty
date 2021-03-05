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
    gsap.from("#titolo_generale", {y: 150, scale: 0.9, opacity: 0.6, duration: 1})
    gsap.from("#testo_generale", {y: 150, scale: 0.9, opacity: 0.6, duration: 1})
    gsap.from("#img1_generale", {y: 15, duration: 1, repeat: -1, yoyo: true, ease: "sine.inOut"})
    gsap.from("#img2_generale", {y: 15, duration: 1, delay: 0.3, repeat: -1, yoyo: true, ease: "sine.inOut"})
    gsap.from("#img3_generale", {y: 15, duration: 1, delay: 0.6, repeat: -1, yoyo: true, ease: "sine.inOut"})
    gsap.from("#section_gameplay_spintoni", {y: 150, opacity: 0, duration: 1})
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
.setPin("#section_gameplay_spintoni")
.setTween(tlGameplay)
.addIndicators({name: "gameplay"})
.addTo(controller)

var tlPersonaggio = new TimelineMax()
.from("#img_avatar_1", {opacity: 0, y: 20, duration: 1}, 0)
.from("#scritta_personaggio", {opacity: 0, y: 20, duration: 1}, 0)
.to("#section_personaggio", {backgroundColor: "rgb(68, 230, 203)", duration: 1}, 0)
.to("#img_avatar_1", {display: "none", duration: 0}, 2)
.to("#img_avatar_2", {display: "block", duration: 0}, 2)
.to("#section_personaggio", {backgroundColor: "rgb(242, 131, 53)", duration: 0}, 2)
.to("#img_avatar_2", {display: "none", duration: 0}, 4)
.to("#img_avatar_3", {display: "block", duration: 0}, 4)
.to("#section_personaggio", {backgroundColor: "rgb(143, 81, 167)", duration: 0}, 4)

var animazione_personaggio = new ScrollMagic.Scene({
    triggerElement: "#section_personaggio",
    triggerHook: 0,
    duration: "100%"
})
.setPin("#section_personaggio")
.setTween(tlPersonaggio)
.addIndicators({name: "personaggio"})
.addTo(controller)