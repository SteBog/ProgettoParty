<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%

	DBManagement gestioneDB = new DBManagement();
	ArrayList<UtentiBean> utente = new ArrayList<UtentiBean>();
	
	utente = gestioneDB.ottieni_dati_utente(request.getSession().getAttribute("Utente").toString());
	
	String nome_utente = utente.get(0).getUsername();

%>

<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profilo di <%=utente.get(0).getUsername() %></title>
    <link rel="stylesheet" href="stili_home.css">
    <style>
        html, body
        {
            background: #ecf0f3;
            margin: 0;
            border: 0;
            padding: 0;
        }
        .container
        {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            width: 800px;
            height: 500px;
            border-radius: 15px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
            display: flex;
        }
        .container_foto
        {
            width: 50%;
            height: 100%;
            border-radius: 15px 0px 0px 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .container_dati
        {
            width: 50%;
            height: 100%;
            border-radius: 0px 15px 15px 0px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }
        .container_dati label
        {
            color: #8c8c8c;
            width: 80%;
            font-size: 16px;
            margin-top: 20px;
            margin-left: 50px;
        }
        .container_dati span
        {
            width: 80%;
            font-size: 18px;
            margin-left: 50px;
        }
        .container_dati input[type=text], .container_dati input[type=password]
        {
            display: none;
            margin-left: 50px;
        }
        .container_img
        {
            width: 70%;
            height: 100%;
            border-radius: 0px 15px 15px 0px;
        }
        .container_img a
        {
            height: 150px;
            width: 150px;
            border: none;
        }
        .modifica_profilo
        {
            margin-top: 50px;
            margin-left: 50px;
        }
        .pulsante
        {
            color: white;
            background-color: #80d0c7;
            border: 0;
            padding: 8px 15px;
            border-radius: 3px;
            transition: all 0.3s ease;
        }
        .pulsante:hover
        {
            background-color: #13547a;
        }
        .foto_profilo
        {
            margin: 30px;
            height: 150px;
        }
    </style>
    <script>
        function converti_in_input()
        {
            let campi = ["username", "email", "password", "data_nascita"]

            for (let i = 0; i < campi.length; i++)
            {
                document.getElementById(campi[i]).style.display = "block"
                document.getElementById("span_" + campi[i]).style.display = "none"

                document.getElementById("conferma").style.display = "block"
                document.getElementById("cambia").style.display = "none"
            }
        }
        
        function scegli_foto()
        {
            document.getElementById("container_dati").style.display = "none"
            document.getElementById("container_img").style.display = "flex"
        }
    </script>
</head>
<body>
	<nav>
        <a href="presentazione.jsp" class="TitoloNav">Progetto Party</a>
        <div class="div-nav">
            <a href="Amici.jsp" class="TestoNav">I tuoi amici</a>
            <a href="profilo.jsp" class="profilo"><%=request.getSession().getAttribute("Utente").toString() %></a>
        </div>
    </nav>
    <div class="container">
        <div class="container_foto">
            <img class="foto_profilo" src="img/<%=utente.get(0).getFotoProfilo() %>.png" alt="Game avatar">
            <input type="button" class="pulsante" value="Cambia Avatar" class="cambia_avatar" onclick="scegli_foto()">
        </div>
        <form action="/WebApp/Servlet_modifica_utente" method="post" class="container_dati" id="container_dati">
            <label for="username">Nome utente</label>
            <span id="span_username"><%=utente.get(0).getUsername() %></span>
            <input type="text" name="username" id="username" value="<%=utente.get(0).getUsername() %>">

            <label for="email">Email</label>
            <span id="span_email"><%=utente.get(0).getEmail() %></span>
            <input type="text" name="email" id="email" value="<%=utente.get(0).getEmail() %>">

            <label for="password">Password</label>
            <span id="span_password">********</span>
            <input type="password" name="password" id="password" value="">

            <label for="data_nascita">Data di nascita</label>
            <span id="span_data_nascita"><%=utente.get(0).getDataNascita() %></span>
            <input type="text" name="data_nascita" id="data_nascita" value="<%=utente.get(0).getDataNascita() %>">
            
            <input type="button" value="Cambia" id="cambia" class="pulsante modifica_profilo" onclick="converti_in_input()">
            <input type="submit" value="Conferma" id="conferma" class="pulsante modifica_profilo" style="display: none;">
        </form>
        <div id="container_img" class="container_img" style="display: none;">
            <a href="/WebApp/Servlet_modifica_utente?img=1" style="background: url('img/1.png') center no-repeat; background-size: 50%;"></a>
            <a href="/WebApp/Servlet_modifica_utente?img=2" style="background: url('img/2.png') center no-repeat; background-size: 50%;"></a>
            <a href="/WebApp/Servlet_modifica_utente?img=3" style="background: url('img/3.png') center no-repeat; background-size: 50%;"></a>
            <a href="/WebApp/Servlet_modifica_utente?img=4" style="background: url('img/4.png') center no-repeat; background-size: 50%;"></a>
            <a href="/WebApp/Servlet_modifica_utente?img=5" style="background: url('img/5.png') center no-repeat; background-size: 50%;"></a>
        </div>
    </div>
</body>
</html>