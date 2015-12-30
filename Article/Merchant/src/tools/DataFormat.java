package tools;

public class DataFormat {
	
	public static String dataFormat(int a){
		if(a<15){
			return "10";
		}else if(a<1000){
			return (a/10+1)*10 + "";
		}else if(a<9500){
			a = a/10;
			int b = a%10;
			if(b>=5)return (a/10+1)*100 + "";
			else return (a/10)*100 + "";
		}else if(a<10000){
			return "10000";
		}else if(a<100000){
			a = a/100;
			int b = a%10;
			int c = (a/10)%10;
			if(c>0){
				if(b < 5)return (a/100)*10000 + c*1000 + "";
				else return (a/100)*10000 + (c+1)*1000 + "";
			}else return (a/100)*10000 + "";
		}else{
			return (a/10000)*10000 + "";
		}
	}
	
}
