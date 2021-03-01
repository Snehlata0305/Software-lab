import java.util.*;

class q1
{
  public static void main(String args[])
  {
    Scanner sc= new Scanner(System.in);
    String input = sc.nextLine();
    String inputs[] = input.split(",");
    int l = inputs.length;
    
    int start = Integer.parseInt(inputs[l-2].trim());
    int end = Integer.parseInt(inputs[l-1].trim());
    System.out.println(input.substring(start,end+1));
  }
}
