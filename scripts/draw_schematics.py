"""Vector drawing primitives; copied into each independent project generator."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

plt.rcParams.update({'font.family':'STIXGeneral', 'mathtext.fontset':'stix',
                     'font.size':9, 'pdf.fonttype':42, 'ps.fonttype':42,
                     'text.usetex':False, 'axes.unicode_minus':False})
CM = 1 / 2.54

class Drawing:
    def __init__(self, bounds):
        x0,y0,x1,y1 = bounds
        self.fig = plt.figure(figsize=((x1-x0)*CM,(y1-y0)*CM))
        self.ax = self.fig.add_axes([0,0,1,1], xlim=(x0,x1), ylim=(y0,y1))
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.nodes = {}
        self.labels = []

    def text(self,x,y,label,size=9,ha='center',va='center'):
        artist=self.ax.text(x,y,label,fontsize=size,ha=ha,va=va,
                            linespacing=1.15,clip_on=False,zorder=4)
        self.labels.append([artist,None])
        return artist

    def box(self,name,x,y,w,h,label,dashed=False,shape='rect',size=9):
        style = {'edgecolor':'black','facecolor':'white','linewidth':.55,
                 'linestyle':(0,(4,3)) if dashed else 'solid', 'zorder':2}
        if shape == 'diamond':
            obj = Polygon([(x-w/2,y),(x,y+h/2),(x+w/2,y),(x,y-h/2)],**style)
        elif shape == 'circle': obj = Circle((x,y),w/2,**style)
        else: obj = Rectangle((x-w/2,y-h/2),w,h,**style)
        self.ax.add_patch(obj); self.text(x,y,label,size)
        self.labels[-1][1]=(x-w/2,y-h/2,x+w/2,y+h/2)
        self.nodes[name] = (x,y,w,h,shape)

    def point(self,name,side):
        x,y,w,h,_ = self.nodes[name]
        return {'n':(x,y+h/2),'s':(x,y-h/2),'e':(x+w/2,y),
                'w':(x-w/2,y),'nw':(x-w/2,y+h/2),
                'ne':(x+w/2,y+h/2),'c':(x,y)}[side]

    def line(self,points,dashed=False):
        xs,ys=zip(*points)
        self.ax.plot(xs,ys,color='black',linewidth=.55,
                     linestyle=(0,(4,3)) if dashed else 'solid',zorder=1)

    def arrow(self,p,q,dashed=False,via=()):
        points=[p,*via,q]
        if via:self.line(points[:-1],dashed)
        self.ax.add_patch(FancyArrowPatch(points[-2],points[-1],
                         arrowstyle='-|>',mutation_scale=7.5,linewidth=.55,
                         color='black',shrinkA=0,shrinkB=0,
                         linestyle=(0,(4,3)) if dashed else 'solid',zorder=1))

    def edge(self,a,b,sa='s',sb='n',**kwargs):
        self.arrow(self.point(a,sa),self.point(b,sb),**kwargs)

    def frame(self,x,y,w,h):
        self.ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor='black',
                                   linewidth=.55,linestyle=(0,(4,3)),zorder=0))

    def save(self,out,name):
        # Fixed physical canvas: do not enlarge or rasterize the scientific figure.
        self.fig.canvas.draw()
        renderer=self.fig.canvas.get_renderer()
        x0,x1=self.ax.get_xlim();y0,y1=self.ax.get_ylim()
        for artist,node in self.labels:
            b=artist.get_window_extent(renderer).transformed(self.ax.transData.inverted())
            if b.x0<x0-.02 or b.x1>x1+.02 or b.y0<y0-.02 or b.y1>y1+.02:
                raise ValueError(name+': clipped label '+repr(artist.get_text()))
            if node and (b.x0<node[0]-.02 or b.x1>node[2]+.02 or b.y0<node[1]-.02 or b.y1>node[3]+.02):
                raise ValueError(name+': label exceeds node '+repr(artist.get_text()))
        self.fig.savefig(out/(name+'.pdf'),format='pdf',
                         metadata={'Creator':'Python Matplotlib','Producer':None,
                                   'CreationDate':None,'ModDate':None})
        plt.close(self.fig)






ROOT = Path(__file__).resolve().parents[1]

def evidence(out):
    d=Drawing((-1.5,-1.35,6.5,3.0))
    d.box("e0",0,0,2.5,.48,r"Anchor $e_0$",size=8.5)
    d.box("e1",5.05,0,2.5,.48,r"Base entity $e_1$",size=8.5)
    d.line([d.point("e0","e"),d.point("e1","w")],dashed=True)
    d.text(2.53,.22,r"$d=18$",size=8)
    d.text(2.53,-.22,r"$S=\{\lambda\}$",size=8)
    d.box("b",0,1.15,2.5,.8,"Backup $b$\n"+r"$d=20,\ S=\{b\}$",size=8)
    d.box("o",5.05,2.45,2.55,.8,"Observation $o$\n"+r"$d=12,\ S=\{a\}$",size=8)
    d.box("c",5.05,1.15,2.8,.8,"Copy $c$\n"+r"local $d^0=35,\ S^0=\{b\}$",size=8)
    d.edge("o","c")
    d.text(5.3,1.8,"required",size=8,ha="left")
    d.line([d.point("b","s"),d.point("e0","n")])
    d.line([d.point("c","s"),d.point("e1","n")])
    d.text(-1.2,-.9,"Solid arrow: evidence dependency\nDashed edge: alias; vertical line: base ownership",size=8,ha="left")
    d.save(out,"evidence-path")

def boundary(out):
    d=Drawing((-1.85,-.85,6.45,3.6))
    d.box("prefix",0,2.95,3.4,.7,"Independent admitted\nprefix and fixed policy",size=8)
    d.box("prod",4.6,2.95,3.4,.7,"Untrusted producer\nsummaries and coverage",size=8,dashed=True)
    d.box("check",0,1.2,3.4,.7,"Separate checker\nreconstruct and compare",size=8)
    d.box("cache",4.6,1.2,3.4,.7,"Verified local cache\nretained IDs and values",size=8)
    d.box("context",0,-.3,3.4,.7,"Independent current cut,\ntime, complete revocations",size=8)
    d.box("answer",4.6,-.3,3.4,.7,"Exact ranked query\nwinner or absence",size=8)
    d.edge("prefix","check")
    d.arrow(d.point("prod","s"),(1.0,1.55),via=((4.6,2.05),(1.0,2.05)))
    d.text(2.8,2.23,"certificate",size=8)
    d.edge("check","cache","e","w")
    d.text(2.3,1.4,"accept",size=8)
    d.edge("cache","answer")
    d.edge("context","answer","e","w")
    d.save(out,"checker-boundary")

def main():
    parser=argparse.ArgumentParser(description="Render evidence and checker relationships; no experiment.")
    parser.add_argument("--out",type=Path,default=ROOT/"figures")
    parser.add_argument("--paper-dir",type=Path,default=None)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    evidence(args.out);boundary(args.out)
    if args.paper_dir is not None:
        import shutil
        args.paper_dir.mkdir(parents=True,exist_ok=True)
        for name in ("evidence-path","checker-boundary"):
            shutil.copyfile(args.out/(name+".pdf"),args.paper_dir/(name+".pdf"))
    print("Rendered evidence dependencies, alias ownership and independent checker inputs.")

if __name__=="__main__":
    main()
