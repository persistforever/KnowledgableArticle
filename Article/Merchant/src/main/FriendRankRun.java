package main;

import java.io.IOException;
import java.util.ArrayList;

import friendrank.FriendRank;
import friendtag.FriendTag;
import tools.Week;
import validfrd.ValidFrd;

public class FriendRankRun {
	private String usertagpath = "";
	private String friendpath = "";
	private String validfrdpath = "";
	private String friendtagpath = "";
	private String friendrankpath = "";
	private String date = "";
	private String day = "";

	public FriendRankRun(String usertagpath, String friendpath,
			String validfrdpath, String friendtagpath, String friendrankpath, 
			String date, String day) {
		this.usertagpath = usertagpath;
		this.friendpath = friendpath;
		this.validfrdpath = validfrdpath;
		this.friendtagpath = friendtagpath;
		this.friendrankpath = friendrankpath;
		this.date = date;
		this.day = day;
	}

	public static void main(String[] args) throws IOException,
			ClassNotFoundException, InterruptedException {
		String usertagpath = args[0];
		String friendpath = args[1];
		String validfrdpath = args[2];
		String friendtagpath = args[3];
		String friendrankpath = args[4];
		String date = args[5];
		String day = args[6];
		FriendRankRun run = new FriendRankRun(usertagpath, friendpath,
				validfrdpath, friendtagpath, friendrankpath, date, day);
		run.run();
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		/*
		System.out
				.println("==================== valid_frd ====================");
		ArrayList<String> friendList = Week
				.Input(this.friendpath, this.date, 7);
		for (int i = 0; i < friendList.size(); i++) {
			ValidFrd vf = new ValidFrd(this.usertagpath, friendList.get(i),
					this.validfrdpath + i, this.date, this.day);
			vf.run();
		}
		
		System.out
				.println("==================== friend_tag ====================");
		FriendTag ft = new FriendTag(this.validfrdpath, this.usertagpath,
				this.friendtagpath, this.date, this.day);
		ft.run();
		*/
		System.out
				.println("==================== friend_rank ====================");
		FriendRank fr = new FriendRank(this.friendtagpath, this.friendrankpath,
				this.date);
		fr.run();
		
	}
}