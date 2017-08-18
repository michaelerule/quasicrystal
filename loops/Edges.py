#!/usr/bin/env jython
# Experimental drawing utility for compass designs

#from future import print_statemenet


from java.awt       import Color,BorderLayout,FlowLayout,Cursor,GridBagConstraints,GridBagLayout,Toolkit,Point,Robot
from java.awt.event import MouseAdapter, MouseListener, MouseMotionListener, ComponentAdapter
from java.awt.image import BufferedImage
from java.awt.Color import BLACK,WHITE,YELLOW,RED
from java.awt.geom  import Line2D,Ellipse2D
from time           import sleep,clock
from cmath          import *
from math           import atan2
from jarray         import array,zeros
from threading      import Thread
from java.lang      import System
from javax.imageio  import ImageIO
from java.io        import File
import random
from javax.swing import *
from java.awt import *
from java.awt.geom import *
from java.awt.event import *
from javax.swing.event import *
from java.lang import *

M = 7
R = 20
SCREENSIZE = 800

units = [R*exp(1j*pi*i/M) for i in range(2*M)]

image = BufferedImage(SCREENSIZE,SCREENSIZE,BufferedImage.TYPE_INT_RGB)
GQ = image.createGraphics()
GQ.color = Color.WHITE
GQ.fillRect(0,0,SCREENSIZE,SCREENSIZE)

class Lattice(JPanel):
    def paint(self,g):
        g.drawImage(image,0,0,SCREENSIZE,SCREENSIZE,None)        
jf = JFrame("Loops")
jp = JPanel(BorderLayout())
l  = Lattice()
jf.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
jf.contentPane = jp
jp.preferredSize = Dimension(SCREENSIZE,SCREENSIZE)
jp.add(l,BorderLayout.CENTER);
jf.pack();
jf.show();

colors = [(1,1,1),
(1  ,0 , 0), (0 , 0, 0),
(0  ,1 , 1), (0 ,.2,.5),
(1  ,1 , 0), (0 , 1, 0),
(1  ,0 , 1), (.4, 0, 1),
(.8 ,.8,.8), (.2,.2,.2),
(1  ,.5, 0), (.2,.2, 0),
(0.5, 1, 0), (1.,.5,.5)]

colors = [Color(r*.999,g*.999,b*.999) for (r,g,b) in colors]

def angle(z):
    return atan2(z.imag,z.real)

def zline(G,a,b):
    '''
    Draw line between two points passed as complex
    '''
    G.draw(Line2D.Float(a.real,a.imag,b.real,b.imag))

class edge:
    def __init__(self,a,b,color=None):
        self.setpoints(a,b)
        self.color  = color
    def moveto(self,a):
        self.setpoints(a,self.b-self.a+a)
    def setpoints(self,a,b,color=None):
        self.a,self.b = a,b
        self.delta  = a-b
        self.len    = abs(self.delta)
        self.angel  = self.delta/self.len
        self.arrow1 = self.b+self.angel*exp( 1j*pi/4)*0.2*self.len
        self.arrow2 = self.b+self.angel*exp(-1j*pi/4)*0.2*self.len
        self.ortho  = self.angel*exp(-pi/2)
        self.color  = color
    def paint(self,G,offset=0):
        '''
        Offset displaces the edge slightly in the direction 
        orthogonal to it. This lets us draw interior / exterior
        polygons more exactly
        '''
        if self.color:
            G.color = self.color
        G.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                           RenderingHints.VALUE_ANTIALIAS_ON);
        delta = offset*self.ortho
        zline(G,self.a+delta,self.b+delta)
        #zline(G,self.b+delta,self.arrow1+delta)
        #zline(G,self.b+delta,self.arrow2+delta)
    def translate(self,z):
        self.a += z
        self.b += z

e1 = edge(30+40j,100+22j)
e2 = edge(e1.a,e1.b)
e2.moveto(e1.b)

def edgeangle(e):
    vec = e.b-e.a
    ang = (angle(vec)+4*pi)%(2*pi)
    return int(ang/(pi/M)+0.5)

def tiletype(v):
    span  = v.angle()
    if span>pi:
        span = 2*pi-span
    if span>=pi/2:
        span = pi-span
    return int(span/(pi/M)+0.5)

def vertexint(v):
    span  = v.angle()
    span = 2*pi-span
    return int(span/(pi/M)+0.5)
    
def vertexspan(v):
    span  = v.angle()
    if span>pi:
        span = 2*pi-span
    return int(span/(pi/M)+0.5)

class vertex:
    def __init__(self,a,b,c,color1=None,color2=None,color3=None):
        self.e1 = edge(a,b,color1)
        self.e2 = edge(b,c,color2)
        self.fill = color3
        if color3 is None:
            # guess via quanta
            count = tiletype(self)
            self.fill = colors[count%len(colors)]
            #print('angle is','%d'%(span*180/pi),'setting to color',count,self.fill)
    def paint(self,G,transparent=False):
        if self.fill:
            a,b = self.e1.a,self.e1.b
            b,c = self.e2.a,self.e2.b
            d   = a+c-b
            pts = [a,b,c,d]
            if not transparent:
                G.color = self.fill
                G.fillPolygon([int(.5+z.real) for z in pts],[int(.5+z.imag) for z in pts],4)
        self.e1.paint(G,offset=0)
        self.e2.paint(G,offset=0)
    def translate(self,z):
        self.e1.translate(z)
        self.e2.translate(z)
    def angle(self):
        p0 = self.e1.a
        p1 = self.e1.b
        p2 = self.e2.b
        return (angle(p2-p1)-angle(p0-p1) + 4*pi)%(2*pi)

c = (1+1j)*(SCREENSIZE/2)
#perim = [vertex(c,c+R*exp(1j*pi*i/M),c) for i in range(M*2)]
perim = [vertex(c,c+R*exp(2*1j*pi*i/M),c) for i in range(M)]

def expand(perim,convexity=0):
    newp = []
    NP = len(perim)
    valid = False
    for i in range(NP):
        v1 = perim[(i+0)%NP]
        v2 = perim[(i+1)%NP]
        pA = v1.e1.a
        p0 = v1.e1.b
        p1 = v1.e2.b
        p2 = v2.e1.b
        pZ = v2.e2.b
        ui0=edgeangle(v1.e1)
        ui1=edgeangle(v1.e2)
        ui2=edgeangle(v2.e1)
        ui3=edgeangle(v2.e2)
        u0=units[ui0%(M*2)]
        u1=units[ui1%(M*2)]
        u2=units[ui2%(M*2)]
        u3=units[ui3%(M*2)]
        #print '0th edge unit is',ui0,u0
        #print '1th edge unit is',ui1,u1
        #print '2th edge unit is',ui2,u2
        #print '3th edge unit is',ui3,u3
        pn = p0+u2
        vn = vertex(p0,pn,p2,colors[1],colors[2])
        # count number of angles spanned by missing tile(s)
        vint = vertexint(vn)
        tid  = tiletype(vn)
        span = vertexspan(vn)
        t1id = vertexspan(v1)
        t2id = vertexspan(v2)
        #print 'vertex span is',span,'; sector count is',vint,'; tile type is',tid
        if vint<M and not (span==t1id or span==t2id):
    	    #print '>concave, use one tile<'
    	    if vint>0:
                newp.append(vn)
                valid=True
            else:
                # This tile has zero area
                # We need to repair the boundary using a virtual tile
                # Keep original vertex if already convex
                # This is a virtual tile however, it doesn't count
                newp.append(vertex(pA,0.5*(p0+p2),pZ,colors[7],colors[8],Color(0,1,1,1)))
        elif vint<M:
            # concave, but nees a multiple-polygon fill
            # only do these if all else has failed
            if convexity>0:
                # Should only do convex fills if no concave regions available
                #print '>convex, use multiple tiles<'
                subspan = vint//2
                assert subspan>0 and subspan<M
                #print 'filling span',vint,'using tiles width',subspan
                uA = units[(ui2-subspan+M*2)%(M*2)]
                uB = units[(ui1+subspan+M*2)%(M*2)]
                newp.append(vertex(p0,p0-uB,p1-uB,colors[1],colors[2]))
                if vint%2!=0:
                    newp.append(vertex(p1-uB,p1+uA-uB,p1+uA,colors[1],colors[2]))
                newp.append(vertex(p1+uA,p2+uA,p2,colors[1],colors[2])) 
                valid=True
                
        elif vint>0 and vint<M*2:
            # True convex shape
            if convexity<2:
                # Keep original vertex if already convex
                # This is a virtual tile however, it doesn't count
                newp.append(vertex(p0,p1,p2,colors[7],colors[8],Color(0,1,1,1)))
            else:
                # Should only do convex fills if no concave regions available
                #print '>convex, use multiple tiles<'
                subspan = vint//2
                assert subspan>0 and subspan<M
                #print 'filling span',vint,'using tiles width',subspan
                uA = units[(ui2-subspan+M*2)%(M*2)]
                uB = units[(ui1+subspan+M*2)%(M*2)]
                newp.append(vertex(p0,p0-uB,p1-uB,colors[1],colors[2]))
                if vint%2!=0:
                    newp.append(vertex(p1-uB,p1+uA-uB,p1+uA,colors[1],colors[2]))
                newp.append(vertex(p1+uA,p2+uA,p2,colors[1],colors[2])) 
                valid=True
    # Remove zero area pieces?
    #cleanp = [v for v in newp if tiletype(vn)>0]
    cleanp = newp
    return cleanp,valid


convexity = 0
def growperim():
    global perim, convexity
    print "Searching convexity",convexity,'...'
    newp,valid = expand(perim,convexity=convexity)
    if not valid:
        convexity += 1
        print "No concave cells, increasing convexity to %d and retrying"%convexity
        if convexity>4:
            print "EXPANSION FAILED PERMANENTLY
    else:
        convexity = 0
        assert len(newp)>0
    if len(newp)>0 and valid:
        perim = newp
    for v in perim:
        v.paint(GQ)
    GQ.color = Color(1,1,1,0.0)
    GQ.fillRect(0,0,SCREENSIZE,SCREENSIZE)
    for v in perim:
        v.paint(GQ,transparent=True)
    l.repaint()
    for i,vn in enumerate(perim):
        vint = vertexint(vn)
        tid  = tiletype(vn)
        span = vertexspan(vn)
        print 'vertex %02d span is'%i,span,'; sector count is',vint,'; tile type is',tid
        # print bridge info too for debugging
        v2 = perim[(i+1)%len(perim)]
        vn = vertex(vn.e2.a,vn.e2.b,v2.e1.b,colors[1],colors[2])
        vint = vertexint(vn)
        tid  = tiletype(vn)
        span = vertexspan(vn)
        print 'bridge    span is',span,'; sector count is',vint,'; tile type is',tid
        
        
jp.mouseClicked = lambda e: growperim()

for v in perim:
    v.paint(GQ)
    l.repaint()

#for ii in range(50):
#    growperim()

print("done")
