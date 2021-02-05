package JavaBeans;

import java.util.ArrayList;

public class MinigiocoBean {
    
private ArrayList<RoundBean> Round;
private String Nome;
private String Mappa;
private int Coppie;
private String Descrizione;



    // Costruttore senza argomenti
    public MinigiocoBean() {
    	setRound(new ArrayList<RoundBean>());
    }

	

	public ArrayList<RoundBean> getRound() {
		return Round;
	}



	public void setRound(ArrayList<RoundBean> round) {
		Round = round;
	}



	public String getNome() {
		return this.Nome;
	}

	public void setNome(String nome) {
		this.Nome = nome;
	}

	public String getMappa() {
		return this.Mappa;
	}

	public void setMappa(String mappa) {
		this.Mappa = mappa;
	}

	public int getCoppie() {
		return this.Coppie;
	}

	public void setCoppie(int coppie) {
		this.Coppie = coppie;
	}

	public String getDescrizione() {
		return this.Descrizione;
	}

	public void setDescrizione(String descrizione) {
		this.Descrizione = descrizione;
	}
    
}