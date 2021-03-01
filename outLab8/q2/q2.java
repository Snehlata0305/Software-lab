import java.util.Arrays;
import java.util.HashMap;
import java.util.Scanner; 
import java.util.Collections;

public class q2 {
	public static void frequencyEle(int arrayElement[], int number) { 
        HashMap<Integer, Integer> arrayHash = new HashMap<Integer, Integer>(); 
  
        for (int i=0; i<number; i++) { 
            if (arrayHash.containsKey(arrayElement[i])) { 
                arrayHash.put(arrayElement[i], arrayHash.get(arrayElement[i]) + 1); 
            } 
            else { 
                arrayHash.put(arrayElement[i], 1); 
            } 
        } 
        int maxValue = Collections.max(arrayHash.values());
        System.out.println(maxValue);
    } 
	public static void main(String[] args) {
		Scanner size = new Scanner(System.in);
		int number = size.nextInt();
		int [] arrayElement = new int[number];
    	for (int i = 0; i < number; i++){
    		arrayElement[i] = size.nextInt();
    	}
    	frequencyEle(arrayElement, number);
	}
}