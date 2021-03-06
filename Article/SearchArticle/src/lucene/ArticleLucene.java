package lucene;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

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
import org.apache.lucene.search.BooleanClause;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import cas.simhash.Unique;
import tools.Article;
import tools.FileOperator;

public class ArticleLucene {
	/* attributes */
	ArrayList<Article> artlist = new ArrayList<Article>(); 
	
	/* methods */
    public ArticleLucene() throws IOException {
    }
    
    /* import methods */
	public ArrayList<Article> importArticle(String inputPath) throws IOException {
        ArrayList<Article> subartlist = FileOperator.ArticleFileReader(
        		new File(inputPath).getCanonicalPath(), "GB18030"); 
        for(Article article: subartlist) {
        	this.artlist.add(article);
        }
        System.out.println(this.artlist.size());
        System.out.println("importing article finished ...");
        return this.artlist;
	}

    /* process methods */
	public void constructIndexer(String indexPath) throws IOException {
        Directory dir = FSDirectory.open(new File(indexPath));
        Analyzer luceneAnalyzer = new StandardAnalyzer(Version.LUCENE_36);
        IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_36,luceneAnalyzer);
        iwc.setOpenMode(OpenMode.CREATE);
        IndexWriter indexWriter = new IndexWriter(dir,iwc);
        for (Article article: this.artlist) {
            Document document = new Document();
            Field idfield = new Field("id", article.id, Field.Store.YES, Field.Index.NO);
            Field urlfield = new Field("url", article.url, Field.Store.YES, Field.Index.NO);
            Field titlefield = new Field("title", article.title, Field.Store.YES, 
            		Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS);  
            Field contentfield = new Field("content", article.content, Field.Store.YES, 
            		Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS);  
            document.add(idfield); 
            document.add(urlfield);
            document.add(titlefield);
            document.add(contentfield);
            indexWriter.addDocument(document);
        }
        indexWriter.close();
        System.out.println("constructing indexer finished ...");
	}
	
    public void searchingQuery(String indexPath, String resultPath) 
    		throws CorruptIndexException, IOException {
    	IndexReader reader = IndexReader.open(FSDirectory.open(new File(indexPath)));
        IndexSearcher searcher = new IndexSearcher(reader);  
    	ScoreDoc[] hits = null;
    	Query query = null;
        Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_36);  
        ArrayList<Article> resultlist = new ArrayList<Article>();
        try {
        	String[] querys = {"发型"};
        	String[] fields = {"title"};
        	BooleanClause.Occur[] flags = { 
        			BooleanClause.Occur.MUST}; 
        	query = MultiFieldQueryParser.parse(Version.LUCENE_36, querys, fields, flags, analyzer);
        } catch (ParseException e) {  
        }  
        if (searcher != null) {  
            TopDocs results = searcher.search(query, 500);
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
    		         attributeslist.add(doc.get("title").toString());
    		         attributeslist.add(doc.get("content").toString());
    		         resultlist.add(new Article(attributeslist));
                }
            }
            searcher.close();
        }
        // resultlist = uniqueResult(resultlist);
        FileOperator.ArticleTextWriter(new File(resultPath).getPath(), resultlist, "gb18030");
        System.out.println("writing article finished ...");
    }
    
    public ArrayList<Article> uniqueResult(ArrayList<Article> attributeslist) {
    	Unique uniqueObject = new Unique();
    	List<List<String>> articlelist = new ArrayList<List<String>>();
    	for(Article article : attributeslist) {
    		articlelist.add(article.toList());
    	}
    	System.out.println(articlelist.size());
    	List<List<String>> resultlist = uniqueObject.unique(articlelist, 2, 5);
    	System.out.println(resultlist.size());
    	ArrayList<Article> arrayarticle = new ArrayList<Article>();
    	for(List<String> list: resultlist) {
    		arrayarticle.add(new Article(new ArrayList<String>(list)));
    	}
    	return arrayarticle;
    }
}
