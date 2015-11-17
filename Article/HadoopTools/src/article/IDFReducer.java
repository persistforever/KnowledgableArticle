package article;

import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class IDFReducer extends Reducer<Text, IntWritable, Text, Text> {
	protected void reduce(Text key, Iterable<IntWritable> value,
			Reducer<Text, IntWritable, Text, Text>.Context context)
			throws IOException, InterruptedException {
		int sum = 0;
		for (IntWritable num : value) {
			sum += num.get();
		}
		double idf = Math.log(1.0 * Integer.parseInt(context.getConfiguration().get("length")) / sum);
		context.write(new Text(key), new Text(String.valueOf(idf)));
	}
}