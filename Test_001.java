import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import java.lang.Math;
public class Test_001 {

	@Test
	public void test() {
		int x;
		Program p = new Program();
		for (int i=0;i<10;i++)
		{
		x = (int) ( Math.random() * 15+1);
		
		System.out.println((p.Myfunc(x)==solution(x)) +" Myfunc("+x+") "+p.Myfunc(x)+" "+ solution(x));
		
		}
		
		
	}
	public int solution(int x) {
		return x*2;
	}


	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(Test_001.class);
				
		}
		
	

}
