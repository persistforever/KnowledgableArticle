package main;

import java.io.IOException;
import lucene.ArticleLucene;

public class SearchRun {
	String articlePath = "";
	String indexPath = "";
	String resultPath = "";
	
	public SearchRun(String articlePath, String indexPath, String resultPath) {
		this.articlePath = articlePath;
		this.indexPath = indexPath;
		this.resultPath = resultPath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String articlePath = args[0];
		String indexPath = args[1];
		String resultPath = args[1];
		SearchRun article = new SearchRun(articlePath, indexPath, resultPath);
		article.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("start");
    	ArticleLucene lucene = new ArticleLucene();
    	lucene.importArticle(this.articlePath);
    	// lucene.constructIndexer(this.indexPath);
    	lucene.searchingQuery(this.indexPath, this.resultPath);
		System.out.println("end");
	}
}