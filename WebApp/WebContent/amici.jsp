<%@
page import =  java.util.ArrayList,java.util.Date,JavaBeans.*;
%><!DOCTYPE html>
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
			<li class="TestoNav">Homepage</li>
			<li class="TestoNav">I tuoi amici</li>
			<li class="TestoNav">Come giocare</li>
			<li class="profilo">
				<div class="immagine_profilo">
				</div>
				<span class="NomeProfilo">Nome Profilo</span>
		</ul>
			<div class="div_amici">
				<div class="immagine_profilo">
				</div>
				<span class="NomeProfilo">Nome Profilo</span>
			</div>
	<%
		for(UtentiBean utenti:utentiList)
		{
			String Username = utenti.getUsername();
			Date Disconnessione = utenti.getDisconnessione();
	%>
		<div class="div_amici">
				<div class="immagine_profilo">
				</div>
			<span class="NomeProfilo"><%=Username %></span>
			<span><%=Disconnessione %></span>
		</div>
		<%
		}
	%>
	</body>
</html>