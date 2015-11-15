package tools;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

public class FileOperator {
	/* import methods */
    public static ArrayList<Article> ArticleFileReader(String FileName, String charset)  
            throws IOException {  
        BufferedReader reader = new BufferedReader(new InputStreamReader(  
                new FileInputStream(FileName), charset));  
        String line = new String();  
        ArrayList<Article> artlist = new ArrayList<Article>();  
        while ((line = reader.readLine()) != null) {
        	ArrayList<String> linelist = new ArrayList<String>();
        	String [] linearray = line.split("\t");
        	for(String attribute: linearray) {
        		linelist.add(attribute);
        	}
        	Article article = new Article(linelist);
        	artlist.add(article);
        }
        reader.close();  
        return artlist;
    }  
    
	/* write methods */
    public static void ArticleFileWriter(String FileName, ArrayList<Article> resultlist, String charset) 
    		throws IOException {
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(  
                new FileOutputStream(FileName), charset));
		String outputstring = "";
		for(Article article: resultlist) {
			outputstring += article.toString() + "\n";
		}
		writer.write(outputstring);
		writer.close();
    }
}
