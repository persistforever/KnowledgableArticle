package main;

import java.io.IOException;
import java.util.ArrayList;

import tools.HadoopFileOperation;
import tools.Week;
import usertag.MerchantSnsAnalyser;
import usertag.MerchantReduceAnalyser;
import usertag.UserTag;



public class UserTagMain {
	private String pyqpath = "";
	private String poipath = "";
	private String mainpath = "";
	private String date = "";
	private int day = 0;
	ArrayList<String> inputList = new ArrayList<String>();
	ArrayList<String> outputList = new ArrayList<String>();
	
	public UserTagMain(String pyqpath, String poipath, String mainpath, String date, String day){
		this.pyqpath = pyqpath;
		this.poipath = poipath;
		this.mainpath = mainpath;
		this.date = date;
		this.day = Integer.parseInt(day);
		this.inputList = Week.Input(this.pyqpath, date, this.day);
	}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		String pyqpath = args[0];
		String poipath = args[1];
		String mainpath = args[2];
		String date = args[3];
		String day = args[4];
		UserTagMain run = new UserTagMain(pyqpath, poipath, mainpath, date, day);
		run.run();
	}
	
	public void run() throws IOException, ClassNotFoundException, InterruptedException{
		System.out.println("============usertag===============");
		this.inputList = Week.Input(this.pyqpath, date, day);
		this.outputList = Week.Input(HadoopFileOperation.CatPath(this.mainpath, date), date, day);
		for(int i=0 ; i<this.inputList.size() ; i++) {
			String in = this.inputList.get(i);
			String out = this.outputList.get(i);
			String today = Week.getDate(date, i);
			UserTag ut = new UserTag(in, this.poipath, out, today,
					MerchantSnsAnalyser.class, MerchantReduceAnalyser.class);
			ut.run();
		}
	}

}
