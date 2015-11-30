package main;

import java.io.IOException;
import java.util.ArrayList;

import tools.Article;
import tools.FileOperator;
import lucene.ArticleLucene;

public class ArticleUnique {
	String articlePath = "";
	String uniquePath = "";
	
	public ArticleUnique(String articlePath, String uniquePath) {
		this.articlePath = articlePath;
		this.uniquePath = uniquePath;
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException, InterruptedException {
		String articlePath = args[0];
		String uniquePath = args[1];
		ArticleUnique article = new ArticleUnique(articlePath, uniquePath);
		article.run();
	}
	
	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out.println("start");
    	ArticleLucene lucene = new ArticleLucene();
    	ArrayList<Article> artlist = lucene.importArticle(this.articlePath);
    	artlist = lucene.uniqueResult(artlist);
    	FileOperator.ArticleTextWriter(this.uniquePath, artlist, "gb18030");
		System.out.println("end");
	}
}