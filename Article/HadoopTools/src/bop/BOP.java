package bop;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import tools.GbkOutputFormat;
import tools.HadoopFileOperation;

public class BOP {
	String datapath = "";
	String pospath = "";
	String boppath = "";

	public BOP(String datapath, String pospath, String boppath) {
		this.datapath = datapath;
		this.pospath = pospath;
		this.boppath = boppath;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("posset", this.pospath);
		Job job = new Job(conf);
		HadoopFileOperation.DeleteDir(this.boppath, conf);

		job.setJarByClass(BOP.class);
		job.setMapperClass(TFMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setReducerClass(BOPReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setOutputFormatClass(GbkOutputFormat.class);
		job.setNumReduceTasks(100);

		FileInputFormat.setInputPaths(job, new Path(this.datapath));
		FileOutputFormat.setOutputPath(job, new Path(this.boppath));
		job.waitForCompletion(true);
	}
}