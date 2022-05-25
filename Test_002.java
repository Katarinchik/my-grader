import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import java.lang.Math;
public class Test_002 {

	@Test
	public void test() {
	int x;
		Program p = new Program();
		for (int i=0;i<10;i++)
		{
		x = (int) ( Math.random() * 100);
		assertEquals(solution(x), p.Myfunc(x));
		}
		
	}
	public int solution(int x) {
		int n0 = 1;
		int n1 = 1;
		int n2;
		for(int i = 3; i <= x; i++){
			n2=n0+n1;
			n0=n1;
			n1=n2;
		}
		return n2 ;
	}

	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(Test_002.class);
		for (Failure failure : result.getFailures()) {
			String myFailure = new String(failure.toString());
			myFailure = myFailure.replace("<", " ");
			myFailure = myFailure.replace(">", " ");
			System.out.println(myFailure);			
		}
		System.out.println(result.wasSuccessful());
	}

}
