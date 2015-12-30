package tools;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * @author crycao
 * @methods ReducerReadFile - read file from reducer
 * @methods	MapperReadFile - read file from mapper
 * @interface ReadOneLineInterface - detail operation in read file methods
 *
 */
public class HadoopFileOperation {
	
	/**
	 * @param context - global infomation between jobtracker and tasktracker
	 * @param path - read file from this directory
	 * @param interfc - detail operation in read file, handle each line
	 */
	@SuppressWarnings("rawtypes")
	public static void ReducerReadFile(Reducer.Context context, String path, ReadOneLineInterface interfc)
			throws IOException, InterruptedException {
		String ctpvPath = context.getConfiguration().get(path);
		FileSystem fs = FileSystem.get(context.getConfiguration());
		Path filePath = new Path(ctpvPath);
		FileStatus status[] = fs.listStatus(filePath);
		for(int i=0 ; i<status.length ; i++) {
			Path inFile = new Path(status[i].getPath().toString());
			if(status[i].isDir()) {
				continue;
			}
			FSDataInputStream fin = fs.open(inFile);
			BufferedReader input = new BufferedReader(new InputStreamReader(fin, "UTF-8"));
			
			String s="";
			while((s = input.readLine()) != null) {
				interfc.ReadOneLine(s);
			}
            // release  
            if (input != null) {  
                input.close();  
                input = null;  
            }  
            if (fin != null) {  
                fin.close();  
                fin = null;  
            }  
            inFile = null;
		}
	}
	
	/**
	 * @param context - global infomation between jobtracker and tasktracker
	 * @param path - read file from this directory
	 * @param interfc - detail operation in read file, handle each line
	 */
	@SuppressWarnings("rawtypes")
	public static void MapperReadFile(Mapper.Context context, String path, ReadOneLineInterface interfc)
			throws IOException, InterruptedException {
		String ctpvPath = context.getConfiguration().get(path);
		FileSystem fs = FileSystem.get(context.getConfiguration());
		Path filePath = new Path(ctpvPath);
		FileStatus status[] = fs.listStatus(filePath);
		for(int i=0 ; i<status.length ; i++) {
			Path inFile = new Path(status[i].getPath().toString());
			if(status[i].isDir()) {
				continue;
			}
			FSDataInputStream fin = fs.open(inFile);
			BufferedReader input = new BufferedReader(new InputStreamReader(fin, "UTF-8"));
			
			String s="";
			while((s = input.readLine()) != null) {
				interfc.ReadOneLine(s);
			}
            // release  
            if (input != null) {  
                input.close();  
                input = null;  
            }  
            if (fin != null) {  
                fin.close();  
                fin = null;  
            }  
            inFile = null;
		}
	}
	
	/**
	 * @param path - delete this directory
	 * @param conf - configuration
	 */
	public static void DeleteDir(String path, Configuration conf) 
			throws IOException, ClassNotFoundException, InterruptedException {
		FileSystem fs = FileSystem.get(conf);
		Path p = new Path(path);
		if(fs.exists(p)) {
			fs.delete(p, true);
		}
	}
	
	public static String CatPath(String ...args) {
		String path = "";
		for(String arg:args) {
			path += arg + "/";
		}
		return path.substring(0, path.length()-1);
	}

	/**
	 * @author crycao
	 * @methods ReadOneLine - detail operation in read file, handle each line
	 *
	 */
	public interface ReadOneLineInterface {
		public void ReadOneLine(String s);
	}
}

