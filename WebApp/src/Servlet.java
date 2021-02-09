package prova;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class Prova1
 */
@WebServlet("/Prova1")
public class Prova1 extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Prova1() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		ServletContext sc = request.getSession().getServletContext();
		request.removeAttribute("COMPANIES");

		DBManagement listaAmici = new DBManagement();
		ArrayList<AmiciziaBean> amiciInDB = new ArrayList<AmiciziaBean>();
		try
		{
			amiciInDB = listaAmici.selectCompanies();
			//RequestDispatcher rd = sc.getRequestDispatcher("/listaAmici.jsp");
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
		String nome = request.getParameter("nome");

		
		//Esempio di cookie
			//Creazione di cookie
		Cookie[] cookies = request.getCookies();
		int lun = cookies.length;
		if (cookies.length == 1)   //esiste sempre 1 che è l'id di sessione
		{
			Cookie cookieName = null;
			cookieName = new Cookie("nomeCompany", nome);
			response.addCookie(cookieName);
		}
		else
		{
			//Esempio di cookie
			//Lettura di cookie
			for (int i = 0; i < cookies.length; i++)
			{
				response.getWriter().append(cookies[i].getName() + " " + cookies[i].getValue() + " ");
			}
		}

		//Lettura di un attributo della sessione
		if (request.getSession().getAttribute("NOMEUTENTE") == null)
		{
			//Aggiunta di un attributo alla sessione
			request.getSession().removeAttribute("NOMEUTENTE");
			request.getSession().setAttribute("NOMEUTENTE", nome);
		}
		response.getWriter().append("sessione - nome utente: " + 
				request.getSession().getAttribute("NOMEUTENTE") + " ");

		CompanyBean company = new CompanyBean();
		company.setCompany_name(nome);
		company.setEmail(email);
		company.setPhone(phone);
		DBManagement saveCompany = new DBManagement();
		
		ServletContext sc = request.getSession().getServletContext();
		
		try
		{
			saveCompany.insertCompany(company);
			
			RequestDispatcher rd = sc.getRequestDispatcher("/insertok.jsp");
			rd.forward(request, response);
			//response.sendRedirect("/insertok.jsp");
		}
		catch (SQLException e)
		{
			System.out.println("ERROR:" + e.getErrorCode() + ":" + e.getMessage());
			e.printStackTrace();
			request.getSession().removeAttribute("COMPANY");
			RequestDispatcher rd = sc.getRequestDispatcher("/error.jsp");
			rd.forward(request, response);
			//response.sendRedirect("/error.jsp");
		}
	}

}