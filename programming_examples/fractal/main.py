import matplotlib.pyplot as plt
def dline(tup1,tup2):
    x1,y1 = tup1
    x2,y2 = tup2
    plt.plot([x1,x2],[y1,y2],'k-')

class prog: #Progress handling
    def set_i(self,i):
        self.runsdone = 0
        self.runstodo = 4**(i-5)
    def update(self):
        ff = float(self.runstodo)
        gg = float(self.runsdone)
        perc = gg*100.0/ff
        print(str(round(perc,5)))


def frac(n,i,m=None):
    n = float(n)
    if m == None:
        x,y = (0,0)
    else:
        x,y = m
    if i > 0:
        dline((x-n,y),(x+n,y))
        dline((x,y-n),(x,y+n))

        dline((x,y-n),(x-n,y-n))
        frac(n/2,i-1,(x-n,y-n))

        dline((x+n,y),(x+n,y-n))
        frac(n/2,i-1,(x+n,y-n))

        dline((x-n,y),(x-n,y+n))
        frac(n/2,i-1,(x-n,y+n))

        dline((x,y+n),(x+n,y+n))
        frac(n/2,i-1,(x+n,y+n))

        if i==5: #update progress data
            progress.runsdone += 1
            progress.update()

def frac_progress(i):
    progress.set_i(i)
    frac(1,i)

progress = prog()
frac_progress(8)
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()
