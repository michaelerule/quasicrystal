// To run this code type the following in the terminal
// javac Quasicrystal.java && java Quasicrystal
// (c) m.rule 2011
// http://wealoneonearth.blogspot.co.uk/2010/03/quasicrystal.html

 import java.awt.image.BufferedImage;    
 import java.io.File;    
 import java.io.IOException;    
 import javax.imageio.ImageIO;    
 import static java.lang.Math.*;    
 import javax.swing.*;
 import java.awt.*;
 
 public class Quasicrystal 
 {    
     public static void main(String [] args) throws IOException {  
         boolean show = false; // whether to display image in a window  
         int k=5;              // numer of plane waves    
         int stripes = 47;     // number of stripes per wave    
         int N = 800;          // image size in pixels
         double phase = 0.0;   // phase shift for the crystal   
         String cmap;
         // select one below
         //cmap = "linear"; 
         //cmap = "squared";
         cmap = "power";
         int N2 = N/2;    
         BufferedImage it = new BufferedImage(N,N,BufferedImage.TYPE_INT_RGB);    
         for ( int i=0; i<N; i++ ) for ( int j=0; j<N; j++ ) 
         {    
             double x = j-N2, y = i-N2; //cartesian coordinates    
             double theta = atan2(y,x); //log-polar coordinates    
             double r = log(sqrt(x*x+y*y));    
             double C=0;                // accumulator    
             for (double t=0; t<PI; t+=PI/k) {
                 C+=cos((x*cos(t)+y*sin(t))*2*PI*stripes/N+phase);
             }
             // linear color map
             int c=0;
             if ( cmap.equals("linear") ) {
                 c=(int)((C+k)/(k*2)*255);
             } 
             else if ( cmap.equals("squared") ) { 
                 c=(int)((1-(C/k)*(C/k))*255);
             } 
             else if ( cmap.equals("power") ) { 
                 c=(int)(Math.pow(1-(C/k)*(C/k),60)*255);
             } 
             else {
                System.err.println("color map variable / parameter should be linear squared or power");
                System.exit(-1);
             }    
             it.setRGB(i,j,c|(c<<8)|(c<<16));    
         }
         
         if (show) {
             JFrame jf = new javax.swing.JFrame("output");
             jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
             JPanel jp = new javax.swing.JPanel(new FlowLayout());
             jp.add(new JLabel(new ImageIcon(it)));
             jf.setContentPane(jp);
             jf.pack();
             jf.setVisible(true);
         }
         
         ImageIO.write(it,"png",new File("Test"+(int)(180*phase/PI)+".png")) ;    
     }
}
