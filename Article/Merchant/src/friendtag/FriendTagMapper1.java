package friendtag;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class FriendTagMapper1 extends Mapper<Object, Text, Text, Text>{

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException 
	{
		
		String s = value.toString();
		if(s.trim().length() == 0)
			return;
		
		String uin = tools.LineSplit.split(value.toString(), "\t", 0);
		String fidlist = tools.LineSplit.split(value.toString(), "\t", 1);
		ArrayList<String> fidList = tools.LineSplit.split(fidlist, " ");
		HashSet<String> qcfidList = new HashSet<String>();
		for(String fid:fidList) {
			if (!qcfidList.contains(fid)) {
				qcfidList.add(fid);
			}
		}

		for(String fid:qcfidList) {
			if(fid.equals("0"))continue;
			context.write(new Text(uin), new Text("F"+fid));			
		}
	}
}


