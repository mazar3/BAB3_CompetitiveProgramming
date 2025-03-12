print("Ayoub la lose")
class Ressource :
    ressources =[]
    Tm=0
    Tr=0
    Tx=0
    Rl=[]

    def __init__ (self,r):
        self.ri=int(r[0])
        self.ra=int(r[1])
        self.rp=int(r[2])
        self.rw=int(r[3])
        self.rm=int(r[4])
        self.rl=int(r[5])
        self.__class__.Rl.append(self.rl)
        self.ru=int(r[6])
        self.rt=r[7]
        self.re=int(r[8])
        if self.rt=='X': re=0



    def specialEffect(self):
        if self.re <0 :
            if self.rt=='A':
                self.ru= self.ru - ((self.ru)*abs(self.re))/100
            if self.rt=='B':
                self.__class__.Tm = self.__class__.Tm - (self.__class__.Tm*self.re)/100
                self.__class__.Tx = self.__class__.Tx  - (self.__class__.Tx *self.re)/100
                if self.__class__.Tm or self.__class__.Tx < 0 :
                    self.__class__.Tx ,self.__class__.Tx =0

            if self.rt=='C':
                for l in self.__class__.Rl:
                    l = l - (l*abs(self.re))/100
                    if l<1 :
                        l=1
            if self.rt=='D':
                self.__class__.Tr = self.__class__.Tr - (self.__class__.Tr*abs(self.re))/100
                if self.__class__.Tr < 0 :
                    self.__class__.Tr =0
        else:
            if self.rt=='A':
                self.ru= self.ru + ((self.ru)*self.re)/100
            if self.rt=='B':
                self.__class__.Tm = self.__class__.Tm + (self.__class__.Tm*self.re)/100
                self.__class__.Tx = self.__class__.Tx  + (self.__class__.Tx *self.re)/100
                if self.__class__.Tm or self.__class__.Tx < 0 :
                    self.__class__.Tx ,self.__class__.Tx =0

            if self.rt=='C':
                for l in self.__class__.Rl:
                    l = l + (l*self.re)/100

            if self.rt=='D':
                self.__class__.Tr = self.__class__.Tr + (self.__class__.Tr*self.re)/100
                if self.__class__.Tr < 0 :
                    self.__class__.Tr =0

with open('0-demo.txt', 'r') as fin,open('demout.txt', 'w') as fout :
    D,R,T=list(map(int,fin.readline().split()))
    for i in range (R):
        l=fin.readline().split()
        Ressource.ressources.append(Ressource(l))
    Ressource.Tm,Ressource.Tx,Ressource.Tr=list(map(int,fin.readline().split()))
    for r in Ressource.ressources:
        r.specialEffect()

