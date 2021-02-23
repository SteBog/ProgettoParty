package JavaBeans;

import java.util.Date;
public class UtentiBean {
    
    private String Email;
    private String Password;
    private String Username;
    private String FotoProfilo;
    private Date DataNascita = new Date();
    

    // Costruttore senza argomenti
    public UtentiBean() { }

    
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

	public Date getDataNascita() {
		return DataNascita;
	}

	public void setDataNascita(Date dataNascita) {
		DataNascita = dataNascita;
	}
	
	
}