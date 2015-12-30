package tools;

import java.util.ArrayList;

public class LineSplit {
	public static int getlength(String s, String delim){
		int i = 0;
		for (int start1 = 0, end1 = s.indexOf(delim, start1);; start1 = end1 + 1, end1 = s
				.indexOf(delim, start1)) {
			@SuppressWarnings("unused")
			String t;
			if (end1 == -1)
				t = s.substring(start1);
			else
				t = s.substring(start1, end1);
			i++;

			if (end1 == -1)
				break;
		}
		return i;
	}
	
	public static String getindexi(String line, int index, String delm){
		String s = "";
		for (int start1 = 0, end1 = line.indexOf(delm, start1);; start1 = end1
				+ delm.length(), end1 = line.indexOf(delm, start1)) {
			if (index <= 0) {
				if (end1 == -1)
					s = line.substring(start1);
				else
					s = line.substring(start1, end1);
				break;
			} else
				--index;
			if (end1 == -1)
				break;
		}
		if(s.length() == 0)s = line;
		return s;

	}
	
	public static String getindexistrong(String line, int index, String delm){
		String s = "";
		for (int start1 = 0, end1 = line.indexOf(delm, start1);; start1 = end1
				+ delm.length(), end1 = line.indexOf(delm, start1)) {
			if (index <= 0) {
				if (end1 == -1)
					s = line.substring(start1);
				else
					s = line.substring(start1, end1);
				break;
			} else
				--index;
			if (end1 == -1)
				break;
		}
		return s.trim();

	}
	
	public static int getLength(String s, String sc) {
		int i = 0;
		for (int start1 = 0, end1 = s.indexOf(sc, start1); ; start1 = end1 + sc.length(), end1 = s.indexOf(sc, start1)) {
			i++;
			if (end1 == -1)
				break;
		}
		return i;
	}

	public static ArrayList<String> split(String s, String sc) {
		ArrayList<String> word = new ArrayList<String>();
		if(s.isEmpty())return word;
		for (int start1 = 0, end1 = s.indexOf(sc, start1); ; start1 = end1 + sc.length(), end1 = s.indexOf(sc, start1)) {
			String t;
			if (end1 == -1)
				t = s.substring(start1);
			else
				t = s.substring(start1, end1);
			word.add(t);
			if (end1 == -1)
				break;
		}
		return word;
	}

	public static String split(String s, String sc, int index) {
		String tid = "";
		int i = 0;
		for (int start1 = 0, end1 = s.indexOf(sc, start1); ; start1 = end1 + sc.length(), end1 = s.indexOf(sc, start1)) {
			String t;
			if (end1 == -1)
				t = s.substring(start1);
			else
				t = s.substring(start1, end1);
			i++;
			if(i == (index+1)){
				tid = t;
				break;
			}
			if (end1 == -1)
				break;
		}
		return tid;
	}
}
