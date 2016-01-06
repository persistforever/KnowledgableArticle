package validfrd;

import java.io.IOException;
import java.util.HashSet;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class ValidFrdMapper extends Mapper<Object, Text, Text, Text>{
	String input = "";
	HashSet<Long> validusers = new HashSet<Long>();

	@Override
	protected void map(Object key, Text value,
			Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String s = value.toString();
		int index = s.indexOf("\t");
		String uin = s.substring(0, index).trim();
		if(this.validusers.contains(Long.parseLong(uin))){
			context.write(new Text(uin), new Text(s.substring(index+1)));
		}
	}

	public class ValidUsers implements tools.HadoopFileOperation.ReadOneLineInterface {
		// attributes
		HashSet<Long> users = new HashSet<Long>();

		// methods
		public void ReadOneLine(String s) {
        	int index = s.indexOf("\t");
        	String uin = s.substring(0, index);
        	long unsignedValue = Long.parseLong(uin);
        	users.add(unsignedValue);
		}
	}
	
	@Override
	protected void setup(Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		for(int i=0 ; i<Integer.parseInt(context.getConfiguration().get("length")) ; i++) {
			input = "usertag"+String.valueOf(i);
			
			ValidUsers validUsers = new ValidUsers();
			validUsers.users = this.validusers;
			tools.HadoopFileOperation.MapperReadFile(context, input, validUsers);
		}
	}
	
}
