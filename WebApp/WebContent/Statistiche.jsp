<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Date" %>
<%@ page import="JavaBeans.*" %>
<%@ page import="classi.DBManagement" %>
<%@ page import="classi.Servlet1" %>

<%
	DBManagement listVittorie = new DBManagement();

	String utente = request.getSession().getAttribute("Utente").toString();
	int vittorie = listVittorie.selectVittorie(utente);
	int giocate = listVittorie.numero_partite_giocate(utente);
	int ore_giocate = listVittorie.ore_giocate(utente);
	int percentuale = 0;
	
	if (giocate > 0) percentuale = (vittorie/giocate) * 100;
	
	ArrayList<qVittorieMinigiochiBean> vittorieMinigiochi = new ArrayList<qVittorieMinigiochiBean>();
	vittorieMinigiochi = listVittorie.selectVittorieMinigiochi(request.getSession().getAttribute("utente_richiesto").toString());
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.3.4/gsap.min.js"></script>
        <link rel="stylesheet" href="stili_home.css">
		<script src="script.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
        <style>
            .container
            {
                position: relative;
                left: 50%;
                top: 50px;
                transform: translateX(-50%);
                width: 1000px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .grafico
            {
                width: 300px;
                height: 300px;
            }
            .scritta
            {
                font-size: 24px;
                margin: 30px 0px;
                width: 300px;
                text-align: center;
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
		<div class="container">
            <span class="scritta">Percentuale partite vinte: <%=percentuale %>%</span>
            <div class="grafico">
                <canvas id="grafico_vittorie_perse" width="200" height="200"></canvas>
            </div>
            <span class="scritta">Quante volte hai trionfato al tuo minigioco preferito?</span>
            <div class="grafico">
                <canvas id="grafico_minigiochi" width="500" height="500"></canvas>
            </div>
            <span class="scritta">Tempo di gioco: <%=ore_giocate %> ore</span>
        </div>
        <%
        	for (int i = 0; i < vittorieMinigiochi.size(); i++)
        	{
        		String numero = vittorieMinigiochi.get(i).toString();
        %>
        	<span><%=numero %></span>
        <%
        	}
        %>
	</body>
    <script>
    
    	var vittorie = <%=vittorie %>;
    	var perse = <%=giocate-vittorie %>;
    
        var ctx = document.getElementById("grafico_vittorie_perse")
        var myDoughnutChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [perse, vittorie],
                    backgroundColor: ["rgba(150, 0, 0, 0.8)", "rgba(0, 150, 0, 0.5)"],
                }],
                labels: [
                    'Perse',
                    'Vinte'
                ]
            },
            options: Chart.defaults.doughnut
        });

        var barre = document.getElementById("grafico_minigiochi")
        var myBarChart = new Chart(barre, {
            type: 'bar',
            data: {
                labels: ["Spintoni", "Pong", "Gara", "Paracadutismo"],
                datasets: [{
                    label: "",
                    barPercentage: 0.5,
                    barThickness: 6,
                    maxBarThickness: 8,
                    minBarLength: 0,
                    backgroundColor: ["rgba(0, 110, 200, 0.6)", "rgba(200, 0, 103, 0.6)", "rgba(200, 157, 0, 0.6)", "rgba(200, 73, 0, 0.6)"],
                    borderColor: ["rgba(0, 110, 200, 0.8)", "rgba(200, 0, 103, 0.8)", "rgba(200, 157, 0, 0.8)", "rgba(200, 73, 0, 0.8)"],
                    borderWidth: 1,
                    data: [
                        23,
                        20,
                        27,
                        25
                    ]
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        stacked: true
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                }
            }
        });
    </script>
</html>