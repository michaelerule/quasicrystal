
import java.awt.*;
import java.awt.color.*;
import java.awt.geom.*;
import javax.swing.*;
import java.awt.event.*;
import javax.swing.event.*;

public class Halo {

    public static final boolean drawpoints = false;

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
        if (drawpoints) {
            G.draw(new Ellipse2D.Float(x-pointradius,y-pointradius,pointradius*2,pointradius*2));
            for (int i=1; i<=nrings; i++) {
                G.draw(new Ellipse2D.Float(this.x-i*ringwidth,this.y-i*ringwidth,2*i*ringwidth,2*i*ringwidth));
            }
            for (int i=0; i<nrays; i++) {
                float h = (float)((i*2*Math.PI)/nrays)+theta;
                float ct = (float)Math.cos(h);
                float st = (float)Math.sin(h);
                G.draw(new Line2D.Float(x,y,x+ct*nrings*ringwidth,y+st*nrings*ringwidth));
                for (int j=1; j<=nrings; j++) {
                    float px = x + ct*j*ringwidth;
                    float py = y + st*j*ringwidth;
                    G.draw(new Ellipse2D.Float(px-pointradius,py-pointradius,pointradius*2,pointradius*2));
                }
            }
        } else {
            for (int i=1; i<=nrings; i++) {
                G.draw(new Ellipse2D.Float(this.x-i*ringwidth,this.y-i*ringwidth,2*i*ringwidth,2*i*ringwidth));
            }
            for (int i=0; i<nrays; i++) {
                float h = (float)((i*2*Math.PI)/nrays)+theta;
                float ct = (float)Math.cos(h);
                float st = (float)Math.sin(h);
                G.draw(new Line2D.Float(x,y,x+ct*nrings*ringwidth,y+st*nrings*ringwidth));
            }
            int stellation = (int)((nrays-1)/2);
            for (int ist=1; ist<=stellation; ist++) {
                // Add midpoints
                for (int i=0; i<nrays; i++) {
                    float h1 = (float)(((i+0)*2*Math.PI)/nrays)+theta;
                    float h2 = (float)(((i+ist)*2*Math.PI)/nrays)+theta;
                    float ct1 = (float)Math.cos(h1);
                    float st1 = (float)Math.sin(h1);
                    float ct2 = (float)Math.cos(h2);
                    float st2 = (float)Math.sin(h2);
                    
                    for (int j=1; j<=nrings; j++) {
                        float px1 = x + ct1*j*ringwidth;
                        float py1 = y + st1*j*ringwidth;
                        float px2 = x + ct2*j*ringwidth;
                        float py2 = y + st2*j*ringwidth;
                        G.draw(new Line2D.Float(px1,py1,px2,py2));
                    }
                }
            }
        }
    }
    
    public Point2D.Float[] points() {
        Point2D.Float[] result = new Point2D.Float[nrings*nrays*3+1];
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
        int stellation = (int)((nrays-1)/2);
        for (int ist=1; ist<=stellation; ist++) {
            // Add midpoints
            for (int i=0; i<nrays; i++) {
                float h1 = (float)(((i+0)*2*Math.PI)/nrays)+theta;
                float h2 = (float)(((i+ist)*2*Math.PI)/nrays)+theta;
                float ct = (float)(Math.cos(h1) + Math.cos(h2))*0.5f;
                float st = (float)(Math.sin(h1) + Math.sin(h2))*0.5f;
                for (int j=1; j<=nrings; j++) {
                    float px = x + ct*j*ringwidth;
                    float py = y + st*j*ringwidth;
                    result[ii++] = new Point2D.Float(px,py);
                }
            }
        }
        return result;
    }
}
    
