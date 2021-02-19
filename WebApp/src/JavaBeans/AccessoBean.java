package JavaBeans;
import java.util.Date;
public class AccessoBean{
    
	private UtentiBean idfUtente;    
    private Date Connessione = new Date();
    private Date Disconnessione = new Date();

    // Costruttore senza argomenti
    public AccessoBean() { }
	

	public UtentiBean getIdfUtente() {
		return idfUtente;
	}

	public void setIdfUtente(UtentiBean idfUtente) {
		this.idfUtente = idfUtente;
	}

	public Date getConnessione() {
		return Connessione;
	}

	public void setConnessione(Date connessione) {
		Connessione = connessione;
	}

	public Date getDisconnessione() {
		return Disconnessione;
	}

	public void setDisconnessione(Date disconnessione) {
		Disconnessione = disconnessione;
	}
}