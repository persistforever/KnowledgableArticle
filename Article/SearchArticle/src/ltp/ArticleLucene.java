package ltp;

import java.util.ArrayList;
import java.util.List;
import edu.hit.ir.ltp4j.*;

public class ArticleLucene {
	public static void main(String[] args) {
		if (Segmentor.create("D://download/ltp4j-master/ltp4j-master/ltp_data/cws.model") < 0) {
			System.err.println("load failed");
			return;
		}

		String sent = "我是中国人";
		List<String> words = new ArrayList<String>();
		int size = Segmentor.segment(sent, words);

		for (int i = 0; i < size; i++) {
			System.out.print(words.get(i));
			if (i == size - 1) {
				System.out.println();
			} else {
				System.out.print("\t");
			}
		}
		Segmentor.release();
	}
}
