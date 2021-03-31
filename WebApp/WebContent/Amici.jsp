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
		<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.3.4/gsap.min.js"></script>
		<script src="script.js"></script>
		<style>
			
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
			
			.NomeProfilo{
				margin-left:10px;
			}
			
			.Navbar{
				background-image: linear-gradient(to bottom left, #80d0c7, #13547a);
				list-style-type:none;
				width:200px;
				height:100vh;
				margin-right: 30px;
				border: 0;
				margin: 0;
				padding: 0;
				color: #ffffff;
				position:relative;
				
			}
			
			.profilo{
				position: absolute;
				bottom: 0px;
				margin-bottom:10px;
				display: flex;
				flex-direction: row;
				align-items: center;
			}
			
			.TitoloNav{
				font-size: 40px;
				text-decoration: none;
				text-align:center;
				margin-bottom:20px;
			}
			
			.TestoNav{
				font-size: 15px;
				text-decoration: none;
				margin-left:20px;
				margin-bottom:10px;
			}
			
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
			
			
			
		</style>
	</head>
	<body>
		<ul class="Navbar">
			<li class="TitoloNav">Progetto Party</li>
			<li class="TestoNav"><a href=#>Homepage</a></li>
			<li class="TestoNav"><a href="Amici.jsp">I tuoi amici</a></li>
			<li class="TestoNav"><a href="Statistiche.jsp">Statistiche</a></li>
			<li class="TestoNav"><a href=#>Come giocare</a></li>
			<li class="profilo">
				<div class="immagine_profilo">
				</div>
				<span class="NomeProfilo"><%= request.getSession().getAttribute("Utente").toString() %></span>
		</ul>
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
		</div>
	<% } %>
	</body>
</html>