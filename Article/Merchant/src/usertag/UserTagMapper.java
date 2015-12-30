package usertag;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class UserTagMapper extends Mapper<Object, Text, Text, Text> {

	protected SnsAnalyse sa = null;

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String line = value.toString();
		if (sa.analyse(line)) {
			context.write(new Text(sa.key), new Text(sa.value));
		}

	}

	@Override
	protected void setup(Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		@SuppressWarnings("unchecked")
		Class<? extends SnsAnalyse> clazz = (Class<? extends SnsAnalyse>) context
				.getConfiguration().getClass("snsanalyser", SnsAnalyse.class);
		try {
			sa = clazz.newInstance();
		} catch (Exception e) {
			System.err.println("Illegal class!");
			e.printStackTrace();
		}

	}
}
