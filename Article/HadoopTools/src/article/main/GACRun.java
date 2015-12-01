package article.main;

import java.io.IOException;

import article.gzh_avg_collectnum.GAC;


public class GACRun {
	String dataPath = "";
	String gzhPath = "";
	String gacPath = "";
	String userThreshold = "";
	String articleThreshold = "";
	
	public GACRun(String dataPath, String gzhPath, String gacPath, 
			String userThreshold, String articleThreshold) {
		this.dataPath = dataPath;
		this.gzhPath = gzhPath;
		this.gacPath = gacPath;
		this.userThreshold = userThreshold;
		this.articleThreshold = articleThreshold;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String dataPath = args[0];
		String gzhPath = args[1];
		String gacPath = args[2];
		String userThreshold = args[3];
		String articleThreshold = args[4];
		GACRun gacRun = new GACRun(dataPath, gzhPath, gacPath, 
				userThreshold, articleThreshold);
		gacRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("============ calculate article average collect number ===============");
		GAC gac = new GAC(this.dataPath, this.gzhPath, this.gacPath, 
				this.userThreshold, this.articleThreshold);
		gac.run();
	}
}