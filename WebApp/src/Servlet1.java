import JavaBeans.*;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.ArrayList;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class Servlet1
 */
@WebServlet("/Servlet1")
public class Servlet1 extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Servlet1() {
        super();
        // TODO Auto-generated constructor stub
    }
    
    /**
	 * @see Servlet#init(ServletConfig)
	 */
	public void init(ServletConfig config) throws ServletException {
		// TODO Auto-generated method stub
		super.init();
		// Altro codice a mia discrezione
	}

	/**
	 * @see Servlet#destroy()
	 */
	public void destroy() {
		// TODO Auto-generated method stub
		super.destroy();
		// Altro a mia discrezione
	}

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		ServletContext sc = request.getSession().getServletContext();
		request.removeAttribute("Utenti");
		DBManagement listUtenti = new DBManagement();
		ArrayList<UtentiBean> utenti = new ArrayList<UtentiBean>();
		try
		{
			utenti = listUtenti.selectUtenti();
			request.setAttribute("COMPANIES", utenti);
			RequestDispatcher rd = sc.getRequestDispatcher("/NewFile.jsp");
			rd.forward(request, response);
		}
		catch (SQLException e)
		{
			e.printStackTrace();
			RequestDispatcher rd = sc.getRequestDispatcher("/error.jsp");
			rd.forward(request, response);
		}
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String Username = request.getParameter("username");
		String Password = request.getParameter("password");
		
		// Esempio
		response.setContentType("text/html");
		PrintWriter out = response.getWriter();

		ServletContext sc = request.getSession().getServletContext();
		request.removeAttribute("Utenti");
		DBManagement listUtenti = new DBManagement();
		ArrayList<UtentiBean> utenti = new ArrayList<UtentiBean>();
		try
		{
			utenti = listUtenti.selectUtenti();
			request.setAttribute("Utenti", utenti);
			RequestDispatcher rd = sc.getRequestDispatcher("/NewFile.jsp");
			rd.forward(request, response);
		}
		catch (SQLException e)
		{
			e.printStackTrace();
			RequestDispatcher rd = sc.getRequestDispatcher("/index.jsp");
			rd.forward(request, response);
		}
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

}
