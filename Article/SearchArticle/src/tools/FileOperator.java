package tools;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

public class FileOperator {
	/* import methods */
    public static ArrayList<Article> ArticleFileReader(String FileName, String charset)  
            throws IOException {  
    	System.out.println(FileName);
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
    public static void ArticleTextWriter(String FileName, ArrayList<Article> resultlist, String charset) 
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
		
    public static void ArticleCSVWriter(String FileName, ArrayList<Article> resultlist, String charset) {
		try {
			File csv = new File(FileName);
			BufferedWriter writer = new BufferedWriter(new FileWriter(csv));
			for(Article article: resultlist) {
				writer.write(article.toString());
				writer.newLine();
			}
			writer.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) { 
			e.printStackTrace(); 
		} 
	}
}
