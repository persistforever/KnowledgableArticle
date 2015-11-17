package lucene;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.queryParser.MultiFieldQueryParser;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import tools.Article;
import tools.FileOperator;

public class ArticleLucene {
	/* attributes */
	ArrayList<Article> artlist = new ArrayList<Article>();
    File fileDir = new File("E://file/knowledgable/lucene/input/4");
    File indexDir = new File("E://file/knowledgable/lucene/index"); 
    File outputDir = new File("E://file/knowledgable/lucene/output/queryresult.csv"); 
	
	/* methods */
    public ArticleLucene() throws IOException {
    	this.importArticle();
    }
    
    /* import methods */
	public void importArticle() throws IOException {
        File[] textFiles = this.fileDir.listFiles();
        for (int i = 0; i < textFiles.length; i++) {  
            if (textFiles[i].isFile()) {
                ArrayList<Article> subartlist = FileOperator.ArticleFileReader(
                		textFiles[i].getCanonicalPath(), "GB18030"); 
                for(Article article: subartlist) {
                	this.artlist.add(article);
                }
            }
        }
        System.out.println("importing article finished ...");
	}

    /* process methods */
	public void constructIndexer() throws IOException {
        Directory dir = FSDirectory.open(indexDir);
        Analyzer luceneAnalyzer = new StandardAnalyzer(Version.LUCENE_36);
        IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_36,luceneAnalyzer);
        iwc.setOpenMode(OpenMode.CREATE);
        IndexWriter indexWriter = new IndexWriter(dir,iwc);
        for (Article article: this.artlist) {
            Document document = new Document();
            Field idfield = new Field("id", article.id, Field.Store.YES, Field.Index.NO);  
            Field urlfield = new Field("url", article.url, Field.Store.YES, Field.Index.NO);   
            Field cpltlfield = new Field("cpltitle", article.completetitle, Field.Store.YES, Field.Index.NO);
            Field contentfield = new Field("content", article.content, Field.Store.YES, 
            		Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS);  
            document.add(idfield); 
            document.add(urlfield);
            document.add(cpltlfield);
            document.add(contentfield);
            indexWriter.addDocument(document);
        }
        indexWriter.close();
        System.out.println("constructing indexer finished ...");
	}
	
    public void searchingQuery(String querystring) 
    		throws CorruptIndexException, IOException {
    	IndexReader reader = IndexReader.open(FSDirectory.open(this.indexDir));
        IndexSearcher searcher = new IndexSearcher(reader);  
    	ScoreDoc[] hits = null;
        Query query = null;
        Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_36);  
        ArrayList<Article> resultlist = new ArrayList<Article>();
        try {
        	String[] fields = {"cpltitle", "content"};
        	QueryParser qp = new MultiFieldQueryParser(Version.LUCENE_36, fields, analyzer);
            query = qp.parse(querystring);  
        } catch (ParseException e) {  
        }  
        if (searcher != null) {  
            TopDocs results = searcher.search(query, 10);
            hits = results.scoreDocs;
            if (hits.length > 0) { 
                System.out.println("找到:" + hits.length + " 个结果!");
                for (ScoreDoc sr : hits)  
                {
    		         int docID = sr.doc;
    		         Document doc = searcher.doc(docID); 
    		         ArrayList<String> attributeslist = new ArrayList<String>();
    		         attributeslist.add(doc.get("id").toString());
    		         attributeslist.add(doc.get("url").toString());
    		         attributeslist.add(doc.get("cpltitle").toString());
    		         attributeslist.add(doc.get("content").toString());
    		         resultlist.add(new Article(attributeslist));
                }    
            }
            searcher.close();
        }
        FileOperator.ArticleCSVWriter(this.outputDir.getPath(), resultlist, "gb18030");
    }
}
