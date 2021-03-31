package JavaBeans;

import java.util.Date;

public class MessaggioBean {

	public MessaggioBean() {}
	

	private int idfMittente;    
	private int idfDestinatario; 
	private String Testo;
    private Date Data = new Date();
    
    
    public int getIdfMittente() {
		return idfMittente;
	}
	public void setIdfMittente(int idfMittente) {
		this.idfMittente = idfMittente;
	}
	public int getIdfDestinatario() {
		return idfDestinatario;
	}
	public void setIdfDestinatario(int idfDestinatario) {
		this.idfDestinatario = idfDestinatario;
	}
	public String getTesto() {
		return Testo;
	}
	public void setTesto(String testo) {
		Testo = testo;
	}
	public Date getData() {
		return Data;
	}
	public void setData(Date data) {
		Data = data;
	}
}
