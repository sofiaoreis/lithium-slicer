package example;

import org.junit.Test;
import org.junit.Assert;
import org.junit.Before;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

import java.util.Arrays;

public class BinarySearchTreeTest {
    
    BinarySearchTree b;

    @Before
    public void setup() {
        b = new BinarySearchTree();
        b.insert(3);
        b.insert(98);        
        b.insert(8);
        b.insert(100);        
        b.insert(101);        
    }
    
    @Test
    public void elementFound() {
        Assert.assertTrue(b.find(3));
    }

    @Test
    public void elementNotFound() {
        Assert.assertFalse(b.find(99));
    }

    @Test
    public void deleteExisting() {
        Assert.assertTrue(b.delete(8));
        StringBuffer sb = new StringBuffer();
        b.display(b.root, sb);
        Assert.assertEquals("3 98 100 101", sb.toString().trim());
    }
    
    @Test
    public void deleteMissing() {
        Assert.assertTrue(b.delete(100));
    }            
    
}
