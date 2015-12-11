package lucene;
  
public class SearchEngineRun {  
    public static void main(String[] args) throws Exception {
    	ArticleLucene lucene = new ArticleLucene();
    	//lucene.importArticle("E://data/knowledge/lucene/input/fashion/unique_article");
    	//lucene.constructIndexer("E://data/knowledge/lucene/index/5");
    	lucene.searchingQuery("E://data/knowledge/lucene/index/5", 
    			"E://data/knowledge/lucene/output/fashion/queryresult");
    }
}