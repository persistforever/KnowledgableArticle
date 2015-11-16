package tools;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Method;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class HadoopFileOperation {
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

	public static String MapperGetDate(Mapper.Context context)
			throws IOException {
		InputSplit split = context.getInputSplit();
		Class splitClass = split.getClass();
		FileSplit fileSplit = null;
		if (splitClass.equals(FileSplit.class)) {
			fileSplit = (FileSplit) split;
		} else if (splitClass.getName().equals(
				"org.apache.hadoop.mapreduce.lib.input.TaggedInputSplit")) {
			try {
				Method getInputSplitMethod = splitClass.getDeclaredMethod(
						"getInputSplit", new Class[0]);
				getInputSplitMethod.setAccessible(true);
				fileSplit = (FileSplit) getInputSplitMethod.invoke(split,
						new Object[0]);
			} catch (Exception e) {
				throw new IOException(e);
			}
		}
		String path = fileSplit.getPath().toString();
		return LineSplit.split(path, "/", 8);
	}

	public static abstract interface ReadOneLineInterface {
		public abstract void ReadOneLine(String paramString);
	}
}