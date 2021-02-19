package JavaBeans;

import java.util.ArrayList;

public class RoundBean {

	private ArrayList<ClassificatoRoundBean> Classificato;
	private MinigiocoBean idfMinigioco; 
	private PartitaBean idfPartita; 
	

	// Costruttore senza argomenti
	public RoundBean() {
		setClassificato(new ArrayList<ClassificatoRoundBean>());
	}


	public ArrayList<ClassificatoRoundBean> getClassificato() {
		return Classificato;
	}


	public void setClassificato(ArrayList<ClassificatoRoundBean> classificato) {
		Classificato = classificato;
	}


	public MinigiocoBean getIdfMinigioco() {
		return idfMinigioco;
	}



	public void setIdfMinigioco(MinigiocoBean idfMinigioco) {
		this.idfMinigioco = idfMinigioco;
	}



	public PartitaBean getIdfPartita() {
		return idfPartita;
	}



	public void setIdfPartita(PartitaBean idfPartita) {
		this.idfPartita = idfPartita;
	}

	
	
}
