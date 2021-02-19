

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
	private static final String DB_CONNECTION = "jdbc:mysql://localhost:3306/Party";
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
	
	public ArrayList<UtentiBean> selectUtenti() throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			String select = "SELECT * FROM Utenti";
			ResultSet utentiList = stmt.executeQuery(select);
			
			ArrayList<UtentiBean> utentiArray = new ArrayList<UtentiBean>();
			while (utentiList.next())
			{
				UtentiBean Utenti = new UtentiBean();
				Utenti.setUsername(utentiList.getString("Nome"));
				Utenti.setUsername(utentiList.getString("Cognome"));
				Utenti.setUsername(utentiList.getString("Email"));
				Utenti.setUsername(utentiList.getString("Password"));
				Utenti.setUsername(utentiList.getString("Username"));
				Utenti.setUsername(utentiList.getString("FotoProfilo"));
				Utenti.setUsername(utentiList.getString("Nazionalita"));
				Utenti.setPassword(utentiList.getString("DataNascita"));
				// PER TUTTI I CAMPI
				
				utentiArray.add(Utenti);
			}
			return utentiArray;
		}
		catch(SQLException sqle)
		{
			System.out.println("SELECT ERROR");
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