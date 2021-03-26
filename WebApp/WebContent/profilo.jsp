<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%

	DBManagement gestioneDB = new DBManagement();
	UtentiBean utente = new UtentiBean();
	
	utente = gestioneDB.ottieni_dati_utente(request.getSession().getAttribute("Utente").toString()).get(0);

%>