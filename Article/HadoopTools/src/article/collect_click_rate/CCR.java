package article.collect_click_rate;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import tools.GbkOutputFormat;
import tools.HadoopFileOperation;

public class CCR {
	String dataPath = "";
	String ccrPath = "";

	public CCR(String dataPath, String acPath) {
		this.dataPath = dataPath;
		this.ccrPath = acPath;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		Job job = new Job(conf);
		HadoopFileOperation.DeleteDir(this.ccrPath, conf);

		job.setJarByClass(CCR.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setOutputFormatClass(GbkOutputFormat.class);
		job.setNumReduceTasks(100);

		MultipleInputs.addInputPath(job, new Path(this.dataPath), TextInputFormat.class, ArticleMapper.class);
		FileOutputFormat.setOutputPath(job, new Path(this.ccrPath));
		job.waitForCompletion(true);
	}
}