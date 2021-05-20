package classi;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import JavaBeans.*;

public class DBManagement {
	
	//Parametri di accesso al database
	/*private static final String DB_DRIVER = "com.mysql.jdbc.Driver";	// com.mysql.cj.jdbc.Driver
	private static final String DB_CONNECTION = "jdbc:mysql://87.250.73.23:3306/Party";	// 12320*/
	// Accesso crittografato (TLS)
	private static final String DB_DRIVER = "com.mysql.cj.jdbc.Driver";	// com.mysql.cj.jdbc.Driver
	private static final String DB_CONNECTION = "jdbc:mysql://87.250.73.23:3306/Party?SSLProtocol=TLSv1.2";
	
	private static final String DB_USER = "adminer";
	private static final String DB_PASSWORD = "CBC349aa";
	

/*	//Parametri di accesso al database locale
	private static final String DB_DRIVER = "com.mysql.jdbc.Driver";	// com.mysql.cj.jdbc.Driver
	private static final String DB_CONNECTION = "jdbc:mysql://localhost/Party";	// 12320
	private static final String DB_USER = "root";
	private static final String DB_PASSWORD = "";
*/
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
				//Utenti.setDisconnessione(utentiList.getDate("Disconnessione"));
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

	
	public ArrayList<UtentiBean> selectAmici(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
	
		//String select = "SELECT U2.Username FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U1.Username ='" + Username + "';";
		String select = "SELECT U2.Username, U2.FotoProfilo FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U1.Username ='" + Username + "' AND U2.Username != '" + Username + "' AND Amicizia.DataAmicizia IS NOT NULL UNION SELECT U1.Username, U1.FotoProfilo FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U2.Username ='" + Username + "' AND U1.Username != '" + Username + "' AND Amicizia.DataAmicizia IS NOT NULL";
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
				//Utenti.setDisconnessione(utentiList.getDate("UltimoAccesso"));
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
	
	public ArrayList<UtentiBean> selectRichiesteAmico(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
	
		//String select = "SELECT U2.Username FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U1.Username ='" + Username + "';";
		String select = "SELECT U2.Username, U2.FotoProfilo FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U1.Username ='" + Username + "' AND U2.Username != '" + Username + "' AND Amicizia.DataAmicizia IS NULL UNION SELECT U1.Username, U1.FotoProfilo FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U2.Username ='" + Username + "' AND U1.Username != '" + Username + "' AND Amicizia.DataAmicizia IS NULL";
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
				//Utenti.setDisconnessione(utentiList.getDate("UltimoAccesso"));
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
	
	public ArrayList<UtentiBean> selectTuttiUtenti(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT Utenti.Username, Utenti.FotoProfilo FROM Utenti WHERE Utenti.Username " + 
				"NOT IN(" + 
				"SELECT U2.Username FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U1.Username ='" + Username + "' AND U2.Username != '" + Username + "' " + 
				"UNION " + 
				"SELECT U1.Username FROM ((Utenti AS U1 INNER JOIN Amicizia ON U1.IDUtente = Amicizia.IDFUtenteRichiedente) INNER JOIN Utenti AS U2 ON U2.IDUtente = Amicizia.IDFUtenteRicevente) WHERE U2.Username ='" + Username + "' AND U1.Username != '" + Username + "' " + 
				") AND Utenti.Username !='" + Username + "'";
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
				Utenti.setFotoProfilo(utentiList.getString("FotoProfilo"));
				//Utenti.setDataNascita(utentiList.getDate("DataNascita"));
				//Utenti.setDisconnessione(utentiList.getDate("UltimoAccesso"));
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
	
	public void inviaRichiestaAmico(String Username1, String Username2) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = null;
		
		query = "INSERT INTO Amicizia (Amicizia.IDFUtenteRichiedente, Amicizia.IDFUtenteRicevente) VALUES ((SELECT Utenti.IDUtente FROM Utenti WHERE Utenti.Username = '" + Username1 + "'),(SELECT Utenti.IDUtente FROM Utenti WHERE Utenti.Username = '" + Username2 + "'));";
		
		System.out.println(query);
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			
		
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
	
	public void accettaRichiestaAmico(String Username1, String Username2) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = null;
		
		query = "UPDATE Amicizia SET DataAmicizia = CURRENT_TIMESTAMP() WHERE IDFUtenteRichiedente = (SELECT Utenti.IDUtente FROM Utenti WHERE Utenti.Username = '" + Username1 + "') AND IDFUtenteRicevente = (SELECT Utenti.IDUtente FROM Utenti WHERE Utenti.Username = '" + Username2 + "');";
		
		System.out.println(query);
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			
		
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
	
	public ArrayList<qVittorieMinigiochiBean> selectVittorieMinigiochi(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT COUNT(ClassificatoRound.Posizione) AS VittorieMinigiochi, Minigioco.Nome AS Minigioco " + 
				"FROM ClassificatoRound INNER JOIN GiocatorePartita ON ClassificatoRound.IDFGiocatore = GiocatorePartita.IDGiocatorePartita " + 
				"INNER JOIN Utenti ON GiocatorePartita.IDFUtente = Utenti.IDUtente " + 
				"INNER JOIN Round ON ClassificatoRound.IDFRound = Round.IDRound " + 
				"INNER JOIN Minigioco ON Round.IDFMinigioco = Minigioco.idMinigioco " + 
				"WHERE Utenti.Username = '" + Username + "' AND ClassificatoRound.Posizione = 0 " + 
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
	
	public float selectVittorie(String Username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT COUNT(Partita.IDPartita) AS Vittorie FROM "
				+ "((Partita INNER JOIN GiocatorePartita ON Partita.IDPartita = GiocatorePartita.IDFPartita) "
				+ " INNER JOIN Utenti ON GiocatorePartita.IDFUtente = Utenti.IDUtente) "
				+ " WHERE Utenti.Username = '" + Username + "' AND GiocatorePartita.NumeroGiocatore = Partita.Vincitore";
		System.out.println(select);
		
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet vittorieList = stmt.executeQuery(select);
			float Vittorie = 0;
			if(vittorieList.next())
			{
				Vittorie = vittorieList.getFloat("Vittorie");
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
	
	public float numero_partite_giocate(String username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = "SELECT COUNT(Partita.IDPartita) AS giocate FROM "
				+ "((Partita INNER JOIN GiocatorePartita ON Partita.IDPartita = GiocatorePartita.IDFPartita) "
				+ "INNER JOIN Utenti ON GiocatorePartita.IDFUtente = Utenti.IDUtente)\n"
				+ "WHERE Utenti.Username = '" + username + "'";
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet partite_giocate_list = stmt.executeQuery(query);
			float giocate = 0;
			if(partite_giocate_list.next())
			{
				giocate = partite_giocate_list.getFloat("giocate");
			}
			return giocate;
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
	
	public int ore_giocate(String username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = "SELECT SUM(TIMEDIFF(Accessi.OraDisconnessione, Accessi.OraConnessione)) AS tempo "
				+ "FROM (Accessi INNER JOIN Utenti ON Utenti.IDUtente = Accessi.IDAccesso) "
				+ "WHERE Utenti.Username = '" + username + "'";
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet ore_giocate = stmt.executeQuery(query);
			int giocate = 0;
			if(ore_giocate.next())
			{
				giocate = ore_giocate.getInt("tempo");	//	Qua sono ancora secondi
				giocate = giocate / 3600;
			}
			return giocate;
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
	
	
	public ArrayList<MessaggioBean> selectMessaggi(String Username1, String Username2) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT Messaggio.Testo, Messaggio.Data, U1.Username " + 
				"FROM ((Utenti AS U1 INNER JOIN Messaggio ON U1.IDUtente = Messaggio.IDFMittente) " + 
				"INNER JOIN Utenti AS U2 ON U2.IDUtente = Messaggio.IDFRicevente) " + 
				"WHERE U1.Username = '" + Username1 + "' AND U2.Username = '" + Username2 + "' OR U1.Username = '" + Username2 + "' AND U2.Username = '" + Username1 + "' " +
				"ORDER BY Messaggio.Data";
		
		System.out.println(select);
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet messaggioList = stmt.executeQuery(select);
			
			ArrayList<MessaggioBean> messaggiArray = new ArrayList<MessaggioBean>();
			while (messaggioList.next())
			{
				MessaggioBean Messaggi = new MessaggioBean();
				Messaggi.setTesto(messaggioList.getString("Testo"));
				Messaggi.setData(messaggioList.getDate("Data"));
				Messaggi.setUtente(messaggioList.getString("Username"));
				
				messaggiArray.add(Messaggi);
			}
			return messaggiArray;
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
	
	public void inviaMessaggio(String Username1, String Username2, String Testo) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = null;
		
		query = "INSERT INTO Messaggio (IDFMittente, IDFRicevente, Testo, Data) VALUES" + 
				"	((SELECT IDUtente FROM Utenti WHERE Username = '" + Username1 + "')," + 
				"	(SELECT IDUtente FROM Utenti WHERE Username = '" + Username2 + "')," + 
				"'" + Testo + "'," + 
				"	current_timestamp());";
		
		System.out.println(query);
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			
		
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
	
	public ArrayList<MessaggioBean> selectUtentiMessaggi(String Username1) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String select = "SELECT U1.Username FROM ((Utenti AS U1 INNER JOIN Messaggio ON U1.IDUtente = Messaggio.IDFMittente) " + 
				"INNER JOIN Utenti AS U2 ON U2.IDUtente = Messaggio.IDFRicevente) " + 
				"WHERE U2.Username = '" + Username1 + "'" + 
				"UNION " + 
				"SELECT U2.Username " + 
				"FROM ((Utenti AS U1 INNER JOIN Messaggio ON U1.IDUtente = Messaggio.IDFMittente) " + 
				"INNER JOIN Utenti AS U2 ON U2.IDUtente = Messaggio.IDFRicevente) " + 
				"WHERE U1.Username = '" + Username1 + "'";
		
		System.out.println(select);
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			ResultSet messaggioList = stmt.executeQuery(select);
			
			ArrayList<MessaggioBean> messaggiArray = new ArrayList<MessaggioBean>();
			while (messaggioList.next())
			{
				MessaggioBean Messaggi = new MessaggioBean();
				//Messaggi.setTesto(messaggioList.getString("Testo"));
				//Messaggi.setData(messaggioList.getDate("Data"));
				Messaggi.setUtente(messaggioList.getString("Username"));
				
				messaggiArray.add(Messaggi);
			}
			return messaggiArray;
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
	public void aggiorna_utente (UtentiBean utente, String username) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		Date data_nascita = utente.getDataNascita();
		SimpleDateFormat sdf = new SimpleDateFormat();
		sdf.applyPattern("yyyy-MM-dd");
		String stringa_data_nascita = sdf.format(data_nascita);
		
		String password = utente.getPassword();
		String query = null;
		
		if (password == null || password == "")
		{
			query = "UPDATE Utenti SET Utenti.Email = '" + utente.getEmail() + "' , Utenti.Username = '" + utente.getUsername() + "', " + 
					"Utenti.DataNascita = '" + stringa_data_nascita + "' WHERE Utenti.Username = '" + username + "'";
		}
		else
		{
			query = "UPDATE Utenti SET Utenti.Email = '" + utente.getEmail() + "' , Utenti.Password = '" + password + "', Utenti.Username = '" + utente.getUsername() + "', " + 
					"Utenti.DataNascita = '" + stringa_data_nascita + "' WHERE Utenti.Username = '" + username + "'";
		}
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			
		
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
	public void aggiorna_immagine_utente (String nome_immagine, String utente) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = "UPDATE Utenti SET Utenti.FotoProfilo = '" + nome_immagine + "' WHERE Utenti.Username = '" + utente + "'";
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			
		
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
	
	public void Registrazione(String Username, String Password, String Email, String DataNascita) throws SQLException
	{
		Statement stmt = null;
		Connection conn = null;
		
		String query = null;
		
		query = "INSERT INTO `Utenti`(`Email`, `Password`, `Username`, `FotoProfilo`, `DataNascita`) VALUES ('"+Email+"','"+Password+"','"+Username+"', 1 ,'"+DataNascita+"')";
		
		System.out.println(query);
		
		try
		{
			conn = getDBConnection();
			stmt = conn.createStatement();
			
			
		
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