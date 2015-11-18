package bow;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import tools.LineSplit;

public class TFMapper extends Mapper<Object, Text, Text, Text> {
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String line = new String(value.getBytes(), 0, value.getLength(), "GB18030");
		String id = LineSplit.split(line, "\t", 0);
		String title = LineSplit.split(line, "\t", 1);
		String content = LineSplit.split(line, "\t", 2);
		HashMap<String, Integer> wordmap = new HashMap<String, Integer>();
		for (String word : LineSplit.split(title, " ")) {
			if (!wordmap.containsKey(word)) {
				wordmap.put(word, 1);
			}
			else {
				int num = wordmap.get(word);
				wordmap.remove(word);
				wordmap.put(word, num+1);
			}
		}
		for (String word : LineSplit.split(content, " ")) {
			if (!wordmap.containsKey(word)) {
				wordmap.put(word, 1);
			}
			else {
				int num = wordmap.get(word);
				wordmap.remove(word);
				wordmap.put(word, num+1);
			}
		}
		for (Map.Entry<String, Integer> entry : wordmap.entrySet()) {
			if (!LineSplit.split(entry.getKey(), ":", 1).equals("w")) {
				context.write(new Text(id), new Text(entry.getKey() + "\t" + entry.getValue()));
			}
		}
	}
}