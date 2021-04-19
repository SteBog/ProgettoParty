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
				width: 30px;
				height: 30px;
				background-image: url("img/Icon_msg.png");
				background-size: cover;
				border: 0px solid black;
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
			form
			{
				margin-top: 0px;
				display: flex;
				flex-wrap: wrap;
			}
			form span
			{
				display: block;
				margin: 5px 0px;
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
			<a href="profilo.jsp" class="profilo"><!--<%=request.getSession().getAttribute("Utente").toString() %>--></a>
		</nav>
		<a href="ListaUtenti.jsp" class="icon_friend">Stringi una nuova amicizia</a>
		<form action="/WebApp/ServletMessaggi" method="post">
		<%
			for(UtentiBean utente:utenti)
			{
				String Username = utente.getUsername();
		%>
			<div class="div_amici">
				<span><%=Username %></span>
				<span>Nome Utente</span>
				<<span>Ultimo accesso:<%//Disconnessione %></span>
				<span>Ultimo accesso: oggi</span>
				<span>
					<input type="submit" name="UtenteRicevente" value="" class="icon_msg">
				</span>
			</div>
			<div class="div_amici">
				<span><%=Username %></span>
				<span>Nome Utente</span>
				<span>Ultimo accesso:<%//Disconnessione %></span>
				<span>Ultimo accesso: oggi</span>
				<span>
					<input type="submit" name="UtenteRicevente" value="" class="icon_msg">
				</span>
			</div>
			<div class="div_amici">
				<span><%=Username %></span>
				<span>Nome Utente</span>
				<span>Ultimo accesso:<%//Disconnessione %></span>
				<span>Ultimo accesso: oggi</span>
				<span>
					<input type="submit" name="UtenteRicevente" value="" class="icon_msg">
				</span>
			</div>
		<% } %>
		</form>
	</body>
</html>