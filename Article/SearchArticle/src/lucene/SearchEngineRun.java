package lucene;
  
public class SearchEngineRun {  
    public static void main(String[] args) throws Exception {
    	ArticleLucene lucene = new ArticleLucene();
    	lucene.importArticle("E://file/knowledge/lucene/input/5/article");
    	lucene.constructIndexer("E://file/knowledge/lucene/index/5");
    	lucene.searchingQuery("E://file/knowledge/lucene/index/5", 
    			"E://file/knowledge/lucene/output/5/queryresult");
    }
}