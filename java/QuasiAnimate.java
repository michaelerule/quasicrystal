// To run this code type the following in the terminal
// javac QuasiAnimate.java 
// java QuasiAnimate
// (c) m.rule 2011
// http://wealoneonearth.blogspot.co.uk/2011/10/animated-quasicrystals.html

 import java.awt.image.BufferedImage;    
 import java.io.File;    
 import java.io.IOException;    
 import javax.imageio.ImageIO;    
 import static java.lang.Math.*;    
 
 public class QuasiAnimate 
 {    
     public static void main(String [] args) throws IOException {    
         int k=4;         //numer of plane waves    
         int stripes = 27; //number of stripes per wave    
         int N = 800;     //image size in pixels    
         int N2 = N/2;    
         BufferedImage it = new BufferedImage(N,N,BufferedImage.TYPE_INT_RGB);    
         for (double phase=0; phase<2*PI; phase+=2*PI/30) 
         {
             for ( int i=0; i<N; i++ ) for ( int j=0; j<N; j++ ) 
             {    
                 double x = j-N2, y = i-N2; //cartesian coordinates    
                 double theta = atan2(y,x); //log-polar coordinates    
                 double r = log(sqrt(x*x+y*y));    
                 double C=0;                // accumulator    
                 for (double t=0; t<PI; t+=PI/k)    
                     C+=cos((theta*cos(t)-r*sin(t))*stripes+phase);    
                     // use the following line for cartesian crystals:    
                     //C+=cos((x*cos(t)+y*sin(t))*2*PI*stripes/N+phase);    
                 int c=(int)((C+k)/(k*2)*255);    
                 it.setRGB(i,j,c|(c<<8)|(c<<16));    
             }    
             ImageIO.write(it,"png",new File("Test"+(int)(180*phase/PI)+".png")) ;    
         }    
     }    
 }
