package usertag;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class UserTag {
	String snsinput = "";
	String dicinput = "";
	String outputpath = "";
	String today = "";
	Class<? extends SnsAnalyse> sa;
	Class<? extends ReduceAnalyse> ua;
	public Long reducenum = new Long(0);

	/**
	 * 
	 * @param snsinput
	 *            Moments data of a period of time
	 * @param dicinput
	 *            Dic file such as qqmusic, poi, etc.
	 * @param output
	 *            Taged User File, <uin, Xid>
	 * @param sa
	 *            The class to deal with Moments data, used in the
	 *            UserTagMapper.
	 * @param ua
	 *            The class to get taged user, used in the UserTagReducer.
	 */
	public UserTag(String snsinput, String dicinput, String outputpath, String today, 
			Class<? extends SnsAnalyse> sa, Class<? extends ReduceAnalyse> ua) {
		this.snsinput = snsinput;
		this.dicinput = dicinput;
		this.outputpath = outputpath;
		this.today = today;
		this.ua = ua;
		this.sa = sa;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("today", this.today);
		conf.setClass("snsanalyser", sa.asSubclass(SnsAnalyse.class),
				SnsAnalyse.class);
		conf.setClass("taganalyser", ua.asSubclass(ReduceAnalyse.class),
				ReduceAnalyse.class);
		tools.HadoopFileOperation.DeleteDir(this.outputpath, conf);
		Job job = new Job(conf);
		job.setJarByClass(UserTag.class);
		job.setReducerClass(UserTagReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setNumReduceTasks(100);
		MultipleInputs.addInputPath(job, new Path(snsinput),
				TextInputFormat.class, UserTagMapper.class);
		MultipleInputs.addInputPath(job, new Path(dicinput),
				TextInputFormat.class, DictMapper.class);
		FileOutputFormat.setOutputPath(job, new Path(outputpath));

		if (job.waitForCompletion(true))
			System.out.println("jobsuccess");
		else System.out.println("jobfailed");
		reducenum = job
				.getCounters()
				.findCounter("org.apache.hadoop.mapred.Task$Counter",
						"REDUCE_OUTPUT_RECORDS").getValue();
	}
}
