package JavaBeans;

import java.util.Date;
public class UtentiBean {
    
    private String Nome;
    private String Cognome;
    private String Email;
    private String Password;
    private String Username;
    private String FotoProfilo;
    private String Nazionalita;
    private Date DataNascita = new Date();
    

    // Costruttore senza argomenti
    public UtentiBean() { }

    
    public String getNome() {
        return this.Nome;
    }
    public void setNome(String nome) {
        this.Nome = nome;
    }
    
    public String getCognome() {
        return this.Cognome;
    }
    public void setCognome(String cognome) {
        this.Cognome = cognome;
    }

	public String getEmail() {
		return this.Email;
	}

	public void setEmail(String email) {
		this.Email = email;
	}

	public String getPassword() {
		return this.Password;
	}

	public void setPassword(String password) {
		this.Password = password;
	}

	public String getUsername() {
		return this.Username;
	}

	public void setUsername(String username) {
		this.Username = username;
	}

	public String getFotoProfilo() {
		return this.FotoProfilo;
	}

	public void setFotoProfilo(String fotoProfilo) {
		this.FotoProfilo = fotoProfilo;
	}

	public String getNazionalita() {
		return this.Nazionalita;
	}

	public void setNazionalita(String nazionalita) {
		this.Nazionalita = nazionalita;
	}

	public Date getDataNascita() {
		return DataNascita;
	}

	public void setDataNascita(Date dataNascita) {
		DataNascita = dataNascita;
	}
	
	
}