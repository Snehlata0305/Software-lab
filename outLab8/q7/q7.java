import java.io.*; 
import java.lang.*; 
import java.util.*; 
import java.util.List;
import java.util.stream.Collectors;


public class q7 {
	public static void main(String[] args) {
		if(args.length > 0) {
            try{
                File file = new File(args[0]);
                Scanner myReader = new Scanner(file);

                String totalData = "";
                while (myReader.hasNextLine()) {
                    String data = myReader.nextLine();
                    data = data.replaceAll("\\p{Punct}",""); 
                    data = data.replaceAll("\\b\\band\\b", "");
                    data = data.replaceAll("\\bthe\\b", "");
                    data = data.replaceAll("\\bis\\b", "");
                    data = data.replaceAll("\\bin\\b", "");
                    data = data.replaceAll("\\bat\\b", "");
                    data = data.replaceAll("\\bof\\b", "");
                    data = data.replaceAll("\\bhis\\b", "");
                    data = data.replaceAll("\\bher\\b", "");
                    data = data.replaceAll("\\bhim\\b", "");
                    totalData = totalData +" "+ data;
                    }

                StringTokenizer st1 = new StringTokenizer(totalData);
                ArrayList<String> dataArray = new ArrayList<>();
                while (st1.hasMoreTokens()){
                	dataArray.add(st1.nextToken());
                }

                HashSet<String> dataSet = new HashSet<String>(dataArray);
                HashMap<String, Integer> dataMap = new HashMap<String, Integer>();
                for (String str : dataSet) {
                	dataMap.put(str, Collections.frequency(dataArray, str));
        		}

                dataMap.entrySet().stream().sorted(Map.Entry.<String, Integer>comparingByValue().reversed().thenComparing(Map.Entry::getKey)).forEach(x -> System.out.println(x.getKey()+","+x.getValue()));
            myReader.close();
            }
            catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
            }
        }


    }
}   