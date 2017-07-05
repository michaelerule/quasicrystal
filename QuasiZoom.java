// To run this code type the following in the terminal
// javac QuasiZoom.java 
// java QuasiZoom
// (c) m.rule 2011
// http://wealoneonearth.blogspot.co.uk/2011/11/visual-analogue-of-shepard-tone.html

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import static java.lang.Math.*;

public class QuasiZoom {

    // Defines a gaussian function. We will use this to define the
    // envelope of spatial frequencies
    public static double gaussian(double x) {
        return exp(-x*x/2)/sqrt(2*PI);
    }

    public static void main(String[] args) throws IOException {
        int k = 5;        //number of plane waves
        int stripes = 3;  //number of stripes per wave
        int N = 500;      //image size in pixels
        int divisions=40; //number of frames to divide the animation into
        int N2 = N/2;

        BufferedImage it = new BufferedImage(N, N, BufferedImage.TYPE_INT_RGB);

        //the range of different spatial frequencies
        int [] M=new int[]{1,2,4,8,16,32,64,128,256};
        
    //the main ( central ) spatial frequency
        double mean=log(16);

    //the spread of the spatial frequency envelope
        double sigma=1;

    //counts the frames 
        int ss=0;

    //iterate over spatial scales, scaling geometrically
        for (double sc=2.0; sc>1.0; sc/=pow(2,1./divisions)) 
        {    
            System.out.println("frame = "+ss);

            //adjust the  wavelengths for the current spatial scale
            double [] m=new double[M.length];
            for (int l=0; l<M.length; l++)
                m[l]=M[l]*sc;

            //modulate each wavelength by a gaussian envelop in log
            //frequency, centered around aforementioned mean with defined
            //standard deviation
            double sum=0;
            double [] W=new double[M.length];
            for (int l=0; l<M.length; l++) {
                W[l]=gaussian((log(m[l])-mean)/sigma);
                sum+=W[l];
            }
            sum*=k;

            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {

                    double x = j - N2, y = i - N2; //cartesian coordinates
                    double C = 0;                  // accumulator
 
                    // iterate over all k plane waves
                    for (double t = 0; t < PI; t += PI / k){
                        //compute the phase of the plane wave
                        double ph=(x*cos(t)+y*sin(t))*2*PI*stripes/N;
                        //take a weighted sum over the different spatial scales
                        for (int l=0; l<M.length; l++)
                            C += (cos(ph*m[l]))*W[l];
                    }
                    // convert the summed waves to a [0,1] interval
                    // and then convert to [0,255] greyscale color
                    C = min(1,max(0,(C*0.5+0.5)/sum));
                    int c = (int) (C * 255);
                    it.setRGB(i, j, c | (c << 8) | (c << 16));
                }
            }
            ImageIO.write(it, "png", new File("out"+(ss++)+".png"));
        }
        
    }
}
