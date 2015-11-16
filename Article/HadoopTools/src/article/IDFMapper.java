package article;

import java.io.IOException;
import java.util.ArrayList;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import tools.LineSplit;

public class IDFMapper extends Mapper<Object, Text, Text, IntWritable> {
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, IntWritable>.Context context)
			throws IOException, InterruptedException {
		String line = new String(value.getBytes(), 0, value.getLength(),
				"GB18030");
		String content = LineSplit.split(line, "\t", 2);
		ArrayList<String> wordList = LineSplit.split(content, " ");
		for (String word : wordList) {
			context.write(new Text(word), new IntWritable(1));
		}
	}
}