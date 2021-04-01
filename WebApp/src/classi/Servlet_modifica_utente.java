package classi;

import java.io.IOException;
import java.sql.SQLException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import JavaBeans.UtentiBean;

/**
 * Servlet implementation class Servlet_modifica_utente
 */
@WebServlet("/Servlet_modifica_utente")
public class Servlet_modifica_utente extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Servlet_modifica_utente() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		UtentiBean utente = new UtentiBean();
		utente.setUsername(request.getParameter("username").toString());
		utente.setEmail(request.getParameter("email").toString());
		utente.setPassword(request.getParameter("password").toString());
		
		String data_nascita = request.getParameter("data_nascita").toString();
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date d = null;
		try {
			d = sdf.parse(data_nascita);
		} catch (ParseException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		sdf.applyPattern("yyyy-MM-dd");
		
		utente.setDataNascita(d);
		
		String old_Username = request.getSession().getAttribute("Utente").toString();
		
		// Esempio
		response.setContentType("text/html");

		ServletContext sc = request.getSession().getServletContext();
		
		DBManagement gestoreDB = new DBManagement();
		
		try {
			gestoreDB.aggiorna_utente(utente, old_Username);
			request.getSession().removeAttribute("Utente");
			request.getSession().setAttribute("Utente", utente.getUsername());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		RequestDispatcher rd = sc.getRequestDispatcher("/Amici.jsp");
		rd.forward(request, response);
	}

}
