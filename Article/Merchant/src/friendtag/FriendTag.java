package friendtag;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import tools.Week;


public class FriendTag {
	public String validfrdpath = "";
	public String usertagpath = "";
	public String outputpath = "";
	ArrayList<String> usertagList = new ArrayList<String>();

	/**
	 * 
	 * @param inputpath0
	 *            friends chain 
	 * @param inputpath1
	 *            user tag
	 * @param outputpath
	 *            Taged User File from there friends, <uin, Xid>
	 */
    public FriendTag(String validfrd, String usertag, String friendtag, String date, String day){
		this.validfrdpath = validfrd;
		this.usertagpath = usertag;
		this.outputpath = friendtag;
		this.usertagList = Week.Input(this.usertagpath, date, Integer.parseInt(day));
	}
    
	public void run() throws IOException, ClassNotFoundException, InterruptedException{
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		Job job = new Job(conf);
		tools.HadoopFileOperation.DeleteDir(this.outputpath, conf);
		
		job.setJarByClass(FriendTag.class);
		job.setReducerClass(FriendTagReducer.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setNumReduceTasks(100);
		
		for(int i=0 ; i<7 ; i++) {
			MultipleInputs.addInputPath(job, new Path(this.validfrdpath+i), TextInputFormat.class, FriendTagMapper1.class);
		}
		for(String in:this.usertagList) {
			MultipleInputs.addInputPath(job, new Path(in), TextInputFormat.class, FriendTagMapper2.class);
		}
		FileOutputFormat.setOutputPath(job, new Path(this.outputpath));
		
		job.waitForCompletion(true);
	}
}
