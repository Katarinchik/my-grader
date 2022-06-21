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
		string mes;
		Program p = new Program();
		for (int i=0;i<10;i++)
		{
		x = (int) ( Math.random() * 100);
		assertEquals(mes,solution(x), p.Myfunc(x));
		if(mes.isEmpty())
		System.out.println("True Myfunc " +solution(x));	
		}
		
	}
	public int solution(int x) {
		return x*2;
	}


	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(Test_001.class);
		for (Failure failure : result.getFailures()) {
			String myFailure = new String(failure.toString());
			myFailure = myFailure.replace("<", " ");
			myFailure = myFailure.replace(">", " "); 
			System.out.println(myFailure);			
		}
		System.out.println(result.wasSuccessful());
	}

}
