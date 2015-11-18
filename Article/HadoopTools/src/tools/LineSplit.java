package tools;

import java.util.ArrayList;

public class LineSplit {

	public static ArrayList<String> split(String s, String sc) {
		ArrayList<String> word = new ArrayList<String>();
		int start1 = 0;
		int end1 = s.indexOf(sc, start1);
		while (true) {
			String t;
			if (end1 == -1)
				t = s.substring(start1);
			else
				t = s.substring(start1, end1);
			word.add(t);
			if (end1 == -1)
				break;
			start1 = end1 + sc.length();
			end1 = s.indexOf(sc, start1);
		}

		return word;
	}

	public static String split(String s, String sc, int index) {
		String tid = "";
		int i = 0;
		int start1 = 0;
		int end1 = s.indexOf(sc, start1);
		while (true) {
			String t;
			if (end1 == -1)
				t = s.substring(start1);
			else
				t = s.substring(start1, end1);
			++i;
			if (i == index + 1) {
				tid = t;
				break;
			}
			if (end1 == -1)
				break;
			start1 = end1 + sc.length();
			end1 = s.indexOf(sc, start1);
		}

		return tid;
	}
}