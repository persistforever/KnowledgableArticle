package article.main;

import java.io.IOException;

import article.collect_click_rate.CCR;


public class CCRRun {
	String dataPath = "";
	String ccrPath = "";
	
	public CCRRun(String dataPath, String acPath) {
		this.dataPath = dataPath;
		this.ccrPath = acPath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String dataPath = args[0];
		String acPath = args[1];
		CCRRun acRun = new CCRRun(dataPath, acPath);
		acRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("============ calculate article average collect number ===============");
		CCR ac = new CCR(this.dataPath, this.ccrPath);
		ac.run();
	}
}