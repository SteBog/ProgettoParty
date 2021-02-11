<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Insert title here</title>
</head>
<body>

<form name="esempio" action="/WebApp/Servlet1" method="post">
	<a href="/WebApp/Servlet1" target="_top">Servlet</a>
	<br>
	<input type="text" name="Username">		<!-- Parametro passato tramite testo -->
	<br>
	<input type="text" name="Password">		<!-- Parametro passato tramite testo -->
	<br>
	<br>
	<input type="submit" name="invia">
</form>
</body>
</html>