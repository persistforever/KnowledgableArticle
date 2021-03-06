package article.gzh_follownum;

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

public class GLC {
	String dataPath = "";
	String gzhPath = "";
	String gacPath = "";
	String userThreshold = "";
	String articleThreshold = "";

	public GLC(String dataPath, String gzhPath, String gacPath, 
			String userThreshold, String articleThreshold) {
		this.dataPath = dataPath;
		this.gzhPath = gzhPath;
		this.gacPath = gacPath;
		this.userThreshold = userThreshold;
		this.articleThreshold = articleThreshold;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("gzh", this.gzhPath);
		conf.set("user", this.userThreshold);
		conf.set("article", this.articleThreshold);
		Job job = new Job(conf);
		HadoopFileOperation.DeleteDir(this.gacPath, conf);

		job.setJarByClass(GLC.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setOutputFormatClass(GbkOutputFormat.class);
		job.setNumReduceTasks(100);

		MultipleInputs.addInputPath(job, new Path(this.gzhPath), TextInputFormat.class, GzhMapper.class);
		FileOutputFormat.setOutputPath(job, new Path(this.gacPath));
		job.waitForCompletion(true);
	}
}