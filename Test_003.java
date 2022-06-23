import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import java.lang.Math;
public class Test_003{ 

	@Test
	public void test() {
	int x,y;
		Program p = new Program();
		for (int i=0;i<10;i++)
		{
		x = (int) ( Math.random() * 100);
		y = (int) ( Math.random() * 100);
		System.out.println((p.Myfunc(x,y)==solution(x,y)) +" Myfunc("+x+","+y+") "+p.Myfunc(x,y)+" "+ solution(x,y));
		}
		
	}
	public int solution(int x, int y) {
		return x+y ;
	}

	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(Test_003.class);
				
		}
		
	}

}
