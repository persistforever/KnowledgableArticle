package userlevel;

import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.HadoopFileOperation;
import tools.LineSplit;

public class UserLevelReducer extends Reducer<Text, Text, Text, Text>{
	HashMap<String, Double> levelmap = new HashMap<String, Double>();

	public class LevelMapReader implements
			HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 4) {
				String mid = LineSplit.split(s, "\t", 1);
				Double level = 0.0; 
				if (!LineSplit.split(s, "\t", 3).equals("")) {
					level = Double.parseDouble(LineSplit.split(s, "\t", 3));
				}
				if (!(UserLevelReducer.this.levelmap.containsKey(mid)))
					UserLevelReducer.this.levelmap.put(mid, level);
			}
		}
	}

	protected void setup(Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		LevelMapReader levelMapReader = new LevelMapReader();

		HadoopFileOperation.ReducerReadFile(context, "dictpath", levelMapReader);
	}

	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context) throws IOException,
			InterruptedException {
		double score = 0.0;
		int level = 0;
		int num = 0;
		for(Text v:value){
			if (this.levelmap.containsKey(v.toString())) {
				score += this.levelmap.get(v.toString());
				num ++;
			}
		}
		if (num != 0) {
			score = 1.0 * score / num;
		}
		else {
			score = 0.0;
		}
		if (score <= 50.0) {
			level = 1;
		}
		else if(score <= 100.0) {
			level = 2;
		}
		else if(score <= 200.0) {
			level = 3;
		}
		else if(score <= 500.0) {
			level = 4;
		}
		else {
			level = 5;
		}
		context.write(new Text(key), new Text(String.valueOf(level)));
	}

}
