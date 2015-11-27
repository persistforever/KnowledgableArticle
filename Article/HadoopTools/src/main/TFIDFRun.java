package main;

import java.io.IOException;

import tfidf.IDF;
import tfidf.TFIDF;

public class TFIDFRun {
	String dataPath = "";
	String idfPath = "";
	String length = "";
	String tfidfPath = "";
	String stopWordPath = "";
	String wordSetPath = "";
	
	public TFIDFRun(String dataPath, String idfPath, String length, String tfidfPath, 
			String stopWordPath, String wordSetPath) {
		this.dataPath = dataPath;
		this.idfPath = idfPath;
		this.length = length;
		this.tfidfPath = tfidfPath;
		this.stopWordPath = stopWordPath;
		this.wordSetPath = wordSetPath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String dataPath = args[0];
		String idfPath = args[1];
		String length = args[2];
		String tfidfPath = args[3];
		String stopWordPath = args[4];
		String wordSetPath = args[5];
		TFIDFRun idfRun = new TFIDFRun(dataPath, idfPath, length, tfidfPath, 
				stopWordPath, wordSetPath);
		idfRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		
		System.out.println("============ calculate IDF value ===============");
		IDF idf = new IDF(this.dataPath, this.idfPath, this.length, 
				this.stopWordPath, this.wordSetPath);
		idf.run();
		
		System.out.println("============ calculate TFIDF value ===============");
		TFIDF tfidf = new TFIDF(this.dataPath, this.idfPath, this.tfidfPath);
		tfidf.run();
	}
}