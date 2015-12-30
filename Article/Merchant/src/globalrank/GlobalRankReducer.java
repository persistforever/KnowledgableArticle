package globalrank;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.Week;

public class GlobalRankReducer extends Reducer<Text, Text, Text, Text>{

	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context) throws IOException,
			InterruptedException {
		String today = context.getConfiguration().get("today");
		double score = 0.0;
		for(Text v:value){
			int datespan = Week.getDateSpan(today, v.toString());
			score += 1.0 * Math.exp(1.0 * (90 - datespan) / 90.0);
		}
		context.write(new Text(key), new Text(String.valueOf(score)));
	}

}
