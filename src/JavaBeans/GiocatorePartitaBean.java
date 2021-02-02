package JavaBeans;

public class GiocatorePartitaBean {

	private UtentiBean idfUtente;    
	private PartitaBean idfPartita; 
	private int NumeroGiocatore;

    // Costruttore senza argomenti
    public GiocatorePartitaBean() { }

	

	public UtentiBean getIdfUtente() {
		return idfUtente;
	}


	public void setIdfUtente(UtentiBean idfUtente) {
		this.idfUtente = idfUtente;
	}


	public PartitaBean getIdfPartita() {
		return idfPartita;
	}


	public void setIdfPartita(PartitaBean idfPartita) {
		this.idfPartita = idfPartita;
	}



	public int getNumeroGiocatore() {
		return NumeroGiocatore;
	}

	public void setNumeroGiocatore(int numeroGiocatore) {
		NumeroGiocatore = numeroGiocatore;
	}
}
