package article;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import tools.GbkOutputFormat;
import tools.HadoopFileOperation;

public class TFIDF {
	String datapath = "";
	String idfpath = "";
	String tfidfpath = "";

	public TFIDF(String datapath, String idfpath, String tfidfpath) {
		this.datapath = datapath;
		this.idfpath = idfpath;
		this.tfidfpath = tfidfpath;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("idfpath", this.idfpath);
		Job job = new Job(conf);
		HadoopFileOperation.DeleteDir(this.tfidfpath, conf);

		job.setJarByClass(TFIDF.class);
		job.setMapperClass(TFMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setReducerClass(TFIDFReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setOutputFormatClass(GbkOutputFormat.class);
		job.setNumReduceTasks(100);

		FileInputFormat.setInputPaths(job,
				new Path[] { new Path(this.datapath) });
		FileOutputFormat.setOutputPath(job, new Path(this.tfidfpath));
		job.waitForCompletion(true);
	}
}