<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%
	DBManagement listUtenti = new DBManagement();
	ArrayList<UtentiBean> utenti = new ArrayList<UtentiBean>();
	// Utente da session
	utenti = listUtenti.selectRichiesteAmico(request.getSession().getAttribute("Utente").toString());
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="stili_home.css">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.3.4/gsap.min.js"></script>
		<script src="script.js"></script>
		<style>
			html, body
			{
				width: 100%;
				height: 100vh;
				border: 0;
				margin: 0;
				padding: 0;
				background-color: #ecf0f3;
				background-repeat:no-repeat;
				background-size: 100%;
			}
			.container
            {
                display: flex;
                flex-wrap: wrap;
                margin: 60px auto 0px auto;
                width: 60%;
                justify-content: center;
            }
            .utente
            {
                width: 200px;
                height: 100px;
                background: white;
                border-radius: 15px;
                margin: 5px;
                padding: 10px;
                display: flex;
                justify-content: space-evenly;
                align-items: center;
            }
            .immagine-profilo
            {
                height: 100%;
                width: 50px;
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;
            }
            .nome-profilo
            {
                display: block;
            }
            .chat-utente
            {
                display: inline-block;
                width: 20px;
                height: 20px;
                background: url('img/Icon_msg.png');
                background-size: contain;
            }
            .aggiungi-amico
            {
                display: inline-block;
                width: 20px;
                height: 20px;
                background: url('img/Icon_friend.png');
                background-size: contain;
            }
		</style>
	</head>
	<body>
		<nav>
	        <div class="div-nav">
	            <a href="presentazione.jsp" class="TitoloNav">Progetto Party</a>
	            <a href="Amici.jsp" class="TestoNav">I tuoi amici</a>
	            <a href="" class="TestoNav">Come giocare</a>
	        </div>
	        <a href="profilo.jsp" class="profilo"><%=request.getSession().getAttribute("Utente").toString() %></a>
		</nav>
        <div class="container">
            <%
                for(UtentiBean utente:utenti)
                {
                    String Username = utente.getUsername();
                    String foto_profilo = utente.getFotoProfilo();
                    //Date Disconnessione = utente.getDisconnessione();
            %>
            <div class="utente">
            Richiesta:
                <div class="immagine-profilo" style="background-image: url('img/<%=foto_profilo %>.png');"></div>
                <div class="dettagli-profilo">
                    <span class="nome-profilo"><%=Username %></span>
                    <a class="chat-utente" href="/WebApp/ServletMessaggi?UtenteRicevente=<%=Username %>"></a>
                    <a class="aggiungi-amico" href="ListaRichieste.jsp" onclick="<%
                        listUtenti.accettaRichiestaAmico(request.getSession().getAttribute("Utente").toString(), Username);
                    %>"></a>
                </div>
            </div>
            <% } %>
    	</div>
	</body>
</html>