package usertag;

import java.io.IOException;
import java.util.ArrayList;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class UserTagReducer extends Reducer<Text, Text, Text, Text>{
	
	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context) throws IOException,
			InterruptedException {
		if(ua.analyse(key, value)){
			for(String k: ua.key)
				for(String v:ua.value)
					context.write(new Text(k),
							new Text(v + "\t" + context.getConfiguration().get("today")));
		}
		ua.key.clear();
		ua.value.clear();
		
	}
	
	protected ReduceAnalyse ua = null;
	@Override
	protected void setup(Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		@SuppressWarnings("unchecked")
		Class<? extends ReduceAnalyse> clazz = (Class<? extends ReduceAnalyse>) context
				.getConfiguration().getClass("taganalyser", ReduceAnalyse.class);
		try {
			ua = clazz.newInstance();
			ua.key = new ArrayList<String>();
			ua.value = new ArrayList<String>();
		} catch (Exception e) {
			System.err.println("Illegal class!");
			e.printStackTrace();
		}
	}

}
