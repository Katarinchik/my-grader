import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class Test_002 {

	@Test
	public void test() {
		Program p = new Program();
		assertEquals(1, p.Myfunc(1));
		assertEquals(1, p.Myfunc(2));
		assertEquals(2, p.Myfunc(3));
		assertEquals(3, p.Myfunc(4));
		assertEquals(5, p.Myfunc(5));
		assertEquals(8, p.Myfunc(6));
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
