package usertag;

public class MerchantSnsAnalyser extends SnsAnalyse{
	public boolean analyse(String line) {

		if (line.trim().length() == 0) {
			return false;
		}
		String tid = tools.LineSplit.split(line, "\t", 10).trim();
		if(tid.trim().length() == 0 || tid.trim().length() == 0) {
			return false;
		}
		this.key = tools.LineSplit.split(tid, " · ", 0).trim() +"<&>"+ tools.LineSplit.split(tid, " · ", 1).trim();
		this.value = tools.LineSplit.split(line, "\t", 1).trim();	
		
		if(this.key.trim().length() == 0 || this.value.trim().length() == 0) {
			return false;
		}
		else {
			long unsignedValue = Long.parseLong(this.value) & Integer.MAX_VALUE; 
			unsignedValue |= 0x80000000L;
			this.value = String.valueOf(unsignedValue) + "\tPY";
			return true;
		}
	}
}
