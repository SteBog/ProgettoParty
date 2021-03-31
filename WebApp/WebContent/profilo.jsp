<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%

	DBManagement gestioneDB = new DBManagement();
	ArrayList<UtentiBean> utente = new ArrayList<UtentiBean>();
	
	utente = gestioneDB.ottieni_dati_utente(request.getSession().getAttribute("Utente").toString());

%>