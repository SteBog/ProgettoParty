package JavaBeans;

import java.util.ArrayList;
import java.util.Date;
public class PartitaBean {
    
	private ArrayList<RoundBean> Round;
	private ArrayList<GiocatorePartitaBean> Vincitore;
	private Date DataPartita = new Date(); 

    // Costruttore senza argomenti
    public PartitaBean() {
    	setRound(new ArrayList<RoundBean>());
    	setVincitore(new ArrayList<GiocatorePartitaBean>());
    }

	public ArrayList<RoundBean> getRound() {
		return Round;
	}

	public void setRound(ArrayList<RoundBean> round) {
		Round = round;
	}

	public ArrayList<GiocatorePartitaBean> getVincitore() {
		return Vincitore;
	}

	public void setVincitore(ArrayList<GiocatorePartitaBean> vincitore) {
		Vincitore = vincitore;
	}

	public Date getDataPartita() {
		return this.DataPartita;
	}

	public void setDataPartita(Date dataPartita) {
		this.DataPartita = dataPartita;
	}
}