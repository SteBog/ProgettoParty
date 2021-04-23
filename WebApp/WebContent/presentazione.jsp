<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="stili_home.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.6.0/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.6.0/ScrollTrigger.min.js"></script>
    
	<!--font-->
	<link rel="preconnect" href="https://fonts.gstatic.com">
	<link href="https://fonts.googleapis.com/css2?family=RocknRoll+One&display=swap" rel="stylesheet">
    <title>Progetto Party</title>
</head>
<!--
    1)  Sfida i tuoi amici in fantastiche sfide
    2)  Sblocca fantastici personaggi e mostrali a tutti
    3)  Competi, vinci e scala le classifiche
-->
<body>
    <nav>
        <a href="presentazione.jsp" class="TitoloNav">Progetto Party</a>
        <div class="div-nav">
            <a href="Amici.jsp" class="TestoNav">I tuoi amici</a>
            <a href="profilo.jsp" class="profilo"><%=request.getSession().getAttribute("Utente").toString() %></a>
        </div>
    </nav>
    <section id="section_introduzione">
        <img src="img/1.png" alt="" id="personaggio_uno">
        <h1 id="testo_uno">Ti presentiamo</h1>
        <h2 id="testo_due">Progetto Party</h2>
        <img src="img/2.png" alt="" id="personaggio_due">
        <img src="img/3.png" alt="" id="personaggio_tre">
        <img src="img/4.png" alt="" id="personaggio_quattro">
        <img src="img/Nuvole.png" alt="" id="sfondo_nuvole_uno">
        <img src="img/Nuvole.png" alt="" id="sfondo_nuvole_due" style="top: -10px;">
    </section>
    <section id="section_minigioco">
        <div class="riga_personaggi" id="prima_riga">
            <img src="img/1.png" alt="">
            <img src="img/2.png" alt="">
            <img src="img/3.png" alt="">
            <img src="img/4.png" alt="">
            <img src="img/5.png" alt="">
        </div>
        <div class="riga_personaggi" id="seconda_riga">
            <img src="img/1.png" alt="">
            <img src="img/2.png" alt="">
            <img src="img/3.png" alt="">
            <img src="img/4.png" alt="">
            <img src="img/5.png" alt="">
        </div>
        <h1 class="h_personaggi">Scegli tra diversi personaggi unici e fantastici</h1>
    </section>
    <section id="classifiche">
        <div id="terzo_classificato" class="div_classificato">
            <img src="img/2.png" alt="">
            <div id="podio_terzo"></div>
        </div>
        <div id="secondo_classificato" class="div_classificato">
            <img src="img/4.png" alt="">
            <div id="podio_secondo"></div>
        </div>
        <div id="primo_classificato" class="div_classificato">
            <img src="img/1.png" alt="">
            <div id="podio_primo"></div>
        </div>
        <span class="banner">Competi con i tuoi avversari e diventa il numero 1</span>
    </section>
    
</body>
<script src="script_presentazione.js"></script>
</html>