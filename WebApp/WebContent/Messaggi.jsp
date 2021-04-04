<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%
	DBManagement listMessaggi = new DBManagement();
	ArrayList<MessaggioBean> messaggi = new ArrayList<MessaggioBean>();
	// Utente da session
	messaggi = listMessaggi.selectMessaggi(request.getSession().getAttribute("Utente").toString(), "SteBog");
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.3.4/gsap.min.js"></script>
		<link rel="stylesheet" href="stili_home.css">
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
			
			
			
			.chat-message {
  			width: 80%;
  			margin: 1em auto;
  			border: 1px solid grey;
  			display: flex;
  			justify-content: flex-end;
			}
			
			.chat-message-text {
  			text-align: right;
			}
			
			.chat-message-timestamp {
  			white-space: nowrap;
 			padding-left: 1em;
 			color: #aaa;
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
		<div>
	<%
		for(MessaggioBean messaggio:messaggi)
		{
			String Testo = messaggio.getTesto();
			Date Data = new Date();
			Data = messaggio.getData();
	%>
		<div class="chat-message">
			<div class="chat-message-text"><%=Testo %></div>
			<span class="chat-message-timestamp"><%=Data %></span>
		</div>
	<% } %>
	</div>
	</body>
</html>