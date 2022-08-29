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
import javax.swing.event.*;
import java.awt.*;
import java.awt.event.*;

public class Quasicrystal 
{    
    static boolean show = true;  // whether to display image in a window  
    static int k = 8;            // numer of plane waves    
    static int stripes = 100;     // number of stripes per wave    
    static int K = 800;          // image size in pixels
    static int downsample = 2;   // Oversampling factor
    static int N = K*downsample; 
    static double phase = 0.0;   // phase shift for the crystal  
         
    static float th = -0.1f;//1f; // edge contour threshold
         
    static JFrame jf = new javax.swing.JFrame("output"); 
    static JPanel jp;
    static JPanel jpim = new JPanel() {
        public void paint(Graphics G) {
            if (it==null) return;
            G.drawImage(it,0,0,it.getWidth()/downsample,it.getHeight()/downsample,null);
        }
    };
    
    // Image data buffers
    static BufferedImage it  = new BufferedImage(N,N,BufferedImage.TYPE_INT_RGB);    
         
    static void init() {
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jp = new javax.swing.JPanel(new BorderLayout());
        jpim.setPreferredSize(new Dimension(K,K));
        jp.add(jpim,BorderLayout.CENTER);
        jf.setContentPane(jp);
        jf.pack();
        jf.setVisible(true);
    }
             
    static void redraw() {
        jpim.paint(jpim.getGraphics());
    }
    
    static void render(
        String cmap,
        float[][] wave, 
        BufferedImage it) 
        {
        System.out.println("edge="+th);
        int width = 3;
        int a = width/2;
        int b = width-a;
        int rr = width*width/4;
        // Next map the rendered wave to an image using selected color map
        int c;
        if ( cmap.equals("linear") ) for (int i=0;i<N;i++) for (int j=0;j<N;j++) 
        {    
            float C = wave[i][j];
            c=(int)((C+1)/2*255);
            it.setRGB(i,j,c|(c<<8)|(c<<16));    
        }
        else if ( cmap.equals("squared") ) for (int i=0;i<N;i++) for (int j=0;j<N;j++) 
        {    
            float C = wave[i][j];
            c=(int)((1-C*C)*255);
            it.setRGB(i,j,c|(c<<8)|(c<<16));    
        }
        else if ( cmap.equals("power") ) for (int i=0;i<N;i++) for (int j=0;j<N;j++) 
        {    
            float C = wave[i][j];
            c=(int)(Math.pow(1-C*C,60)*255);
            it.setRGB(i,j,c|(c<<8)|(c<<16));    
        } 
        else if ( cmap.equals("edge") ) for (int i=0;i<N;i++) for (int j=0;j<N;j++) 
        {    
            float C = wave[i][j];
            boolean edge = 
            ((j>=a&&j<N-b)&&(wave[i][j-a]>th)!=(wave[i][j+b]>th)) 
            || ((i>=a&&i<N-b)&&(wave[i-a][j]>th)!=(wave[i+b][j]>th));
            c=!edge? 255:0;
            it.setRGB(i,j,c|(c<<8)|(c<<16));    
        }
        else if ( cmap.equals("threshold") ) for (int i=0;i<N;i++) for (int j=0;j<N;j++) 
        {    
            float C = wave[i][j];
            c=wave[i][j]>th? 255:0;
            it.setRGB(i,j,c|(c<<8)|(c<<16));    
        }
        else if (cmap.equals("ridge")) for (int i=a;i<N-b;i++) for (int j=a;j<N-b;j++) 
        {    
            float c11 = wave[i  ][j  ];
            float cc = c11*c11;
            int count = 0;
            int count2 = 0;
            int norm = 0;
            for (int ii=-a; ii<=b; ii++) for (int jj=-a; jj<=b; jj++) {
                if (ii*ii+jj*jj>rr) continue;
                float x = wave[i+ii][j+jj];
                if (x*x>cc) count2++;
                if (x>c11) count++;
                norm ++;
            }
            c = count*255/norm;
            int G = count2*255/norm;
            it.setRGB(i,j,c|(G<<8)|(c<<16));    
        }
        else {
            System.err.println(
            "color map variable / parameter should be linear squared power threshold or edge");
            System.exit(-1);
        }
    }
    
    public static void main(String [] args) throws IOException {   
    
        try {
            javax.swing.UIManager.setLookAndFeel(javax.swing.UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            try {
                javax.swing.UIManager.setLookAndFeel("com.sun.java.swing.plaf.gtk.GTKLookAndFeel");
            } catch (Exception e2) {}
        }


        String cmap;
        // select one below
        //cmap = "linear"; 
        //cmap = "squared";
        //cmap = "power";
         cmap = "edge";
        // cmap = "threshold";
        //cmap = "ridge"; // experimental do not use

        int N2 = N/2;

        // Precompute planar rotations for speed
        double [] ct = new double[k];
        double [] st = new double[k];
        for (int ik=0; ik<k; ik++) {
            double t=ik*PI/k;
            ct[ik] = cos(t);
            st[ik] = sin(t);
        }

        // First fill a buffer with wavefunction amplitudes
        float [][] wave = new float[N][N];
        float scale = (float)(2*PI*stripes/N);
        for (int i=0;i<N;i++) for (int j=0;j<N;j++) 
        {
            double x = j-N2, y = i-N2; //cartesian coordinates    
            double C=0;                // accumulator    
            for (int ik=0; ik<k; ik++) {
                C+=cos((x*ct[ik]+y*st[ik])*scale+phase);
            }
            // normalize by number of superimposed waves
            wave[i][j] = (float)(C/k);
        }

        render(cmap,wave,it);

        if (show) {
            init();
            redraw();
            JSlider slider = new JSlider(JSlider.HORIZONTAL,-200,200,0);
            JButton save   = new JButton(new AbstractAction("Save") {
                public void actionPerformed(ActionEvent e) {
                    try {
                        ImageIO.write(it,"png",new File("Test"+(int)(180*phase/PI)+".png"));
                    } catch(IOException ex) {
                        System.out.println("error saving to disk");
                    }
                }
            });
            slider.setMinorTickSpacing(1);
            JPanel controls = new JPanel(new BorderLayout());
            controls.add(slider,BorderLayout.CENTER);
            controls.add(save  ,BorderLayout.EAST);
            jp.add(controls, BorderLayout.SOUTH);
            jf.pack();
            slider.addChangeListener(new ChangeListener() {
                public void stateChanged(ChangeEvent e) {
                    float th2 = (float)(slider.getValue())/1000.0f;
                    System.out.println(th2);
                    if (th2!=th) {
                        th = th2;
                        render(cmap,wave,it);
                        redraw();
                    }
                }
            });
         }
         
         ImageIO.write(it,"png",new File("Test"+(int)(180*phase/PI)+".png"));
     }
}
