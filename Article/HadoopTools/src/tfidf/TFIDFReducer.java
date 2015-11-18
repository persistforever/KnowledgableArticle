package tfidf;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import tools.HadoopFileOperation;
import tools.LineSplit;

public class TFIDFReducer extends Reducer<Text, Text, Text, Text> {
	HashMap<String, Double> idfmap = new HashMap<String, Double>();

	public class IDFMapReader implements
			HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 2) {
				String word = LineSplit.split(s, "\t", 0);
				double idf = Double.parseDouble(LineSplit.split(s, "\t", 1));
				if (!(TFIDFReducer.this.idfmap.containsKey(word)))
					TFIDFReducer.this.idfmap.put(word, Double.valueOf(idf));
			}
		}
	}

	protected void setup(Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		IDFMapReader idfMapReader = new IDFMapReader();

		HadoopFileOperation.ReducerReadFile(context, "idfpath", idfMapReader);
	}

	@SuppressWarnings({ "unchecked", "rawtypes" })
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		HashMap<String, Double> tfmap = new HashMap<String, Double>();
		HashMap<String, Double> tfidfmap = new HashMap<String, Double>();
		for (Text v : value) {
			String word = LineSplit.split(v.toString(), "\t", 0);
			double num = Double.parseDouble(LineSplit.split(v.toString(), "\t", 1));
			tfmap.put(word, num);
		}
		for (Map.Entry<String, Double> entry : tfmap.entrySet()) {
			String word = entry.getKey();
			if (this.idfmap.containsKey(word)) {
				double tfidf = entry.getValue() * idfmap.get(word);
				tfidfmap.put(word, Double.valueOf(tfidf));
			}
		}
		ArrayList<Map.Entry<String, Double>> wordlist = new ArrayList<Map.Entry<String, Double>>(tfidfmap.entrySet());
		Collections.sort(wordlist, new Comparator() {
			public int compare(Object o1, Object o2) {
				return ((Map.Entry<String, Double>)o2).getValue().compareTo(
						((Map.Entry<String, Double>)o1).getValue());
			}
		});
		String v = "";
		for (int i = 0; i < Math.min(wordlist.size(), 300); ++i) {
			String word = wordlist.get(i).getKey();
			String num = String.valueOf(wordlist.get(i).getValue());
			v = v + word + "<#>" + num + "\t";
		}
		context.write(new Text(key), new Text(v.trim()));
	}
}