package friendrank;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class FriendRank {
	String inputpath = "";
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
	public FriendRank(String usertag, String globalrank, String date) {
		this.inputpath = usertag;
		this.outputpath = globalrank;
		this.date = date;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("today", this.date);
		Job job = new Job(conf);
		tools.HadoopFileOperation.DeleteDir(this.outputpath, conf);

		job.setJarByClass(FriendRank.class);
		job.setMapperClass(FriendRankMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setReducerClass(FriendRankReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setNumReduceTasks(100);

		MultipleInputs.addInputPath(job, new Path(this.inputpath),
				TextInputFormat.class, FriendRankMapper.class);
		FileOutputFormat.setOutputPath(job, new Path(outputpath));
		job.waitForCompletion(true);
	}

}
