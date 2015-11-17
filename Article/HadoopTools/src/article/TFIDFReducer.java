package article;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;

import tools.HadoopFileOperation;
import tools.HadoopFileOperation.ReadOneLineInterface;
import tools.LineSplit;

public class TFIDFReducer extends Reducer<Text, Text, Text, Text> {
	HashMap<String, Double> idfMap = new HashMap<String, Double>();

	public class IDFMapReader implements
			HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 2) {
				String word = LineSplit.split(s, "\t", 0);
				double idf = Double.parseDouble(LineSplit.split(s, "\t", 1));
				if (!(TFIDFReducer.this.idfMap.containsKey(word)))
					TFIDFReducer.this.idfMap.put(word, Double.valueOf(idf));
			}
		}
	}

	protected void setup(Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		IDFMapReader idfMapReader = new IDFMapReader();

		HadoopFileOperation.ReducerReadFile(context, "idfpath", idfMapReader);
	}

	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		HashMap<String, Double> wordMap = new HashMap<String, Double>();
		HashMap<String, Double> tfidfMap = new HashMap<String, Double>();
		String word;
		for (Text v : value) {
			word = v.toString();
			if (wordMap.containsKey(word)) {
				double num = ((Double) wordMap.get(word)).doubleValue() + 1.0D;
				wordMap.remove(word);
				wordMap.put(word, Double.valueOf(num));
			} else {
				wordMap.put(word, Double.valueOf(1.0D));
			}
		}
		int length = 0;
		for (Map.Entry<String, Double> entry : wordMap.entrySet()) {
			length = (int) (length + ((Double) entry.getValue()).doubleValue());
		}
		for (Map.Entry<String, Double> entry : wordMap.entrySet()) {
			word = entry.getKey().toString();
			if (this.idfMap.containsKey(word)) {
				double num = ((Double) wordMap.get(word)).doubleValue()
						/ length
						* ((Double) this.idfMap.get(word)).doubleValue();
				tfidfMap.put(word, Double.valueOf(num));
			}
		}
		/*
		ArrayList<HashMap<String, Double>> wordList = new ArrayList(tfidfMap.entrySet());
		Collections.sort((List) wordList, new Comparator() {
			public int compare(Map.Entry<String, Double> o1,
					Map.Entry<String, Double> o2) {
				return ((Double) o2.getValue()).compareTo((Double) o1
						.getValue());
			}
		});
		String v = "";
		for (int i = 0; i < Math.min(wordList.size(), 300); ++i) {
			word = wordList.get(i);
			String num = String.valueOf(((Map.Entry) ((List) wordList).get(i))
					.getValue());
			v = v + word + "<#>" + num + "\t";
		}
		context.write(new Text(key), new Text(v.trim()));
		*/
	}
}