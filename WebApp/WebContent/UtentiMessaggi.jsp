<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%
		DBManagement listMessaggi = new DBManagement();
		ArrayList<MessaggioBean> messaggi = new ArrayList<MessaggioBean>();
		// Utente da session
		messaggi = listMessaggi.selectUtentiMessaggi(request.getSession().getAttribute("Utente").toString());
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
				margin-right: 20px;
				margin-top: 40px;
				margin-left: 20px;
				margin-bottom: 20px;
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
			
			.icon_friend
			{
				display: block;
				height: auto;
				width: 200px;
				margin: 70px 0px 0px 20px;
				background-size: 100%;
				border: 1px solid black;
				padding: 30px;
				color: black;
				text-decoration: none;
				border-radius: 10px;
				text-align: center;
			}
			.container
			{
				margin-top: 0px;
				display: flex;
				flex-wrap: wrap;
			}
			.container span
			{
				display: block;
				margin: 5px 0px;
				width: 100%;
			}
			.non-visibile
			{
				display: none;
			}
			.titolo
			{
				margin-top: 75px;
				font-size: 48px;
				margin-left: 40%;
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
	    <span class="titolo">Chat recenti:</span>
		<div class="container">
		<%
			for(MessaggioBean messaggio:messaggi)
			{
				String Username = messaggio.getUtente();
		%>
			<div class="div_amici">
				<span><%=Username %></span>
				<a href="/WebApp/ServletMessaggi?UtenteRicevente=<%=Username %>" class="icon_msg"></a>
			</div>
		<% } %>
		</div>
	</body>
</html>