package JavaBeans;

import java.util.ArrayList;
import java.util.Date;
public class PartitaBean {
    
	private ArrayList<RoundBean> Round;
	private ArrayList<GiocatorePartitaBean> Giocatore;
	private Date DataPartita = new Date(); 

    // Costruttore senza argomenti
    public PartitaBean() {
    	setRound(new ArrayList<RoundBean>());
    	setGiocatore(new ArrayList<GiocatorePartitaBean>());
    }

	public ArrayList<RoundBean> getRound() {
		return Round;
	}

	public void setRound(ArrayList<RoundBean> round) {
		Round = round;
	}

	public ArrayList<GiocatorePartitaBean> getGiocatore() {
		return Giocatore;
	}

	public void setGiocatore(ArrayList<GiocatorePartitaBean> giocatore) {
		Giocatore = giocatore;
	}

	public Date getDataPartita() {
		return this.DataPartita;
	}

	public void setDataPartita(Date dataPartita) {
		this.DataPartita = dataPartita;
	}
}