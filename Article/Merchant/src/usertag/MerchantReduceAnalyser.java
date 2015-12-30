package usertag;

import org.apache.hadoop.io.Text;

public class MerchantReduceAnalyser extends ReduceAnalyse{

	@Override
	public boolean analyse(Text key, Iterable<Text> value) {

		for(Text v:value) {
			if(tools.LineSplit.split(v.toString(), "\t", 1).equals("PY")) {
				this.key.add(tools.LineSplit.split(v.toString(), "\t", 0));
			}
			else {
				this.value.add(v.toString()+"<@>"+key.toString());
			}
		}
		return true;
	}
}
