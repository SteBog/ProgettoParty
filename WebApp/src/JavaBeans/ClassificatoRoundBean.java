package JavaBeans;

public class ClassificatoRoundBean {

	private RoundBean idfRound;
	private GiocatorePartitaBean idfGiocatore;
	private int Posizione;
	
	// Costruttore senza argomenti
	public ClassificatoRoundBean() {}

	public RoundBean getIdfRound() {
		return idfRound;
	}

	public void setIdfRound(RoundBean idfRound) {
		this.idfRound = idfRound;
	}

	public GiocatorePartitaBean getIdfGiocatore() {
		return idfGiocatore;
	}

	public void setIdfGiocatore(GiocatorePartitaBean idfGiocatore) {
		this.idfGiocatore = idfGiocatore;
	}

	public int getPosizione() {
		return Posizione;
	}

	public void setPosizione(int posizione) {
		Posizione = posizione;
	}
	

}
