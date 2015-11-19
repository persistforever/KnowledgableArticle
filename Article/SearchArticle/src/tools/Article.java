package tools;

import java.util.ArrayList;

public class Article {
	/* attributes */
	public String id = "";
	public String url = "";
	public String title = "";
	public String content = "";
	
	/* methods */
	public Article(ArrayList<String> linelist) {
		if (linelist.size() >= 4) {
			this.id = linelist.get(0);
			this.url = linelist.get(1);
			this.title = linelist.get(2);
			this.content = linelist.get(3);
		}
	}
	
	public String toString() {
		String outstring = "";
		outstring += this.id.toString() ;
		return outstring.trim();
	}
}
