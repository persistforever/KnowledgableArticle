package article.article_collectnum;

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

public class AC {
	String dataPath = "";
	String acPath = "";

	public AC(String dataPath, String acPath) {
		this.dataPath = dataPath;
		this.acPath = acPath;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		Job job = new Job(conf);
		HadoopFileOperation.DeleteDir(this.acPath, conf);

		job.setJarByClass(AC.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setOutputFormatClass(GbkOutputFormat.class);
		job.setNumReduceTasks(100);

		MultipleInputs.addInputPath(job, new Path(this.dataPath), TextInputFormat.class, ArticleMapper.class);
		FileOutputFormat.setOutputPath(job, new Path(this.acPath));
		job.waitForCompletion(true);
	}
}