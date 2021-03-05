

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import JavaBeans.*;

public class DBManagement {
	
	//Parametri di accesso al database
	private static final String DB_DRIVER = "com.mysql.jdbc.Driver";
	private static final String DB_CONNECTION = "jdbc:mysql://87.250.73.23:3306/Party";
	private static final String DB_USER = "adminer";
	private static final String DB_PASSWORD = "CBC349aa";
	
	private static Connection getDBConnection() throws Exception
	{
		System.out.println("-------MYSQL JDBC Connection----------");
		Connection dbConnection = null;
		
		try
		{
			Class.forName(DB_DRIVER);
		}
		catch (ClassNotFoundException e)
		{
			System.out.println("ERROR: MySQL JDBC Driver not found!!!");
			throw new Exception(e.getMessage());
		}
		
		try
		{
			dbConnection = DriverManager.getConnection(DB_CONNECTION, DB_USER, DB_PASSWORD);
			System.out.println("SQL Connection to Party database established!");
		}
		catch (SQLException e)
		{
			System.out.println("Connection to Party database failed");
			throw new SQLException(e.getErrorCode() + ":" + e.getMessage());
		}
		return dbConnection;
	}
	
	public ArrayList<UtentiBean> selectUtenti(String Username,String Password) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT * FROM Utenti WHERE Username='" + Username + "' AND Password ='"  + Password + "';";
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet utentiList = stmt.executeQuery(select);
			
			ArrayList<UtentiBean> utentiArray = new ArrayList<UtentiBean>();
			while (utentiList.next())
			{
				UtentiBean Utenti = new UtentiBean();
				Utenti.setEmail(utentiList.getString("Email"));
				Utenti.setPassword(utentiList.getString("Password"));
				Utenti.setUsername(utentiList.getString("Username"));
				Utenti.setFotoProfilo(utentiList.getString("FotoProfilo"));
				Utenti.setDataNascita(utentiList.getDate("DataNascita"));
				Utenti.setDisconnessione(utentiList.getDate("Disconnessione"));
				// PER TUTTI I CAMPI
				
				utentiArray.add(Utenti);
			}
			return utentiArray;
		}
		catch(SQLException sqle)
		{
			System.out.println("SELECT ERROR");
			System.out.println(select);
			throw new SQLException(sqle.getErrorCode() + ":" + sqle.getMessage());
			
		}
		catch(Exception err)
		{
			System.out.println("GENERIC ERROR");
			throw new SQLException(err.getMessage());
		}
		finally
		{
			if (stmt != null)
			{
				stmt.close();
			}
			if (conn != null)
			{
				conn.close();
			}
		}
	}
	
	public int selectStatUtenti(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT COUNT(Partita.Vincitore) AS Vittorie FROM Partita INNER JOIN Utenti ON Partita.Vincitore = Utenti.IDUtente WHERE Utenti.Username = '" + Username + "'";
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			int Vittorie = 0;
			
			ResultSet Vittorielist = stmt.executeQuery(select);
			
			while (Vittorielist.next())
			{
				Vittorie = Vittorielist.getInt("Vittorie");
				// PER TUTTI I CAMPI
			}
			return Vittorie;
		}
		catch(SQLException sqle)
		{
			System.out.println("SELECT ERROR");
			System.out.println(select);
			throw new SQLException(sqle.getErrorCode() + ":" + sqle.getMessage());
			
		}
		catch(Exception err)
		{
			System.out.println("GENERIC ERROR");
			throw new SQLException(err.getMessage());
		}
		finally
		{
			if (stmt != null)
			{
				stmt.close();
			}
			if (conn != null)
			{
				conn.close();
			}
		}
	}

	
	public ArrayList<UtentiBean> selectAmici(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = 
				"SELECT Utenti.Username, Accesso.Disconnessione AS UltimoAccesso" +
				"FROM (((Amicizia AS A1 INNER JOIN Utenti ON A1.IDFUtenteRichiedente = Utenti.IDUtente)" +
					"INNER JOIN Amicizia ON Amicizia.IDFUtenteRicevente = Utenti.IDUtente)" +
					"INNER JOIN Accesso ON Utenti.IDUtente = Accesso.IDFUtente)" +
					"WHERE Utenti.Username =" + Username;
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet utentiList = stmt.executeQuery(select);
			
			ArrayList<UtentiBean> utentiArray = new ArrayList<UtentiBean>();
			while (utentiList.next())
			{
				UtentiBean Utenti = new UtentiBean();
				Utenti.setEmail(utentiList.getString("Email"));
				Utenti.setPassword(utentiList.getString("Password"));
				Utenti.setUsername(utentiList.getString("Username"));
				Utenti.setFotoProfilo(utentiList.getString("FotoProfilo"));
				Utenti.setDataNascita(utentiList.getDate("DataNascita"));
				Utenti.setDisconnessione(utentiList.getDate("Disconnessione"));
				// PER TUTTI I CAMPI
				
				utentiArray.add(Utenti);
			}
			return utentiArray;
		}
		catch(SQLException sqle)
		{
			System.out.println("SELECT ERROR");
			System.out.println(select);
			throw new SQLException(sqle.getErrorCode() + ":" + sqle.getMessage());
			
		}
		catch(Exception err)
		{
			System.out.println("GENERIC ERROR");
			throw new SQLException(err.getMessage());
		}
		finally
		{
			if (stmt != null)
			{
				stmt.close();
			}
			if (conn != null)
			{
				conn.close();
			}
		}
	}
	
	


}