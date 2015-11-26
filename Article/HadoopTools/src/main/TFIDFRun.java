package main;

import java.io.IOException;

import tfidf.IDF;
import tfidf.TFIDF;

public class TFIDFRun {
	String datapath = "";
	String idfpath = "";
	String length = "";
	String tfidfpath = "";
	String wordpath = "";
	
	public TFIDFRun(String datapath, String idfpath, String length, String tfidfpath, String wordpath) {
		this.datapath = datapath;
		this.idfpath = idfpath;
		this.length = length;
		this.tfidfpath = tfidfpath;
		this.wordpath = wordpath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String datapath = args[0];
		String idfpath = args[1];
		String length = args[2];
		String tfidfpath = args[3];
		String wordpath = args[4];
		TFIDFRun idfRun = new TFIDFRun(datapath, idfpath, length, tfidfpath, wordpath);
		idfRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		
		System.out.println("============ calculate IDF value ===============");
		IDF idf = new IDF(this.datapath, this.idfpath, this.length, this.wordpath);
		idf.run();
		
		System.out.println("============ calculate TFIDF value ===============");
		TFIDF tfidf = new TFIDF(this.datapath, this.idfpath, this.tfidfpath);
		tfidf.run();
	}
}