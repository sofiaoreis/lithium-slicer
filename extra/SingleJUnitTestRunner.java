import org.junit.runner.JUnitCore;
import org.junit.runner.Request;
import org.junit.runner.Result;

import org.junit.runner.notification.Failure;

import java.util.List;

public class SingleJUnitTestRunner {
    public static void main(String... args) throws ClassNotFoundException {
        String[] classAndMethod = args[0].split("#");
        Request request = Request.method(Class.forName(classAndMethod[0]),
                classAndMethod[1]);
        Result result = new JUnitCore().run(request);
        List<Failure> failures = result.getFailures();
        if (failures.isEmpty()) {
            System.out.println("No failures");
        } else if (failures.size() > 1) {
            System.out.println("There should be one failure at most");            
        } else {
            Failure failure = failures.get(0);
            System.out.println(failure.toString());
        }
    }
}
