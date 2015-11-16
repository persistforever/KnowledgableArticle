package tools;

import java.util.ArrayList;

public class LineSplit {
	public static int getlength(String s, String delim) {
		int i = 0;
		int start1 = 0;
		int end1 = s.indexOf(delim, start1);
		while (true) {
			String t;
			if (end1 == -1)
				t = s.substring(start1);
			else
				t = s.substring(start1, end1);
			++i;

			if (end1 == -1)
				break;
			start1 = end1 + 1;
			end1 = s.indexOf(delim, start1);
		}

		return i;
	}

	public static String getindexi(String line, int index, String delm) {
		String s = "";
		int start1 = 0;
		int end1 = line.indexOf(delm, start1);
		while (true) {
			if (index <= 0) {
				if (end1 == -1) {
					s = line.substring(start1);
					break;
				}
				s = line.substring(start1, end1);
				break;
			}
			--index;
			if (end1 == -1)
				break;
			start1 = end1 + delm.length();
			end1 = line.indexOf(delm, start1);
		}

		if (s.length() == 0)
			s = line;
		return s;
	}

	public static String getindexistrong(String line, int index, String delm) {
		String s = "";
		int start1 = 0;
		int end1 = line.indexOf(delm, start1);
		while (true) {
			if (index <= 0) {
				if (end1 == -1) {
					s = line.substring(start1);
					break;
				}
				s = line.substring(start1, end1);
				break;
			}
			--index;
			if (end1 == -1)
				break;
			start1 = end1 + delm.length();
			end1 = line.indexOf(delm, start1);
		}

		return s.trim();
	}

	public static int getLength(String s, String sc) {
		int i = 0;
		int start1 = 0;
		int end1 = s.indexOf(sc, start1);
		while (true) {
			++i;
			if (end1 == -1)
				break;
			start1 = end1 + sc.length();
			end1 = s.indexOf(sc, start1);
		}

		return i;
	}

	public static ArrayList<String> split(String s, String sc) {
		ArrayList word = new ArrayList();
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

	public static boolean isNumber(String str) {
		for (int i = str.length(); --i >= 0;) {
			if (!(Character.isDigit(str.charAt(i)))) {
				return false;
			}
		}
		return true;
	}
}