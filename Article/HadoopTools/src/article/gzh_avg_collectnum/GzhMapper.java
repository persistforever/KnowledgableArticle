package article.gzh_avg_collectnum;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class GzhMapper extends Mapper<Object, Text, Text, Text> {
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String line = new String(value.getBytes(), 0, value.getLength(), "UTF8");
		if (line.split("\t").length >= 3) {
			String id = line.split("\t")[0];
			Integer follow = Integer.parseInt(line.split("\t")[2]);
			if (follow >= Integer.parseInt(context.getConfiguration().get("user")))
			context.write(new Text(id), new Text(String.valueOf(follow)));
		}
	}
}