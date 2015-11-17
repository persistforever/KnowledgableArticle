package tools;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.io.compress.GzipCodec;
import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.ReflectionUtils;

public class GbkOutputFormat<K, V> extends FileOutputFormat<K, V> {
	public static String SEPERATOR = "mapreduce.output.textoutputformat.separator";

	public RecordWriter<K, V> getRecordWriter(TaskAttemptContext job)
			throws IOException, InterruptedException {
		Configuration conf = job.getConfiguration();
		boolean isCompressed = getCompressOutput(job);
		String keyValueSeparator = conf.get(SEPERATOR, "\t");
		CompressionCodec codec = null;
		String extension = "";
		if (isCompressed) {
		      Class<? extends CompressionCodec> codecClass = 
		    	        getOutputCompressorClass(job, GzipCodec.class);
		    	      codec = (CompressionCodec) ReflectionUtils.newInstance(codecClass, conf);
		    	      extension = codec.getDefaultExtension();
		}
		Path file = getDefaultWorkFile(job, extension);
		FileSystem fs = file.getFileSystem(conf);
		if (!(isCompressed)) {
			FSDataOutputStream fileOut = fs.create(file, false);
		      return new LineRecordWriter<K, V>(fileOut, keyValueSeparator);
		}
		FSDataOutputStream fileOut = fs.create(file, false);
	      return new LineRecordWriter<K, V>(new DataOutputStream
                  (codec.createOutputStream(fileOut)),
                  keyValueSeparator);
	}

	protected static class LineRecordWriter<K, V> extends RecordWriter<K, V> {
		private static final String gbk = "gb18030";
		private static final byte[] newline;
		protected DataOutputStream out;
		private final byte[] keyValueSeparator;

		static {
			try {
				newline = "\n".getBytes(gbk);
			} catch (UnsupportedEncodingException uee) {
				throw new IllegalArgumentException(
						"can't find gb18030 encoding");
			}
		}

		public LineRecordWriter(DataOutputStream out, String keyValueSeparator) {
			this.out = out;
			try {
				this.keyValueSeparator = keyValueSeparator.getBytes(gbk);
			} catch (UnsupportedEncodingException uee) {
				throw new IllegalArgumentException(
						"can't find gb18030 encoding");
			}
		}

		public LineRecordWriter(DataOutputStream out) {
			this(out, "\t");
		}

		private void writeObject(Object o) throws IOException {
			if (!(o instanceof Text)) {
				return;
			}

			this.out.write(o.toString().getBytes(gbk));
		}

		public synchronized void write(K key, V value) throws IOException {
			boolean nullKey = (key == null) || (key instanceof NullWritable);
			boolean nullValue = (value == null)
					|| (value instanceof NullWritable);
			if ((nullKey) && (nullValue)) {
				return;
			}
			if (!(nullKey)) {
				writeObject(key);
			}
			if ((!(nullKey)) && (!(nullValue))) {
				this.out.write(this.keyValueSeparator);
			}
			if (!(nullValue)) {
				writeObject(value);
			}
			this.out.write(newline);
		}

		public synchronized void close(TaskAttemptContext context)
				throws IOException {
			this.out.close();
		}
	}
}