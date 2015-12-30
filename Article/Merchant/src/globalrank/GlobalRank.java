package globalrank;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import tools.Week;

public class GlobalRank {
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
	public GlobalRank(String usertag, String globalrank, String date, String day) {
		this.inputpath = usertag;
		this.outputpath = globalrank;
		this.tmpout = globalrank + "_tmp";
		this.inputList = Week.Input(this.inputpath, date, Integer.parseInt(day));
		this.date = date;
	}

	public void run() throws IOException, ClassNotFoundException,
			InterruptedException {
		Configuration conf = new Configuration();
		conf.set("mapred.job.queue.name", "searchteam");
		conf.set("mapred.job.priority", "NORMAL");
		conf.set("date", this.date);
		Job job = new Job(conf);
		tools.HadoopFileOperation.DeleteDir(tmpout, conf);

		job.setJarByClass(GlobalRank.class);
		job.setMapperClass(GlobalRankMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setReducerClass(GlobalRankReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setNumReduceTasks(100);

		for (String out : inputList) {
			MultipleInputs.addInputPath(job, new Path(out),
					TextInputFormat.class, GlobalRankMapper.class);
		}
		FileOutputFormat.setOutputPath(job, new Path(tmpout));
		job.waitForCompletion(true);

		// sort
		job = new Job(conf);
		tools.HadoopFileOperation.DeleteDir(outputpath, conf);

		job.setJarByClass(GlobalRank.class);
		job.setMapperClass(SortMapper.class);
		job.setMapOutputKeyClass(IntWritable.class);
		job.setMapOutputValueClass(Text.class);
		job.setSortComparatorClass(IntKeyDescComparator.class);
		FileInputFormat.setInputPaths(job, new Path(tmpout));
		FileOutputFormat.setOutputPath(job, new Path(outputpath));
		job.waitForCompletion(true);
		reducenum = job
				.getCounters()
				.findCounter("org.apache.hadoop.mapred.Task$Counter",
						"REDUCE_OUTPUT_RECORDS").getValue();

		tools.HadoopFileOperation.DeleteDir(tmpout, conf);
	}

	public static class SortMapper extends
			Mapper<Object, Text, IntWritable, Text> {

		@Override
		protected void map(Object key, Text value,
				Mapper<Object, Text, IntWritable, Text>.Context context)
				throws IOException, InterruptedException {
			String s = value.toString();
			int index = s.indexOf("\t");
			String num = s.substring(0, index);
			String sid = s.substring(index + 1);
			context.write(new IntWritable(Integer.parseInt(num)), new Text(sid));
		}
	}

	public static class IntKeyDescComparator extends WritableComparator {
		protected IntKeyDescComparator() {
			super(IntWritable.class, true);

		}

		@SuppressWarnings("rawtypes")
		@Override
		public int compare(WritableComparable a, WritableComparable b) {
			return -super.compare(a, b);
		}

	}

}
