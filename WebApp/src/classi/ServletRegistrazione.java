
package classi;
import JavaBeans.*;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Date;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class ServletRegistrazione
 */
@WebServlet("/ServletRegistrazione")
public class ServletRegistrazione extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ServletRegistrazione() {
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
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String Username = request.getParameter("username");
		String Password = request.getParameter("password");
		String Email = request.getParameter("email");
		String DataNascita = request.getParameter("dataNascita");
		
		// Esempio
		response.setContentType("text/html");

		ServletContext sc = request.getSession().getServletContext();
		request.removeAttribute("Utenti");
		DBManagement listUtenti = new DBManagement();
		try
		{
			listUtenti.Registrazione(Username,Password,Email,DataNascita);
				
				request.getSession().setAttribute("Utente", Username);
				RequestDispatcher rd = sc.getRequestDispatcher("/presentazione.jsp");
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