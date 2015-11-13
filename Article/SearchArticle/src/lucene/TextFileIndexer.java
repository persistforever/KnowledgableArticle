package lucene;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Date;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
  
public class TextFileIndexer {  
    public static void main(String[] args) throws Exception {  
        /* 指明要索引文件夹的位置 */  
        File fileDir = new File("E://file/knowledgable/lucene/input");  
        /* 这里放索引文件的位置 */  
        File indexDir = new File("E://file/knowledgable/lucene/output"); 
        
        Directory dir = FSDirectory.open(indexDir);
        Analyzer luceneAnalyzer = new StandardAnalyzer(Version.LUCENE_36);
        IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_36,luceneAnalyzer);
        iwc.setOpenMode(OpenMode.CREATE);
        IndexWriter indexWriter = new IndexWriter(dir,iwc);  
        File[] textFiles = fileDir.listFiles();  
        long startTime = new Date().getTime(); 
          
        //增加document到索引去  
        for (int i = 0; i < textFiles.length; i++) {  
            if (textFiles[i].isFile()) {  
                System.out.println("File " + textFiles[i].getCanonicalPath()  
                        + "正在被索引....");  
                ArrayList<String []> articleList = FileReaderAll(textFiles[i].getCanonicalPath(), 
                		textFiles[i].getPath(), "GB18030"); 
                for (String [] article: articleList) {
                    Document document = new Document();  
	                Field FieldPath = new Field("path", article[0], Field.Store.YES, Field.Index.NO);  
	                Field FieldUrl = new Field("url", article[1], Field.Store.YES, Field.Index.NO); 
	                Field FieldBody = new Field("body", article[2], Field.Store.YES, 
	                		Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS);  
	                document.add(FieldPath); 
	                document.add(FieldUrl);   
	                document.add(FieldBody);  
	                indexWriter.addDocument(document);
                }
            }  
        }  
        indexWriter.close();  
          
        //测试一下索引的时间  
        long endTime = new Date().getTime();  
        System.out  
                .println("这花费了"  
                        + (endTime - startTime)  
                        + " 毫秒来把文档增加到索引里面去!"  
                        + fileDir.getPath());  
    }  
  
    public static ArrayList<String []> FileReaderAll(String FileName, String FilePath, String charset)  
            throws IOException {  
        BufferedReader reader = new BufferedReader(new InputStreamReader(  
                new FileInputStream(FileName), charset));  
        String line = new String();  
        ArrayList<String []> contentList = new ArrayList<String []>();  
          
        while ((line = reader.readLine()) != null) {
        	String [] article = line.split("\t");
        	String [] content = new String [3];
        	content[0] = FilePath + '/' + article[0];
        	content[1] = article[1];
        	content[2] = article[2];
        	contentList.add(content);
        }
        reader.close();  
        return contentList;
    }  
}  