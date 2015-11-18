package main;

import java.io.IOException;

import bow.BOW;


public class BOWRun {
	String datapath = "";
	String wordpath = "";
	String bowpath = "";
	
	public BOWRun(String datapath, String wordpath, String bowpath) {
		this.datapath = datapath;
		this.wordpath = wordpath;
		this.bowpath = bowpath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String datapath = args[0];
		String wordpath = args[1];
		String bowpath = args[2];
		BOWRun idfRun = new BOWRun(datapath, wordpath, bowpath);
		idfRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("============ construct article bag of word ===============");
		BOW bow = new BOW(this.datapath, this.wordpath, this.bowpath);
		bow.run();
	}
}