package lucene;
import java.io.File;
import java.io.IOException;  

import org.apache.lucene.analysis.Analyzer;  
import org.apache.lucene.analysis.standard.StandardAnalyzer;  
import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryParser.ParseException;  
import org.apache.lucene.queryParser.QueryParser;  
import org.apache.lucene.search.IndexSearcher;  
import org.apache.lucene.search.Query;  
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
  
public class TestQuery {  
    public static void main(String[] args) throws IOException, ParseException {  
    	String index = "E://file/knowledgable/lucene/output";         //����������·��
        IndexReader reader = IndexReader.open(FSDirectory.open(new File(index)));
        IndexSearcher searcher = new IndexSearcher(reader);  
        
    	ScoreDoc[] hits = null;  
        String queryString = "��Ʊ";   //�����Ĺؼ���
        Query query = null;  
        
  
        Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_36);  
        try {  
            QueryParser qp = new QueryParser(Version.LUCENE_36,"body", analyzer);  
            query = qp.parse(queryString);  
        } catch (ParseException e) {  
        }  
        if (searcher != null) {  
            TopDocs results = searcher.search(query,10);    //�������Ϊ10����¼
            hits = results.scoreDocs;
            if (hits.length > 0) {  
                System.out.println("�ҵ�:" + hits.length + " �����!");  
            }  // ��ʾ��¼  
            for (ScoreDoc sr : hits)  
            {
		         // �ĵ����  
		         int docID = sr.doc;  
		         // ����������  
		         Document doc = searcher.doc(docID);  
		         System.out.println("url = " + doc.get("url"));
		         System.out.println("title = " + doc.get("body"));
            }  
            searcher.close();
        } 
       
    }  
  
}  