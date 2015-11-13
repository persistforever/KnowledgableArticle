package tools;

import java.util.ArrayList;

public class Article {
	/* attributes */
	public String id = "";
	public String url = "";
	public String completetitle = "";
	public String keytitle = "";
	
	/* methods */
	public Article(ArrayList<String> linelist) {
		if (linelist.size() >= 4) {
			this.id = linelist.get(0);
			this.url = linelist.get(1);
			this.keytitle = linelist.get(2);
			this.completetitle = linelist.get(3);
		}
	}
	
	public String toString() {
		String outstring = "";
		outstring += this.id.toString() + "\t" ;
		outstring += this.url.toString() + "\t" ;
		outstring += this.keytitle.toString() + "\t" ;
		outstring += this.completetitle.toString() + "\t" ;
		return outstring.trim();
	}
}
