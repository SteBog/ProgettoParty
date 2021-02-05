<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Insert title here</title>
</head>
<body>

<form name="esempio" action="/ProvaServlet/ProvaServlet" method="post">
	<a href="/ProvaServlet/ProvaServlet" target="_top">Servlet</a>
	<input type="text" name="nome">		<!-- Parametro passato tramite testo -->
	<input type="submit" name="nome">
</form>
</body>
</html>