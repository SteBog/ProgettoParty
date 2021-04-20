<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.3.4/gsap.min.js"></script>
		<link href="stili.css" rel="stylesheet" type="text/css">
		<script src="script.js"></script>
	</head>
		<body>
			<form action="/WebApp/Servlet1" method="post">
				<div class="container" id="div_login">
						<%
							if(request.getSession().getAttribute("Error") == "true")
							{
								
						%>
								<span class="titolo_progetto">Progetto Party</span>
								<input type="text" name="username" class="errore" id="username_login" placeholder="Nome Utente">
								<input type="password" name="password" class="errore" id="password_login" placeholder="Password">
								<span class="scritta_errore">Errore! Utente o password sbagliato.</span>
								<input type="submit" class="pulsante_form" value="Accedi">
								<span>Login fallito</span>
						<%
							}
							else
							{
						%>
							<span class="titolo_progetto">Progetto Party</span>
							<input type="text" name="username" id="username_login" placeholder="Nome Utente">
							<input type="password" name="password" id="password_login" placeholder="Password">
							<input type="submit" class="pulsante_form" value="Accedi">
						<%
							}
						%>
					<span class="scritta_basso" onclick="prossimo_div_login();">Non hai un account? Registrati!</span>
				</div>
			</form>
			<form action="/WebApp/Servlet1" method="post">
				<div class="container" id="div_registrazione_first" style="display: none;">
					<span class="titolo_progetto">Progetto Party</span>
					<input type="text" name="email" id="email_registrazione" placeholder="Email">
					<input type="password" name="password" id="password_registrazione" placeholder="Password">
					<input type="data" name="dataNascita" id="dataNascita_registrazione" placeholder="La tua data di nascita">
					<input type="button" onclick="prossimo_div_registrazione();" class="pulsante_form" value="Avanti">
					<span class="scritta_basso" onclick="precedente_div_login();">Torna alla schermata di login</span>
				</div>
				<div class="container" id="div_registrazione_second" style="display: none;">
					<span class="titolo_progetto">Progetto Party</span>
					<input type="text" name="username" id="username_registrazione" placeholder="Nome Utente">
					<input type="submit" class="pulsante_form" value="Registrati">
					<span class="scritta_basso" onclick="precedente_div_registrazione();">Torna alla schermata precedente</span>
				</div>
			</form>
		</body>
</html>