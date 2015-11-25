package bop;

import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import tools.LineSplit;

public class TFMapper extends Mapper<Object, Text, Text, Text> {
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String line = new String(value.getBytes(), 0, value.getLength(), "GB18030");
		if (LineSplit.split(line, "\t").size() >= 3) {
			String id = LineSplit.split(line, "\t", 0);
			String title = LineSplit.split(line, "\t", 1);
			String content = LineSplit.split(line, "\t", 2);
			HashSet<String> wordset = new HashSet<String>();
			HashMap<String, Integer> posmap = new HashMap<String, Integer>();
			for (String word : LineSplit.split(title, " ")) {
				if (word.split(":").length == 2) {
					if (!wordset.contains(word)) {
						wordset.add(word);
					}
				}
			}
			for (String word : LineSplit.split(content, " ")) {
				if (word.split(":").length == 2) {
					if (!wordset.contains(word)) {
						wordset.add(word);
					}
				}
			}

			for (String word : wordset) {
				String pos = word.split(":")[1];
				if (!posmap.containsKey(pos)) {
					posmap.put(pos, 1);
				}
				else {
					int num = posmap.get(pos);
					posmap.remove(pos);
					posmap.put(pos, num+1);
				}
			}
			for (Map.Entry<String, Integer> entry : posmap.entrySet()) {
				context.write(new Text(id), new Text(entry.getKey() + "\t" + entry.getValue()));
			}
		}
	}
}