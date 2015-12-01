package article.article_collectnum;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class ArticleMapper extends Mapper<Object, Text, Text, Text> {
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String line = new String(value.getBytes(), 0, value.getLength(), "GB18030");
		if (line.split("\t").length >= 11) {
			String id = line.split("\t")[0];
			String collect = line.split("\t")[8];
			context.write(new Text(id), new Text(collect));
		}
	}
}