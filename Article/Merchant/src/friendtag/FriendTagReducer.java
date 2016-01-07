package friendtag;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;


public class FriendTagReducer extends Reducer<Text, Text, Text, Text>{
	
	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {

		ArrayList<String> pid = new ArrayList<String>(); // placeID
		ArrayList<String> uid = new ArrayList<String>(); // userID
		
		for(Text v:value) {
			String x = v.toString().trim();
			String type = x.substring(0, 1);
			String id = x.substring(1);
			
			if (type.equals("F")) {
				uid.add(id);
			}
			else if (type.equals("D")) {
				pid.add(id);
			}
		}
		
		if(uid.isEmpty() || pid.isEmpty()) {
			return;
		}
		for(String u:uid) {
			for(String p:pid) {
				context.write(new Text(u), new Text(p));
			}
		}
	}
	
}
