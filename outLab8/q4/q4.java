import java.text.SimpleDateFormat;
import java.util.Date;
import java.lang.*;
class timeThread implements Runnable
{
	Thread t;
 	public void run()
 	{
 	
 	while (true)
 	 {  
 	  Date d = new Date();
 	  SimpleDateFormat sdate = new SimpleDateFormat("hh:mm:ss");
 	   try
 	   {  t.sleep(1000);
 	      System.out.println(sdate.format(d));
 	   }
	  catch (InterruptedException e)
	   { break;}
	 }
	}
}
class q4{
	public static void main(String args[])
	{
	Thread t1 = new Thread(new timeThread());
	t1.start();
	}
}
