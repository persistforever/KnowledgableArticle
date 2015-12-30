package main;

import globalrank.GlobalRank;

import java.io.IOException;

import usertag.MerchantReduceAnalyser;
import usertag.MerchantSnsAnalyser;
import usertag.UserTag;



public class MerchantRun {
	private String snspath = "";
	private String poipath = "";
	private String usertagpath = "";
	private String rankpath = "";
	private String date = "";
	private String day = "";
	
	public MerchantRun(String snspath, String poipath, String usertagpath, String rankpath, 
			String date, String day){
		this.snspath = snspath;
		this.poipath = poipath;
		this.usertagpath = usertagpath;
		this.rankpath = rankpath;
		this.date = date;
		this.day = day;
	}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		String snspath = args[0];
		String poipath = args[1];
		String usertagpath = args[2];
		String rankpath = args[3];
		String date = args[4];
		String day = args[5];
		MerchantRun run = new MerchantRun(snspath, poipath, usertagpath, rankpath, 
				date, day);
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
		*/
		System.out.println("============ global_rank ===============");
		GlobalRank gr = new GlobalRank(this.usertagpath, this.rankpath, this.date, this.day);
		gr.run();
		outinfo[0] = gr.reducenum;
		
		System.out.println("============end===============");
	}
}