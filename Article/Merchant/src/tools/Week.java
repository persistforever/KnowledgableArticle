package tools;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

public class Week {
	public static void main(String[] args) {
		ArrayList<String> friendList = Week.Input("/user/hdpfelicialin/cas/zgb/friends/", "20150710", 7);
		System.out.println(friendList);
	}
	
	public static ArrayList<String> WeekDate(String date, int day) {
		ArrayList<String> week = new ArrayList<String>();
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
		try {
			Date sdate = dateFormat.parse(date);
			Calendar cal = Calendar.getInstance();
			cal.setTime(sdate);
			for(int i=0 ; i<day; i++) {
				Date tmp = cal.getTime();
				week.add(dateFormat.format(tmp));
				cal.add(Calendar.DAY_OF_YEAR, -1);
			}
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return week;
	}
	
	public static ArrayList<String> Input(String snsinput, String date, int day) {
		ArrayList<String> week = Week.WeekDate(date, day);
		ArrayList<String> output = new ArrayList<String>();
		for(String d:week) {
			String tmp = snsinput.replace(date, d);
			output.add(tmp);
		}
		return output;
	}
	
	public static String getDate(String start, int day) {
		String date = start;
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
		try {
			Date sdate = dateFormat.parse(start);
			Calendar cal = Calendar.getInstance();
			cal.setTime(sdate);
			cal.add(Calendar.DAY_OF_YEAR, day);
			Date tmp = cal.getTime();
			date = dateFormat.format(tmp);
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return date;
	}
	
	public static int getDateSpan(String start, String end) {
		int result = 0;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");
        Calendar c1 = Calendar.getInstance();
        Calendar c2 = Calendar.getInstance();
        try {
			c1.setTime(sdf.parse(start));
	        c2.setTime(sdf.parse(end));
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        result = c2.get(Calendar.MONTH) - c1.get(Calendar.MONTH);
        return result;
	}
}

