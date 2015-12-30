package usertag;

public abstract class SnsAnalyse {
	public String key = "";
	public String value = "";
	public abstract boolean analyse(String line);
	
}
