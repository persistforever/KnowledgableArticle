package main;

import globalrank.GlobalRank;

import java.io.IOException;

import userlevel.UserLevel;
import usertag.MerchantReduceAnalyser;
import usertag.MerchantSnsAnalyser;
import usertag.UserTag;



public class MerchantRun {
	private String usertagpath = "";
	private String poipath = "";
	private String rankpath = "";
	private String levelpath = "";
	private String date = "";
	private String day = "";
	
	public MerchantRun(String usertagpath, String poipath, String rankpath, String levelpath,
			String date, String day){
		this.usertagpath = usertagpath;
		this.poipath = poipath;
		this.rankpath = rankpath;
		this.levelpath = levelpath;
		this.date = date;
		this.day = day;
	}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		String usertagpath = args[0];
		String poipath = args[1];
		String rankpath = args[2];
		String levelpath = args[3];
		String date = args[4];
		String day = args[5];
		MerchantRun run = new MerchantRun(usertagpath, poipath, rankpath, levelpath, date, day);
		run.run();
	}
	
	public void run() throws IOException, ClassNotFoundException, InterruptedException{
		Long[] outinfo = new Long[3];
		
		System.out.println("============start===============");
		/*
		System.out.println("============ user_tag ===============");
		UserTag ut = new UserTag(this.snspath, this.poipath, this.usertagpath, this.date,
				MerchantSnsAnalyser.class, MerchantReduceAnalyser.class);
		ut.run();
		
		System.out.println("============ global_rank ===============");
		GlobalRank gr = new GlobalRank(this.usertagpath, this.rankpath, this.date, this.day);
		gr.run();
		outinfo[0] = gr.reducenum;
		*/
		System.out.println("============ user_level ===============");
		UserLevel ul = new UserLevel(this.usertagpath, this.poipath, this.levelpath, this.date, this.day);
		ul.run();
		outinfo[0] = ul.reducenum;
		
		System.out.println("============end===============");
	}
}