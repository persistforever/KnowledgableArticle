package bow;

import java.io.IOException;
import java.util.HashMap;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.HadoopFileOperation;
import tools.LineSplit;

public class BOWReducer extends Reducer<Text, Text, Text, Text> {
	HashMap<String, Integer> wordindex = new HashMap<String, Integer>();

	public class IDFMapReader implements HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 2) {
				String word = LineSplit.split(s, "\t", 0);
				int id = Integer.parseInt(LineSplit.split(s, "\t", 1));
				if (!(BOWReducer.this.wordindex.containsKey(word))) {
					BOWReducer.this.wordindex.put(word, id);
				}
			}
		}
	}

	protected void setup(Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		IDFMapReader idfMapReader = new IDFMapReader();

		HadoopFileOperation.ReducerReadFile(context, "wordset", idfMapReader);
	}

	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String [] bowvector = new String [this.wordindex.size()];
		for (int i=0 ; i<bowvector.length ; i++) {
			bowvector[i] = "0";
		}
		for (Text v : value) {
			String word = LineSplit.split(v.toString(), "\t", 0);
			String num = LineSplit.split(v.toString(), "\t", 1);
			if (this.wordindex.containsKey(word)) {
				bowvector[this.wordindex.get(word)-1] = num;
			}
		}
		String outstr = "";
		for (int i=0 ; i<bowvector.length ; i++) {
			outstr += bowvector[i] + " ";
		}
		context.write(new Text(key), new Text(outstr.trim()));
	}
}