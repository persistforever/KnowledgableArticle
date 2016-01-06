package main;

import java.io.IOException;

import userlevel.UserLevel;

public class UserLevelRun {
	private String usertagpath = "";
	private String poipath = "";
	private String levelpath = "";
	private String date = "";
	private String day = "";

	public UserLevelRun(String usertagpath, String poipath, String levelpath,
			String date, String day) {
		this.usertagpath = usertagpath;
		this.poipath = poipath;
		this.levelpath = levelpath;
		this.date = date;
		this.day = day;
	}

	public static void main(String[] args) throws IOException,
			ClassNotFoundException, InterruptedException {
		String usertagpath = args[0];
		String poipath = args[1];
		String levelpath = args[2];
		String date = args[3];
		String day = args[4];
		UserLevelRun run = new UserLevelRun(usertagpath, poipath, levelpath,
				date, day);
		run.run();
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out
				.println("==================== user_level ====================");
		UserLevel ul = new UserLevel(this.usertagpath, this.poipath,
				this.levelpath, this.date, this.day);
		ul.run();
	}
}