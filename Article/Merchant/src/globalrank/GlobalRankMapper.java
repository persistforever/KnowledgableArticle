package globalrank;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class GlobalRankMapper extends Mapper<Object, Text, Text, Text> {

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String s = value.toString();
		String merchant = tools.LineSplit.split(s, "\t", 1);
		String time = tools.LineSplit.split(s, "\t", 2);
		context.write(new Text(merchant), new Text(time));
	}

}
