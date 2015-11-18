package tools;

import java.util.ArrayList;

public class Article {
	/* attributes */
	public String id = "";
	public String url = "";
	public String completetitle = "";
	// public String keytitle = "";
	public String content = "";
	
	/* methods */
	public Article(ArrayList<String> linelist) {
		if (linelist.size() >= 4) {
			this.id = linelist.get(0);
			this.url = linelist.get(1);
			this.completetitle = linelist.get(2);
			this.content = linelist.get(3);
		}
	}
	
	public String toString() {
		String outstring = "";
		outstring += this.id.toString() + "," ;
		outstring += this.url.toString() + "," ;
		outstring += this.completetitle.toString() + "," ;
		outstring += this.content.toString();
		return outstring.trim();
	}
}
