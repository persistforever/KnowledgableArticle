package tfidf;

import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.HadoopFileOperation;
import tools.LineSplit;

public class IDFReducer extends Reducer<Text, IntWritable, Text, Text> {
	HashMap<String, Integer> wordindex = new HashMap<String, Integer>();

	public class IDFMapReader implements HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 2) {
				String word = LineSplit.split(s, "\t", 0);
				int id = Integer.parseInt(LineSplit.split(s, "\t", 1));
				if (!(IDFReducer.this.wordindex.containsKey(word))) {
					IDFReducer.this.wordindex.put(word, id);
				}
			}
		}
	}

	protected void setup(Reducer<Text, IntWritable, Text, Text>.Context context)
			throws IOException, InterruptedException {
		IDFMapReader idfMapReader = new IDFMapReader();

		HadoopFileOperation.ReducerReadFile(context, "wordset", idfMapReader);
	}
		
	protected void reduce(Text key, Iterable<IntWritable> value,
			Reducer<Text, IntWritable, Text, Text>.Context context)
			throws IOException, InterruptedException {
		int sum = 0;
		for (IntWritable num : value) {
			sum += num.get();
		}
		double idf = Math.log(1.0 * Integer.parseInt(context.getConfiguration().get("length")) / sum);
		if (this.wordindex.containsKey(key.toString())) {
			context.write(new Text(key), new Text(String.valueOf(idf)));
		}
	}
}