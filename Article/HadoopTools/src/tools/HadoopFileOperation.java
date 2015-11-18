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

public class HadoopFileOperation {
	@SuppressWarnings("rawtypes")
	public static void ReducerReadFile(Reducer.Context context, String path,
			ReadOneLineInterface interfc) throws IOException,
			InterruptedException {
		String ctpvPath = context.getConfiguration().get(path);
		FileSystem fs = FileSystem.get(context.getConfiguration());
		Path filePath = new Path(ctpvPath);
		FileStatus[] status = fs.listStatus(filePath);
		for (int i = 0; i < status.length; ++i) {
			Path inFile = new Path(status[i].getPath().toString());
			if (status[i].isDir()) {
				continue;
			}
			FSDataInputStream fin = fs.open(inFile);
			BufferedReader input = new BufferedReader(new InputStreamReader(
					fin, "GB18030"));

			String s = "";
			while ((s = input.readLine()) != null) {
				interfc.ReadOneLine(s);
			}

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

	@SuppressWarnings("rawtypes")
	public static void MapperReadFile(Mapper.Context context, String path,
			ReadOneLineInterface interfc) throws IOException,
			InterruptedException {
		String ctpvPath = context.getConfiguration().get(path);
		FileSystem fs = FileSystem.get(context.getConfiguration());
		Path filePath = new Path(ctpvPath);
		FileStatus[] status = fs.listStatus(filePath);
		for (int i = 0; i < status.length; ++i) {
			Path inFile = new Path(status[i].getPath().toString());
			if (status[i].isDir()) {
				continue;
			}
			FSDataInputStream fin = fs.open(inFile);
			BufferedReader input = new BufferedReader(new InputStreamReader(
					fin, "UTF-8"));

			String s = "";
			while ((s = input.readLine()) != null) {
				interfc.ReadOneLine(s);
			}

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

	public static void DeleteDir(String path, Configuration conf)
			throws IOException, ClassNotFoundException, InterruptedException {
		FileSystem fs = FileSystem.get(conf);
		Path p = new Path(path);
		if (fs.exists(p))
			fs.delete(p, true);
	}

	public static String CatPath(String[] args) {
		String path = "";
		for (String arg : args) {
			path = path + arg + "/";
		}
		return path.substring(0, path.length() - 1);
	}

	public static abstract interface ReadOneLineInterface {
		public abstract void ReadOneLine(String paramString);
	}
}