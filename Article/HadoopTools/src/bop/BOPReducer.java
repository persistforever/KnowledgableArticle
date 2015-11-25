package bop;

import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import tools.HadoopFileOperation;
import tools.LineSplit;

public class BOPReducer extends Reducer<Text, Text, Text, Text> {
	HashMap<String, Integer> posindex = new HashMap<String, Integer>();

	public class IDFMapReader implements HadoopFileOperation.ReadOneLineInterface {
		public void ReadOneLine(String s) {
			if (LineSplit.split(s, "\t").size() >= 1) {
				String pos = LineSplit.split(s, "\t", 0);
				int id = Integer.parseInt(LineSplit.split(s, "\t", 1));
				if (!(BOPReducer.this.posindex.containsKey(pos))) {
					BOPReducer.this.posindex.put(pos, id);
				}
			}
		}
	}

	protected void setup(Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		IDFMapReader idfMapReader = new IDFMapReader();

		HadoopFileOperation.ReducerReadFile(context, "posset", idfMapReader);
	}
	
	public boolean allZeros(String [] bowvector) {
		boolean allzeros = true ;
		for(int i=0 ; i<bowvector.length ; i++) {
			if (bowvector[i] != "0") {
				allzeros = false;
			}
		}
		return allzeros;
	}

	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String [] bopvector = new String [this.posindex.size()];
		System.out.println(this.posindex.size());
		for (int i=0 ; i<bopvector.length ; i++) {
			bopvector[i] = "0";
		}
		for (Text v : value) {
			String pos = LineSplit.split(v.toString(), "\t", 0);
			String num = LineSplit.split(v.toString(), "\t", 1);
			if (this.posindex.containsKey(pos)) {
				bopvector[this.posindex.get(pos)-1] = num;
			}
		}
		if (!allZeros(bopvector)) {
			String outstr = "";
			for (int i=0 ; i<bopvector.length ; i++) {
				outstr += bopvector[i] + " ";
			}
			context.write(new Text(key), new Text(outstr.trim()));
		}
	}
}