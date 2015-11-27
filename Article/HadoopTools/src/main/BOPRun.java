package main;

import java.io.IOException;

import bop.BOP;


public class BOPRun {
	String datapath = "";
	String pospath = "";
	String boppath = "";
	
	public BOPRun(String datapath, String pospath, String boppath) {
		this.datapath = datapath;
		this.pospath = pospath;
		this.boppath = boppath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String datapath = args[0];
		String pospath = args[1];
		String boppath = args[2];
		BOPRun idfRun = new BOPRun(datapath, pospath, boppath);
		idfRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("============ construct article bag of word ===============");
		BOP bop = new BOP(this.datapath, this.pospath, this.boppath);
		bop.run();
	}
}