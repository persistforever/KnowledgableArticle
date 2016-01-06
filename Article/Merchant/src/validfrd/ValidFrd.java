package validfrd;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import tools.Week;

public class ValidFrd {
	String usertag = "";
	String friends = "";
	String validfrd = "";
	public long reducenum = 0;
	ArrayList<String> inputList = new ArrayList<String>();

	/**
	 * 
	 * @param usertag (uin, Xid) taged user file 
	 * @param friends (uin, fuin1 fuin2 ...) friends links
	 * @param validfrd (uin, fuin1 fuin2 ...) output file, first item of each line is the user who has been taged
	 */
	public ValidFrd(String usertag, String friends, String validfrd, String date, String day) {
		this.usertag = usertag;
		this.friends = friends;
		this.validfrd = validfrd;
		this.inputList = Week.Input(this.usertag, date, Integer.parseInt(day));
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		
		for(int i=0 ; i<this.inputList.size() ; i++) {
			conf.set("usertag"+String.valueOf(i), this.inputList.get(i));
		}
		conf.set("length", String.valueOf(this.inputList.size()));
		
		Job job = new Job(conf);
		tools.HadoopFileOperation.DeleteDir(this.validfrd, conf);
		
		job.setJarByClass(ValidFrd.class);
		job.setMapperClass(ValidFrdMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setNumReduceTasks(100);
		
		FileOutputFormat.setOutputPath(job, new Path(this.validfrd));
		FileInputFormat.setInputPaths(job, new Path(this.friends));
		job.waitForCompletion(true);
		reducenum = job.getCounters().findCounter("org.apache.hadoop.mapred.Task$Counter", "REDUCE_OUTPUT_RECORDS").getValue();
	}
}
