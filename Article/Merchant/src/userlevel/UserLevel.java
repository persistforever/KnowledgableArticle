package userlevel;

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

public class UserLevel {
	String inputpath = "";
	String dictpath = "";
	String outputpath = "";
	String tmpout = "";
	String date = "";
	public long reducenum = 0;
	ArrayList<String> inputList = new ArrayList<String>();

	/**
	 * 
	 * @param userhistory
	 *            (uin, Xid) taged user file
	 * @param output
	 *            (frequency, Xid) the sorted file, descending
	 * @param tmpout
	 *            (frequency, Xid) unsorted file
	 */
	public UserLevel(String usertag, String dictpath, String globalrank, 
			String date, String day) {
		this.inputpath = usertag;
		this.dictpath = dictpath;
		this.outputpath = globalrank;
		this.inputList = Week.Input(this.inputpath, date, Integer.parseInt(day));
		this.date = date;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("dictpath", this.dictpath);
		Job job = new Job(conf);
		tools.HadoopFileOperation.DeleteDir(this.outputpath, conf);

		job.setJarByClass(UserLevel.class);
		job.setMapperClass(UserLevelMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setReducerClass(UserLevelReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setNumReduceTasks(100);

		for (String out : inputList) {
			MultipleInputs.addInputPath(job, new Path(out),
					TextInputFormat.class, UserLevelMapper.class);
		}
		FileOutputFormat.setOutputPath(job, new Path(outputpath));
		job.waitForCompletion(true);
	}

}
