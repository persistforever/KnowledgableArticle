package userlevel;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class UserLevelMapper extends Mapper<Object, Text, Text, Text> {

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String s = value.toString();
		String uid = tools.LineSplit.split(s, "\t", 0);
		String merchant = tools.LineSplit.split(s, "\t", 1);
		String mid = tools.LineSplit.split(merchant, "<@>", 0);
		context.write(new Text(uid), new Text(mid));
	}

}
