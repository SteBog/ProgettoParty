package JavaBeans;

import java.util.Date;

public class AmiciziaBean {

	private int idUtenteRichiedente;    
	private int idUtenteRicevente; 
    private Date DataAmicizia = new Date();

    // Costruttore senza argomenti
    public AmiciziaBean() { }

	public int getIdUtenteRichiedente() {
		return idUtenteRichiedente;
	}

	public void setIdUtenteRichiedente(int idUtenteRichiedente) {
		this.idUtenteRichiedente = idUtenteRichiedente;
	}

	public int getIdUtenteRicevente() {
		return idUtenteRicevente;
	}

	public void setIdUtenteRicevente(int idUtenteRicevente) {
		this.idUtenteRicevente = idUtenteRicevente;
	}

	public Date getDataAmicizia() {
		return DataAmicizia;
	}

	public void setDataAmicizia(Date dataAmicizia) {
		DataAmicizia = dataAmicizia;
	}


}
