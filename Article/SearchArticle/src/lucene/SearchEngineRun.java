package lucene;
  
public class SearchEngineRun {  
    public static void main(String[] args) throws Exception {
    	ArticleLucene lucene = new ArticleLucene();
    	lucene.importArticle("E://file/knowledge/lucene/input/5/article");
    	// lucene.constructIndexer();
    	// lucene.searchingQuery();
    }
}