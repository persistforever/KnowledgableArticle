package tfidf;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import tools.GbkOutputFormat;
import tools.HadoopFileOperation;

public class IDF {
	String datapath = "";
	String idfpath = "";
	String length = "";
	String wordpath = "";

	public IDF(String datapath, String idfpath, String length, String wordpath) {
		this.datapath = datapath;
		this.idfpath = idfpath;
		this.length = length;
		this.wordpath = wordpath;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("length", this.length);
		conf.set("wordset", this.wordpath);
		Job job = new Job(conf);
		HadoopFileOperation.DeleteDir(this.idfpath, conf);

		job.setJarByClass(IDF.class);
		job.setMapperClass(IDFMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);
		job.setReducerClass(IDFReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setOutputFormatClass(GbkOutputFormat.class);
		job.setNumReduceTasks(100);

		FileInputFormat.setInputPaths(job,
				new Path[] { new Path(this.datapath) });
		FileOutputFormat.setOutputPath(job, new Path(this.idfpath));
		job.waitForCompletion(true);
	}
}