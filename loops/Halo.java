
import java.awt.*;
import java.awt.color.*;
import java.awt.geom.*;
import javax.swing.*;
import java.awt.event.*;
import javax.swing.event.*;

public class Halo {

    public static final boolean drawpoints = false;

    public double pointradius = 2;
    public Color foreground = new Color(0,0,0);

    public double ringwidth; // step size? hmmmm
    public int   nrings;
    public int   nrays;
    public double theta;
    public double x;
    public double y;
    
    // some available public storage for remembering where the
    // parent halo is;
    // 
    public Halo parent = null;
    
    // This doesn't really work
    // Let's just patch it
    public double parent_x = 0f;
    public double parent_y = 0f;

    public Halo(double width, int n, int k, double h, double x, double y, Halo parent) 
    {
        this.x = x;
        this.y = y;
        this.nrings = n;
        this.ringwidth = width;
        this.nrays = k;
        this.theta = h;
        this.parent = parent;
    }
    
    public void draw(Graphics2D G) {
        G.setColor(foreground);
        if (drawpoints) {
            G.draw(new Ellipse2D.Double(x-pointradius,y-pointradius,pointradius*2,pointradius*2));
            for (int i=1; i<=nrings; i++) {
                G.draw(new Ellipse2D.Double(this.x-i*ringwidth,this.y-i*ringwidth,2*i*ringwidth,2*i*ringwidth));
            }
            for (int i=0; i<nrays; i++) {
                double h = (double)((i*2*Math.PI)/nrays)+theta;
                double ct = (double)Math.cos(h);
                double st = (double)Math.sin(h);
                G.draw(new Line2D.Double(x,y,x+ct*nrings*ringwidth,y+st*nrings*ringwidth));
                for (int j=1; j<=nrings; j++) {
                    double px = x + ct*j*ringwidth;
                    double py = y + st*j*ringwidth;
                    G.draw(new Ellipse2D.Double(px-pointradius,py-pointradius,pointradius*2,pointradius*2));
                }
            }
        } else {
            for (int i=1; i<=nrings; i++) {
               G.draw(new Ellipse2D.Double(this.x-i*ringwidth,this.y-i*ringwidth,2*i*ringwidth,2*i*ringwidth));
            }
            
            /*
            int i=0;
            double h = (double)((i*2*Math.PI)/nrays)+theta;
            double ct = (double)Math.cos(h);
            double st = (double)Math.sin(h);
            G.draw(new Line2D.Double(x,y,x+ct*nrings*ringwidth,y+st*nrings*ringwidth));
            */
            
            for (int i=0; i<nrays; i++) {
                double h = (double)((i*2*Math.PI)/nrays)+theta;
                double ct = (double)Math.cos(h);
                double st = (double)Math.sin(h);
                G.draw(new Line2D.Double(x,y,x+ct*nrings*ringwidth,y+st*nrings*ringwidth));
            }
            
            int stellation = (int)((nrays-1)/2);
            for (int ist=1; ist<=stellation; ist++) {
                // Add midpoints
                for (int i=0; i<nrays; i++) {
                    double h1 = (double)(((i+0)*2*Math.PI)/nrays)+theta;
                    double h2 = (double)(((i+ist)*2*Math.PI)/nrays)+theta;
                    double ct1 = (double)Math.cos(h1);
                    double st1 = (double)Math.sin(h1);
                    double ct2 = (double)Math.cos(h2);
                    double st2 = (double)Math.sin(h2);
                    
                    for (int j=1; j<=nrings; j++) {
                        double px1 = x + ct1*j*ringwidth;
                        double py1 = y + st1*j*ringwidth;
                        double px2 = x + ct2*j*ringwidth;
                        double py2 = y + st2*j*ringwidth;
                        G.draw(new Line2D.Double(px1,py1,px2,py2));
                    }
                }
            }
            
            
        }
    }
    
    public Point2D.Double[] points() {
        Point2D.Double[] result = new Point2D.Double[nrings*nrays*8+1];
        int ii = 0;
        result[ii++] = new Point2D.Double(x,y);
        for (int i=0; i<nrays; i++) {
            double h = (double)((i*2*Math.PI)/nrays)+theta;
            double ct = (double)Math.cos(h);
            double st = (double)Math.sin(h);
            for (int j=1; j<=nrings; j++) {
                double px = x + ct*j*ringwidth;
                double py = y + st*j*ringwidth;
                result[ii++] = new Point2D.Double(px,py);
            }
        }
        /*
        int stellation = (int)((nrays-1)/2);
        for (int ist=1; ist<=stellation; ist++) {
            // Add midpoints
            for (int i=0; i<nrays; i++) {
                double h1 = (double)(((i+0)*2*Math.PI)/nrays)+theta;
                double h2 = (double)(((i+ist)*2*Math.PI)/nrays)+theta;
                double ct = (double)(Math.cos(h1) + Math.cos(h2))*0.5f;
                double st = (double)(Math.sin(h1) + Math.sin(h2))*0.5f;
                for (int j=1; j<=nrings; j++) {
                    double px = x + ct*j*ringwidth;
                    double py = y + st*j*ringwidth;
                    result[ii++] = new Point2D.Double(px,py);
                }
            }
        }
        */
        return result;
    }
}
    
