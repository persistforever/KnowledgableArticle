package gzh_avg_collectnum;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.HadoopFileOperation;

public class AvgCollectReducer extends Reducer<Text, Text, Text, DoubleWritable> {
	HashMap<String, Integer[]> gzhDict = new HashMap<String, Integer[]>();
	Integer userNumberThreshold = 0;
	Integer articleNumberThreshold = 0;

	public class GzhReader implements HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String line) {
			if (line.split("\t").length >= 3) {
				String gzhId = line.split("\t")[0];
				Integer[] info = new Integer[2];
				info[0] = Integer.parseInt(line.split("\t")[2]);
				info[1] = 0;
				if (!(AvgCollectReducer.this.gzhDict.containsKey(gzhId))) {
					AvgCollectReducer.this.gzhDict.put(gzhId, info);
				}
			}
		}
	}

	protected void setup(Reducer<Text, Text, Text, DoubleWritable>.Context context)
			throws IOException, InterruptedException {
		GzhReader gzhReader = new GzhReader();

		HadoopFileOperation.ReducerReadFile(context, "gzh", gzhReader);
		this.userNumberThreshold = Integer.parseInt(context.getConfiguration().get("user"));
		this.articleNumberThreshold = Integer.parseInt(context.getConfiguration().get("article"));
	}

	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, DoubleWritable>.Context context)
			throws IOException, InterruptedException {
		ArrayList<String []> articleList = new ArrayList<String []>();
		for (Text v : value) {
			String articleId = v.toString().split("<#>")[0];
			Double collect = Double.parseDouble(v.toString().split("<#>")[1]); 
			if (this.gzhDict.containsKey(key.toString())) {
				collect = 1.0 * collect / this.gzhDict.get(key.toString())[0];
				this.gzhDict.get(key.toString())[1] ++;
				String[] article = {articleId, String.valueOf(collect)};
				articleList.add(article);
			}
		}
		if (this.gzhDict.containsKey(key.toString()) && 
				this.gzhDict.get(key.toString())[0] >= this.userNumberThreshold &&
				this.gzhDict.get(key.toString())[1] >= this.articleNumberThreshold) {
			for (String [] article: articleList) {
				context.write(new Text(article[0]), 
						new DoubleWritable(Double.parseDouble(article[1])));
			}
		}
	}
}