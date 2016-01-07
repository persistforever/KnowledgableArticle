package friendrank;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class FriendRankMapper extends Mapper<Object, Text, Text, Text> {

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String s = value.toString();
		String uin = tools.LineSplit.split(s, "\t", 0);
		String merchant = tools.LineSplit.split(s, "\t", 1);
		String mid = tools.LineSplit.split(merchant, "<@>", 0);
		String time = tools.LineSplit.split(s, "\t", 2);
		context.write(new Text(uin+"\t"+mid), new Text(time));
	}

}
