package article.main;

import java.io.IOException;

import article.article_collectnum.AC;


public class ACRun {
	String dataPath = "";
	String acPath = "";
	
	public ACRun(String dataPath, String acPath) {
		this.dataPath = dataPath;
		this.acPath = acPath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String dataPath = args[0];
		String acPath = args[1];
		ACRun acRun = new ACRun(dataPath, acPath);
		acRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("============ calculate article average collect number ===============");
		AC ac = new AC(this.dataPath, this.acPath);
		ac.run();
	}
}