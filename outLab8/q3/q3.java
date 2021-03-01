import java.util.Scanner;
import java.util.regex.*;
import java.util.ArrayList;
import java.lang.*;
public class q3 {
	
	
	public boolean fun1(String myStr) {
		// write your code here
		return myStr!=null && myStr.chars().allMatch(Character::isLetterOrDigit) && myStr.length()<=5;

	}
	public boolean fun2(String myStr) {
		// write your code here
		return Pattern.compile("a*b+c").matcher(myStr).matches();
	}
	public boolean fun3(String myStr) {
		// write your code here
		return Pattern.compile("(?x) (?:  a  (?= a* (\\1?+ b))  )+ \\1").matcher(myStr).matches();
	}
	public ArrayList<String> fun4(String myStr, String patt) {
			// write your code here
		ArrayList<String> strings = new ArrayList<String>();
		int n,i,j,k,match_j=0;
		String str="",match="";
		n = myStr.length();
		i = 0;
		while(i<n)
		
		{
			match = "";

			for(j=i+1;j<=n;j++)
			{
				str = myStr.substring(i,j);
				//System.out.println(str);
				//System.out.println(patt);
				if(Pattern.compile(patt).matcher(str).matches())
				{
					match = str;
					match_j = j;
					//System.out.println(match);

				}
				//else break;
			}
		if(match!=null && !match.isEmpty())
		{
			strings.add(match);
			i = match_j;
		}
		else
			i = i+1;		
		}
		return strings;
	}
}  