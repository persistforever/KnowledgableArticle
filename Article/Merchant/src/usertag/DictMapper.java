package usertag;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class DictMapper extends Mapper<Object, Text, Text, Text> {

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String s = value.toString();
		String k = tools.LineSplit.split(s, "\t", 0);
		String v = tools.LineSplit.split(s, "\t", 1);
		context.write(new Text(k), new Text(v));

	}
	
}
