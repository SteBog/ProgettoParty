package classi;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import JavaBeans.*;

public class DBManagement {
	
	//Parametri di accesso al database
	private static final String DB_DRIVER = "com.mysql.jdbc.Driver";	// com.mysql.cj.jdbc.Driver
	private static final String DB_CONNECTION = "jdbc:mysql://87.250.73.23:3306/Party";	// 12320
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
		
		String select = "SELECT U2.Username, U2.Disconnessione AS UltimoAccesso FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U1.Username ='" + Username + "';";
		System.out.println(select);
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet utentiList = stmt.executeQuery(select);
			
			ArrayList<UtentiBean> utentiArray = new ArrayList<UtentiBean>();
			while (utentiList.next())
			{
				UtentiBean Utenti = new UtentiBean();
				//Utenti.setEmail(utentiList.getString("Email"));
				//Utenti.setPassword(utentiList.getString("Password"));
				Utenti.setUsername(utentiList.getString("Username"));
				//Utenti.setFotoProfilo(utentiList.getString("FotoProfilo"));
				//Utenti.setDataNascita(utentiList.getDate("DataNascita"));
				Utenti.setDisconnessione(utentiList.getDate("UltimoAccesso"));
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
	
	
	public ArrayList<qVittorieMinigiochiBean> selectVittorieMinigiochi(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT COUNT(ClassificatoRound.Posizione) AS VittorieMinigiochi, Minigioco.Nome AS Minigioco " + 
				"FROM ((((ClassificatoRound INNER JOIN Round ON ClassificatoRound.IDFRound = Round.IDRound) " + 
				"INNER JOIN Minigioco ON Round.IDFMinigioco = Minigioco.IDMinigioco) " + 
				"INNER JOIN GiocatorePartita ON ClassificatoRound.IDFGiocatore = GiocatorePartita.IDFUtente) " + 
				"INNER JOIN Utenti ON GiocatorePartita.IDFUtente = Utenti.IDUtente) " + 
				"WHERE Utenti.Username = '" + Username + "' AND ClassificatoRound.Posizione = 1 " + 
				"GROUP BY Minigioco.Nome";
		
		System.out.println(select);
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet vittorieMinigiochiList = stmt.executeQuery(select);
			
			ArrayList<qVittorieMinigiochiBean> vittorieArray = new ArrayList<qVittorieMinigiochiBean>();
			while (vittorieMinigiochiList.next())
			{
				qVittorieMinigiochiBean Vittorie = new qVittorieMinigiochiBean();
				Vittorie.setVittorieMinigiochi(vittorieMinigiochiList.getInt("VittorieMinigiochi"));
				Vittorie.setMinigioco(vittorieMinigiochiList.getString("Minigioco"));
				// PER TUTTI I CAMPI
				
				vittorieArray.add(Vittorie);
			}
			return vittorieArray;
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
	
	public int selectVittorie(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT COUNT(Partita.Vincitore) AS Vittorie " + 
				"FROM (Partita INNER JOIN Utenti ON Partita.Vincitore = Utenti.IDUtente) " + 
				"WHERE Utenti.Username = '" + Username + "';";
		
		System.out.println(select);
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet vittorieList = stmt.executeQuery(select);
			int Vittorie = 0;
			if(vittorieList.next())
			{
				Vittorie = vittorieList.getInt("Vittorie");
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
	
	public ArrayList<UtentiBean> ottieni_dati_utente(String username) throws SQLException
	{
		Connection conn = null;
		Statement stmt = null;
		
		String query = "SELECT Utenti.IDUtente, Utenti.Email, Utenti.Username, Utenti.FotoProfilo, Utenti.DataNascita "
				+ "FROM Utenti WHERE Utenti.Username = '" + username + "'";
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet risultato = stmt.executeQuery(query);
			ArrayList<UtentiBean> array_utenti = new ArrayList<UtentiBean>();
			
			while (risultato.next())
			{
				UtentiBean utente = new UtentiBean();
				utente.setID(risultato.getInt("IDUtente"));
				utente.setEmail(risultato.getString("Email"));
				utente.setUsername(risultato.getNString("Username"));
				utente.setFotoProfilo(risultato.getString("FotoProfilo"));
				utente.setDataNascita(risultato.getDate("DataNascita"));
				//	I dati una volta creata la tabella accesso
				
				array_utenti.add(utente);
			}
			
			return array_utenti;
		}
		catch(SQLException e)
		{
			System.out.println(e);
		}
		catch (Exception e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
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
		
		return null;
	}
	public void aggiorna_utente (UtentiBean utente) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			String query = "UPDATE Utenti SET Utenti.Email = '" + utente.getEmail() + "' , Utenti.Username = '" + utente.getUsername() + "', Utenti.FotoProfilo = '" + utente.getFotoProfilo() + "', Utenti.DataNascita = '" + utente.getDataNascita() + "'"
					+ " WHERE Utenti.IDUtente = " + utente.getID();
		
			stmt.executeUpdate(query);
		}
		catch(SQLException sqle)
		{
			System.out.println("UPDATE ERROR");
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