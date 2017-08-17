
import java.awt.*;
import java.awt.color.*;
import java.awt.geom.*;
import javax.swing.*;
import java.awt.event.*;
import javax.swing.event.*;

public class Halo {

    public float pointradius = 2;
    public Color foreground = new Color(0,0,0);

    public float ringwidth;    
    public int   nrings;
    public int   nrays;
    public float theta;
    public float x;
    public float y;
    
    public Halo(float width, int n, int k, float h, float x, float y) {
        this.x = x;
        this.y = y;
        this.nrings = n;
        this.ringwidth = width;
        this.nrays = k;
        this.theta = h;
    }
    
    public void draw(Graphics2D G) {
        G.setColor(foreground);
        G.draw(new Ellipse2D.Float(x-pointradius,y-pointradius,pointradius*2,pointradius*2));
        for (int i=1; i<=nrings; i++) {
            //G.draw(new Ellipse2D.Float(this.x-i*ringwidth,this.y-i*ringwidth,2*i*ringwidth,2*i*ringwidth));
        }
        for (int i=0; i<nrays; i++) {
            float h = (float)((i*2*Math.PI)/nrays)+theta;
            float ct = (float)Math.cos(h);
            float st = (float)Math.sin(h);
            G.draw(new Line2D.Float(x,y,x+ct*nrings*ringwidth,y+st*nrings*ringwidth));
            for (int j=1; j<=nrings; j++) {
                float px = x + ct*j*ringwidth;
                float py = y + st*j*ringwidth;
                //G.draw(new Ellipse2D.Float(px-pointradius,py-pointradius,pointradius*2,pointradius*2));
            }
        }
    }
    
    public Point2D.Float[] points() {
        Point2D.Float[] result = new Point2D.Float[nrings*nrays+1];
        int ii = 0;
        result[ii++] = new Point2D.Float(x,y);
        for (int i=0; i<nrays; i++) {
            float h = (float)((i*2*Math.PI)/nrays)+theta;
            float ct = (float)Math.cos(h);
            float st = (float)Math.sin(h);
            for (int j=1; j<=nrings; j++) {
                float px = x + ct*j*ringwidth;
                float py = y + st*j*ringwidth;
                result[ii++] = new Point2D.Float(px,py);
            }
        }
        return result;
    }
}
    
