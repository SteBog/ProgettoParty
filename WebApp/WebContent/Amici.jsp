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
				display: flex;
			}
			.div_amici{
				border-radius: 5px;
				background: #ecf0f3;
				box-shadow:  5px 5px 5px #87898b,
                -5px -5px 5px #ffffff;
				height: 50px;
				width: 400px;
				margin-right:20px;
				margin:20px;
				display: flex;
				flex-direction: row;
				align-items: center;
			}

			.immagine_profilo{
				width: 30px;
				height: 30px;
				border-radius: 50%;
				background-image: url("default.png");
				background-size: 100%;
				margin-left:15px;
			}
			
			.icon_msg{
				width: 30px;
				height: 30px;
				background-image: url("img/Icon_msg.png");
			}
		</style>
	</head>
	<body>
		<nav>
	        <!-- <div class="div-nav">
	            <a href="presentazione.jsp" class="TitoloNav">Progetto Party</a>
	            <a href="Amici.jsp" class="TestoNav">I tuoi amici</a>
	            <a href="" class="TestoNav">Come giocare</a>
	        </div>
	        <a href="profilo.jsp" class="profilo"><%=request.getSession().getAttribute("Utente").toString() %></a>
		</nav>-->
	<form action="/WebApp/ServletMessaggi" method="post">
	<%
		for(UtentiBean utente:utenti)
		{
			String Username = utente.getUsername();
			//Date Disconnessione = utente.getDisconnessione();
	%>
		<div class="div_amici">
				<div class="immagine_profilo">
				</div>
			<span class="NomeProfilo">Nome: <%=Username %></span>
			<span>Ultimo accesso:<%//Disconnessione %></span>
			<span><input type="submit" name="UtenteRicevente" value="<%=Username %>"><img src="img/Icon_msg.png" class="icon_msg"></span>
		</div>
	<% } %>
	</form>
	</body>
</html>