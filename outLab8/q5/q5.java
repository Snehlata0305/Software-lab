import java.util.Scanner;
import java.util.ArrayList;

public class q5 {
	public static void main(String[] args) {
		Scanner inp = new Scanner(System.in);
		
		int numOfList = inp.nextInt();
		
		ArrayList<ArrayList<Integer>> ipList = new ArrayList<ArrayList<Integer>>();
		
		for(int i=0;i<numOfList;i++) {
			ArrayList<Integer> tempList = new ArrayList<Integer>();
			tempList.add(0);
			int numOfElem = inp.nextInt();
			for(int j=0;j<numOfElem;j++) {
				int elem = inp.nextInt();
				tempList.add(elem);
			}
			ipList.add(tempList);
		}
		
		String opStr = "";
		
		int numOfQuery = inp.nextInt();
		for(int k=0;k<numOfQuery;k++) {
			try{
				int listno = inp.nextInt();
				int elemno = inp.nextInt();
				opStr += ipList.get(listno-1).get(elemno)+"\n";
			}catch(IndexOutOfBoundsException e) {
				opStr += "ERROR!\n";
			}
		}
		System.out.println(opStr.trim());
	}
}
