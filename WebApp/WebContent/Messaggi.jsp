<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%
	DBManagement listMessaggi = new DBManagement();
	ArrayList<MessaggioBean> messaggi = new ArrayList<MessaggioBean>();
	// Utente da session
	messaggi = listMessaggi.selectMessaggi(request.getSession().getAttribute("Utente").toString(), request.getSession().getAttribute("UtenteRicevente").toString());
%>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="stili_home.css">
    <title>Chat</title>
    <style>
        html, body
        {
            background-color: #ecf0f3;
        }
        .barra-inserimento
        {
            position: fixed;
            display: flex;
            justify-content: flex-start;
            bottom: 10px;
            width: 500px;
            height: 30px;
            left: 50%;
            transform: translateX(-50%);
        }
        .barra-inserimento input[type=text]
        {
            width: 90%;
            height: 26px;
            border: 0;
            padding: 2px;
            border-radius: 10px;
        }
        .barra-inserimento input[type=submit]
        {
            width: 30px;
            height: 30px;
            margin-left: 15px;
        }
        .container-messaggi
        {
            position: relative;
            top: 70px;
            left: 50%;
            transform: translateX(-50%);
            width: 500px;
            height: calc(100vh - 200px);
            display: flex;
            flex-direction: column;
            overflow: scroll;
        }
        .messaggio
        {
            background: white;
            max-width: 250px;
            padding: 20px;
            border-radius: 15px;
            margin-top: 10px;
        }
        .messaggio pre
        {
            font-family: 'Courier New', Courier, monospace;
            margin: 5px 0px;
            max-width: 200px;
            white-space: pre-wrap;
        }
        .date-messaggio
        {
            font-size: 12px;
            color: #8c8c8c;
        }
        .local-messaggio
        {
            align-self: flex-end;
        }
        .remote-messaggio
        {
            align-self: flex-start;
            background: yellowgreen;
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
    <div class="container-messaggi">
        <%
			for(MessaggioBean messaggio:messaggi)
			{
				String Utente = messaggio.getUtente();
				String Testo = messaggio.getTesto();
				Date Data = new Date();
				Data = messaggio.getData();
                if (Utente.equals(request.getSession().getAttribute("Utente").toString()))
                {
                	%>
                    <div class="messaggio local-messaggio">
                        <b class="usr-messaggio"><%=Utente %></b>
                        <pre class="txt-messaggio"><%=Testo %></pre>
                        <pre class="date-messaggio"><%=Data %></pre>
                    </div>
                    <% 
                }
                else
                {
                	%>
                    <div class="messaggio remote-messaggio">
                        <b class="usr-messaggio"><%=Utente %></b>
                        <pre class="txt-messaggio"><%=Testo %></pre>
                        <pre class="date-messaggio"><%=Data %></pre>
                    </div>
                    <% }
                }
        %>
    </div>
    <form action="/WebApp/ServletInviaMessaggio" method="post" class="barra-inserimento">
        <input type="text" name="messaggio" id="">
        <input type="submit" value="">
    </form>
</body>
</html>