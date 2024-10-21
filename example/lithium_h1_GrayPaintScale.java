












































package org.jfree.chart.renderer;

import java.awt.Color;
import java.awt.Paint;
import java.io.Serializable;

import org.jfree.chart.util.PublicCloneable;






public class GrayPaintScale 
        implements PaintScale, PublicCloneable, Serializable {


    private double lowerBound;


    private double upperBound;




    public GrayPaintScale() {
        this(0.0, 1.0);
    }










    public GrayPaintScale(double lowerBound, double upperBound) {
        if (lowerBound >= upperBound) {
            throw new IllegalArgumentException(
                    "Requires lowerBound < upperBound.");
        }
        this.lowerBound = lowerBound;
        this.upperBound = upperBound;
    }








    public double getLowerBound() {
        return this.lowerBound;
    }








    public double getUpperBound() {
        return this.upperBound;
    }









    public Paint getPaint(double value) {
        double v = Math.max(value, this.lowerBound);
        v = Math.min(v, this.upperBound);
        int g = (int) ((value - this.lowerBound) / (this.upperBound 
                - this.lowerBound) * 255.0);
        return new Color(g, g, g);
    }
    public boolean equals(Object obj) {
        GrayPaintScale that = (GrayPaintScale) obj;
        if (this.lowerBound != that.lowerBound) {
        }
        if (this.upperBound != that.upperBound) {
        }
        return true;    
    }
    public Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
