var timeline_login
var timeline_registrazione

function prossimo_div_login()
{
    timeline_login = gsap.timeline()
    .fromTo("#div_login", {x: 0, opacity: 1, display: "flex"}, {x: -100, opacity: 0, display: "none", duration: 1})
    .fromTo("#div_registrazione_first", {x: 100, opacity: 0, display: "none"}, {x: 0, opacity: 1, display: "flex", duration: 1})
}
function precedente_div_login()
{
    timeline_login.reverse()
}

function prossimo_div_registrazione()
{
    timeline_registrazione = gsap.timeline()
    .fromTo("#div_registrazione_first", {x: 0, opacity: 1, display: "flex"}, {x: -100, opacity: 0, display: "none", duration: 1})
    .fromTo("#div_registrazione_second", {x: 100, opacity: 0, display: "none"}, {x: 0, opacity: 1, display: "flex", duration: 1})
}
function precedente_div_registrazione()
{
    timeline_registrazione.reverse()
}