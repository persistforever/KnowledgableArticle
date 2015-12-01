package article.gzh_avg_collectnum;

import java.io.IOException;
import java.util.ArrayList;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class AvgCollectReducer extends Reducer<Text, Text, Text, Text> {
	
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		ArrayList<String []> articleList = new ArrayList<String []>();
		int follow = 0;
		for (Text v : value) {
			if (v.toString().split("<#>").length == 1) {
				if (Integer.parseInt(v.toString()) > follow) {
					follow = Integer.parseInt(v.toString());
				}
			}
			else if (v.toString().split("<#>").length >= 2) {
				String articleId = v.toString().split("<#>")[0];
				String collect = v.toString().split("<#>")[1];
				String[] article = {articleId, collect};
				articleList.add(article);
			}
		}
		if (articleList.size() >= Integer.parseInt(context.getConfiguration().get("article")) && 
				follow > Integer.parseInt(context.getConfiguration().get("user"))) {
			for (String [] article: articleList) {
				context.write(new Text(article[0]), 
						new Text(article[1] + "\t" + String.valueOf(follow)));
			}
		}
	}
}