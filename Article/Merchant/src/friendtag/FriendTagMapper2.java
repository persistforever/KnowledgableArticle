package friendtag;

import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class FriendTagMapper2 extends Mapper<Object, Text, Text, Text> {

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String uin = tools.LineSplit.split(value.toString(), "\t", 0);
		String mid = tools.LineSplit.split(value.toString(), "\t", 1);
		String time = tools.LineSplit.split(value.toString(), "\t", 2);
		context.write(new Text(uin), new Text("D" + mid + "\t" + time));
	}
}
