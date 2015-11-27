package tfidf;

import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.HadoopFileOperation;
import tools.LineSplit;

public class IDFReducer extends Reducer<Text, IntWritable, Text, Text> {
	HashSet<String> stopwords = new HashSet<String>();
	HashMap<String, Integer> wordsets = new HashMap<String, Integer>();

	public class StopWordReader implements HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			String word = s.trim();
			if (!(IDFReducer.this.stopwords.contains(word))) {
				IDFReducer.this.stopwords.add(word);
			}
		}
	}

	public class WordSetReader implements HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 2) {
				String word = LineSplit.split(s, "\t", 0);
				int id = Integer.parseInt(LineSplit.split(s, "\t", 1));
				if (!(IDFReducer.this.wordsets.containsKey(word))) {
					IDFReducer.this.wordsets.put(word, id);
				}
			}
		}
	}

	protected void setup(Reducer<Text, IntWritable, Text, Text>.Context context)
			throws IOException, InterruptedException {
		StopWordReader stopWordReader = new StopWordReader();
		WordSetReader wordSetReader = new WordSetReader();

		HadoopFileOperation.ReducerReadFile(context, "stopwords", stopWordReader);
		HadoopFileOperation.ReducerReadFile(context, "wordsets", wordSetReader);
	}
		
	protected void reduce(Text key, Iterable<IntWritable> value,
			Reducer<Text, IntWritable, Text, Text>.Context context)
			throws IOException, InterruptedException {
		int sum = 0;
		for (IntWritable num : value) {
			sum += num.get();
		}
		double idf = Math.log(1.0 * Integer.parseInt(context.getConfiguration().get("length")) / sum);
		if (!this.stopwords.contains(key.toString().split(":")[0])) {
			context.write(new Text(key), new Text(String.valueOf(idf)));
		}
	}
}