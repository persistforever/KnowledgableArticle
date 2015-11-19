package lucene;
  
public class SearchEngineRun {  
    public static void main(String[] args) throws Exception {
    	ArticleLucene lucene = new ArticleLucene();
    	// lucene.constructIndexer();
    	lucene.searchingQuery("¹ÉÆ±");
    }
}