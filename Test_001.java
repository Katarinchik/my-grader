import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class Bai1TestRunner {

	@Test
	public void test() {
	int x;
		Program p = new Program();
		for (int i=0;i<10;i++)
		{
		x = (int) ( Math.random() * 100);
		assertEquals(solution(x), p.Puzzle(x));
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