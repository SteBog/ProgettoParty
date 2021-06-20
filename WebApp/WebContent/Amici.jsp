<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%
	DBManagement listUtenti = new DBManagement();
	ArrayList<UtentiBean> utenti = new ArrayList<UtentiBean>();
	// Utente da session
	utenti = listUtenti.selectAmici(request.getSession().getAttribute("Utente").toString());
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="stili_home.css">
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
				display: flex;
				flex-direction: column;
			}
			.div_amici
			{
				border-radius: 5px;
				/*background: #ecf0f3;
				box-shadow:  5px 5px 5px #87898b,
                -5px -5px 5px #ffffff;*/
				background: white;
				height: 100px;
				width: 200px;
				margin-right:20px;
				margin:20px;
				display: flex;
				flex-direction: column;
				align-items: flex-start;
				padding: 15px;
			}
			.immagine_profilo
			{
				width: 30px;
				height: 30px;
				border-radius: 50%;
				background-image: url("default.png");
				background-size: 100%;
			}
			
			.icon_msg
			{
				width: 20px;
				height: 20px;
				background-image: url("img/Icon_msg.png");
				background-size: cover;
				border: 0px solid black;
				margin: 2px;
			}
			.icon_stats
			{
				width: 20px;
				height: 20px;
				background-image: url("img/icon_stats.png");
				background-size: cover;
				border: 0px solid black;
				margin: 2px;
			}
			
			.richiesta_amicizia
			{
				display: block;
				height: auto;
				width: 45%;
				background-size: 100%;
				border-bottom: 1px solid black;
				border-right: 1px solid black;
				padding: 30px;
				color: black;
				text-decoration: none;
				text-align: center;
				background-color: #d7d7d7;
				opacity:0.2;
			}
			.amicizia_sopseso{
				display: block;
				height: auto;
				width: 45%;
				background-size: 100%;
				border-bottom: 1px solid black;
				border-left: 1px solid black;
				padding: 30px;
				color: black;
				text-decoration: none;
				text-align: center;
				background-color: #d7d7d7;
				opacity:0.2;
			}
			.container
			{
				margin-top: 0px;
				display: flex;
				flex-wrap: wrap;
			}
			.container_button
			{				
				display: flex;
				flex-wrap: wrap;
				flex-direction:row;
			}
			.container span
			{
				display: block;
				margin: 5px 0px;
				width: 100%;
			}
			button_container{
				float: left;
			}
			.non-visibile
			{
				display: none;
			}
			.chat
			{
				width: 50px;
				height: 50px;
				background-size: contain;
				background-image: url(img/Icon_msg.png);
				background-repeat: no-repeat;
				margin-left: 180vh;
				margin-top: 10px;
				border-radius: 50%;
				border: 1px solid black;
			}
		</style>
	</head>
	<body>
		<nav>
        <a href="presentazione.jsp" class="TitoloNav">Progetto Party</a>
        <div class="div-nav">
            <a href="Amici.jsp" class="TestoNav">I tuoi amici</a>
            <a href="profilo.jsp" class="profilo"><%=request.getSession().getAttribute("Utente").toString() %></a>
        </div>
    </nav>
	<a class="chat" href="UtentiMessaggi.jsp"></a>
	<div class="container_button">
			<a href="ListaUtenti.jsp" class="richiesta_amicizia">Invia richiesta amico</a>
			<a href="ListaRichieste.jsp" class="amicizia_sopseso">Richieste in sospeso</a>
	</div>
		<div class="container">
		<%
			for(UtentiBean utente:utenti)
			{
				String Username = utente.getUsername();
		%>
			<div class="div_amici">
				<span><%=Username %></span>
				<span>Ultimo accesso:<%//Disconnessione %></span>
				<a href="/WebApp/ServletMessaggi?UtenteRicevente=<%=Username %>" class="icon_msg"></a>
				<a href="/WebApp/VisualizzaStatistiche?utente_richiesto=<%=Username %>" class="icon_stats"></a>
			</div>
		<% } %>
		</div>
	</body>
</html>