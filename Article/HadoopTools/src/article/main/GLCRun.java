package article.main;

import java.io.IOException;

import article.gzh_follownum.GLC;


public class GLCRun {
	String dataPath = "";
	String gzhPath = "";
	String gacPath = "";
	String userThreshold = "";
	String articleThreshold = "";
	
	public GLCRun(String dataPath, String gzhPath, String gacPath, 
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
		GLCRun glcRun = new GLCRun(dataPath, gzhPath, gacPath, 
				userThreshold, articleThreshold);
		glcRun.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("============ calculate article average collect number ===============");
		GLC glc = new GLC(this.dataPath, this.gzhPath, this.gacPath, 
				this.userThreshold, this.articleThreshold);
		glc.run();
	}
}