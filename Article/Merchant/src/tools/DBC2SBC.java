package tools;

public class DBC2SBC {

	
	public static String replaceDBC2SBC(String input) {
	    long lowerBound = 0xff01;
	    long upperBound = 0xff5f;
	    char[] cs = input.toCharArray();
	    for(int i = 0;i<cs.length;i++){
	    	long cl = (long)cs[i];
	    	if(cl == 0x3000 || (cl>=lowerBound && cl<= upperBound)){
	    		cs[i] -=  0xfee0;
	    	}
	    }
	    
	    return new String(cs);
	}
	
	public static void main(String[] args){
		String s = "";
		s = replaceDBC2SBC(s);
		System.out.println(s);
	}
}
