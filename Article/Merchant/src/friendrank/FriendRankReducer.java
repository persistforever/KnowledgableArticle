package friendrank;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.Week;

public class FriendRankReducer extends Reducer<Text, Text, Text, Text> {

	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {

		String today = context.getConfiguration().get("today");
		double score = 0.0;
		int num = 0;
		for (Text v : value) {
			int datespan = Week.getDateSpan(v.toString(), today);
			score += 1.0 * Math.exp(1.0 * (90 - datespan) / 90.0);
			num += 1;
		}
		String uin = tools.LineSplit.split(key.toString(), "\t", 0);
		String mid = tools.LineSplit.split(key.toString(), "\t", 1);
		context.write(new Text(uin), new Text(String.valueOf(mid) + "\t"
				+ String.valueOf(score) + "\t" + String.valueOf(num)));
	}

}
