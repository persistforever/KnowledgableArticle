package usertag;

import java.util.ArrayList;
import org.apache.hadoop.io.Text;

public abstract class ReduceAnalyse {
	public ArrayList<String> key = null;
	public ArrayList<String> value = null;
	public abstract boolean analyse(Text key, Iterable<Text> value);
}
