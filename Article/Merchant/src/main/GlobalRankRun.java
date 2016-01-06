package main;

import globalrank.GlobalRank;

import java.io.IOException;

public class GlobalRankRun {
	private String usertagpath = "";
	private String rankpath = "";
	private String date = "";
	private String day = "";

	public GlobalRankRun(String usertagpath, String rankpath,
			String date, String day) {
		this.usertagpath = usertagpath;
		this.rankpath = rankpath;
		this.date = date;
		this.day = day;
	}

	public static void main(String[] args) throws IOException,
			ClassNotFoundException, InterruptedException {
		String usertagpath = args[0];
		String rankpath = args[1];
		String date = args[2];
		String day = args[3];
		GlobalRankRun run = new GlobalRankRun(
				usertagpath, rankpath, date, day);
		run.run();
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		System.out
				.println("==================== global_rank ====================");
		GlobalRank gr = new GlobalRank(this.usertagpath, this.rankpath,
				this.date, this.day);
		gr.run();
	}
}