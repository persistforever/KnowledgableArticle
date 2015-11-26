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
		outstring += this.id.toString() + "\t";
		outstring += this.url.toString() + "\t";
		outstring += this.title.toString() + "\t";
		outstring += this.content.toString() + "\t";
		return outstring.trim();
	}
	
	public ArrayList<String> toList() {
		ArrayList<String> arraylist = new ArrayList<String>();
		arraylist.add(this.id.toString());
		arraylist.add(this.url.toString());
		arraylist.add(this.title.toString());
		arraylist.add(this.content.toString());
		return arraylist;
	}
}
