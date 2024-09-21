import pygame as py
import sys

py.init()

rook=py.Rect(17,17,90,98)
pawn=py.Rect(16,19,90,98)
bishop=py.Rect(11,11,96,98)
knight=py.Rect(11,13,96,120)
king=py.Rect(11,12,97,98)
queen=py.Rect(7,7,97,98)


class Rook:
    def __init__(self,pos,clr):
        self.clr=clr
        self.pos=pos
        self.crop=rook
        self.set=[]
        self.castle=True
        self.me='rook'

    def recon(self,full=True):
        if self.clr=='white' and self.pos not in ('A1','H1'):
            self.castle=False
        elif self.clr=='black' and self.pos not in ('A8','H8'):
            self.castle=False


        if self.pos=='taken':
            self.set=[]
            return []
        psbl_r=[]
        psbl_c=[]
        for i in 'ABCDEFGH':
            psbl_r.append(f'{i}{self.pos[1]}')
        for i in range(1,9):
            psbl_c.append(f'{self.pos[0]}'+f'{i}')

        for i in AP:
            ind_r,ind_c=psbl_r.index(self.pos),psbl_c.index(self.pos)
            if i.pos in psbl_r:
                flag=psbl_r.index(i.pos)
                if i.pos==self.pos:
                    continue
                elif ind_r<flag:
                    del psbl_r[flag+1:]
                elif flag<ind_r:
                    del psbl_r[:flag]


                if i.clr==self.clr:
                    psbl_r.remove(i.pos)
            if i.pos in psbl_c:
                flag=psbl_c.index(i.pos)
                if flag==ind_c:
                    continue
                elif ind_c<flag:
                    del psbl_c[flag+1:]
                elif flag<ind_c:
                    del psbl_c[:flag]
                
                if i.clr==self.clr:
                    psbl_c.remove(i.pos)

        psbl_c.remove(self.pos)
        psbl_r.remove(self.pos)

        now=psbl_c+psbl_r

        if full:
            opp=Bps if self.clr=='white' else Wps
            king=wk if self.clr=='white' else bk
            og=self.pos
            for i in now.copy():
                self.pos=i
                for x in opp:
                    x.recon(False)
                    if king.pos in x.set:
                        if i==x.pos:
                            continue
                        now.remove(i)
                        break
                self.pos=og

        self.set=now


class Bishop:
    def __init__(self,pos,clr):
        self.clr=clr
        self.pos=pos
        self.crop=bishop
        self.set=[]  
        self.me='bishop'

    def recon(self,full=True):
        if self.pos=='taken':
            self.set=[]
            return []
        psbl_r=[]
        psbl_c=[]
        for i in 'ABCDEFGH':
            psbl_r.append(f'{i}{self.pos[1]}')
        for i in range(1,9):
            psbl_c.append(f'{self.pos[0]}'+f'{i}')
        
        a=list(reversed(psbl_r[0:psbl_r.index(self.pos)]))
        b=psbl_r[psbl_r.index(self.pos)+1:]
        c=list(reversed(psbl_c[:psbl_c.index(self.pos)]))
        d=psbl_c[psbl_c.index(self.pos)+1:]

        first=[]
        second=[]
        third=[]
        fourth=[]

        x=b if len(b)<len(d) else d
        for i in range(len(x)):
            first.append(b[i][0]+d[i][1])

        x=b if len(b)<len(c) else c
        for i in range(len(x)):
            second.append(b[i][0]+c[i][1])

        x=a if len(a)<len(c) else c
        for i in range(len(x)):
            third.append(a[i][0]+c[i][1])

        x=a if len(a)<len(d) else d
        for i in range(len(x)):
            fourth.append(a[i][0]+d[i][1])

        tot=[first,second,third,fourth]
        for i in tot:
            for x in AP:
                if x.pos in i:
                    del i[i.index(x.pos)+1:]
                    if x.clr==self.clr:
                        i.remove(x.pos)

        now=tot[0]+tot[1]+tot[2]+tot[3]

        if full:
            opp=Bps if self.clr=='white' else Wps
            king=wk if self.clr=='white' else bk
            og=self.pos
            for i in now.copy():
                self.pos=i
                for x in opp:
                    x.recon(False)
                    if king.pos in x.set:
                        if i==x.pos:
                            continue
                        now.remove(i)
                        break
                self.pos=og


        self.set= now


class Pawn:
    def __init__(self,pos,clr):
        self.clr=clr
        self.pos=pos
        self.crop=pawn
        self.set=[]
        self.me='pawn'

    def recon(self,full=True):
        if self.pos=='taken':
            self.set=[]
            return []

        if self.clr=='white':
            straight=[self.pos[0]+str(int(self.pos[1])+1)]
            files='ABCDEFGH'
            if self.pos[1]=='2':
                straight=[self.pos[0]+str(int(self.pos[1])+1),self.pos[0]+str(int(self.pos[1])+2)]
                psbl_side=[]
            elif self.pos[0]=='A':
                psbl_side=['B'+str(int(self.pos[1])+1)]
            elif self.pos[0]=='H':
                psbl_side=['G'+str(int(self.pos[1])+1)]
            else:
                psbl_side=[files[files.index(self.pos[0])-1]+str(int(self.pos[1])+1),files[files.index(self.pos[0])+1]+str(int(self.pos[1])+1)]
        else:
            
            straight=[self.pos[0]+str(int(self.pos[1])-1)]
            files='ABCDEFGH'
            if self.pos[1]=='7':
                straight=[self.pos[0]+str(int(self.pos[1])-1),self.pos[0]+str(int(self.pos[1])-2)]
            if self.pos[0]=='A':
                psbl_side=['B'+str(int(self.pos[1])-1)]
            elif self.pos[0]=='H':
                psbl_side=['G'+str(int(self.pos[1])-1)]
            else:
                psbl_side=[files[files.index(self.pos[0])-1]+str(int(self.pos[1])-1),files[files.index(self.pos[0])+1]+str(int(self.pos[1])-1)]
        side=[]
        for i in AP:
            if i.pos in straight:
                if i.pos==straight[0]:
                    straight.clear()
                elif len(straight)==2 and i.pos==straight[1]:
                    straight.pop()
                if len(straight)==2 and i.pos==straight[1]:
                    straight.append(self.pos[0]+str(int(self.pos[1])+1))
            if i.pos in psbl_side and i.clr != self.clr:
                side.append(i.pos)

        now=straight+side

        for i in now:
            if i not in coord:
                now.remove(i)

        if full:
            opp=Bps if self.clr=='white' else Wps
            king=wk if self.clr=='white' else bk
            og=self.pos
            for i in now.copy():
                self.pos=i
                for x in opp:
                    x.recon(False)
                    if king.pos in x.set:
                        if i==x.pos:
                            continue
                        now.remove(i)
                        break
                self.pos=og

        
        self.set= now

    def promotion(self):
        pos=self.pos
        self.pos='taken'
        queen=Queen(pos,self.clr)
        AP.append(queen)
        Wps.append(queen) if self.clr=='white' else Bps.append(queen)
        return queen

                
        
class Knight:
    def __init__(self,pos,clr):
        self.clr=clr
        self.pos=pos
        self.crop=knight
        self.set=[]
        self.me='knight'

    def recon(self,full=True):
        if self.pos=='taken':
            self.set=[]
            return []
        files='ABCDEFGH'
        psbl=[]
        first=files[files.index(self.pos[0])-2 : files.index(self.pos[0])+3] if files.index(self.pos[0])>1 else files[:files.index(self.pos[0])+3]
        w=first.split(self.pos[0])

        for i in range(len(w)):
            if len(w[i])<2:
                psbl.extend((w[i]+str(int(self.pos[1])-2),w[i]+str(int(self.pos[1])+2)))
            elif i==0:
                psbl.extend((w[i][0]+str(int(self.pos[1])-1),w[i][0]+str(int(self.pos[1])+1)))
                psbl.extend((w[i][1]+str(int(self.pos[1])-2),w[i][1]+str(int(self.pos[1])+2)))
            else:
                psbl.extend((w[i][1]+str(int(self.pos[1])-1),w[i][1]+str(int(self.pos[1])+1)))
                psbl.extend((w[i][0]+str(int(self.pos[1])-2),w[i][0]+str(int(self.pos[1])+2)))
            
        for i in psbl:
            if i not in coord:
                psbl.remove(i)
        for i in AP:
            if i.pos in psbl and i.clr==self.clr:
                psbl.remove(i.pos)

        now=psbl

        if full:
            opp=Bps if self.clr=='white' else Wps
            king=wk if self.clr=='white' else bk
            og=self.pos
            for i in now.copy():
                self.pos=i
                for x in opp:
                    x.recon(False)
                    if king.pos in x.set:
                        if i==x.pos:
                            continue
                        now.remove(i)
                        break
                self.pos=og

        self.set= now


class Queen:
    def __init__(self,pos,clr):
        self.clr=clr
        self.pos=pos
        self.crop=queen
        self.set=[]
        self.me='queen'

    def recon(self,full=True):
        if self.pos=='taken':
            self.set=[]
            return []
        psbl_r=[]
        psbl_c=[]
        for i in 'ABCDEFGH':
            psbl_r.append(f'{i}{self.pos[1]}')
        for i in range(1,9):
            psbl_c.append(f'{self.pos[0]}'+f'{i}')


        a=list(reversed(psbl_r[0:psbl_r.index(self.pos)]))
        b=psbl_r[psbl_r.index(self.pos)+1:]
        c=list(reversed(psbl_c[:psbl_c.index(self.pos)]))
        d=psbl_c[psbl_c.index(self.pos)+1:]

        first=[]
        second=[]
        third=[]
        fourth=[]

        x=b if len(b)<len(d) else d
        for i in range(len(x)):
            first.append(b[i][0]+d[i][1])

        x=b if len(b)<len(c) else c
        for i in range(len(x)):
            second.append(b[i][0]+c[i][1])

        x=a if len(a)<len(c) else c
        for i in range(len(x)):
            third.append(a[i][0]+c[i][1])

        x=a if len(a)<len(d) else d
        for i in range(len(x)):
            fourth.append(a[i][0]+d[i][1])

        tot=[first,second,third,fourth]
        for i in tot:
            for x in AP:
                if x.pos in i:
                    del i[i.index(x.pos)+1:]
                    if x.clr==self.clr:
                        i.remove(x.pos)

        for i in AP:
            ind_r,ind_c=psbl_r.index(self.pos),psbl_c.index(self.pos)
            if i.pos in psbl_r:
                flag=psbl_r.index(i.pos)
                if i.pos==self.pos:
                    continue
                elif ind_r<flag:
                    del psbl_r[flag+1:]
                elif flag<ind_r:
                    del psbl_r[:flag]


                if i.clr==self.clr:
                    psbl_r.remove(i.pos)
            if i.pos in psbl_c:
                flag=psbl_c.index(i.pos)
                if flag==ind_c:
                    continue
                elif ind_c<flag:
                    del psbl_c[flag+1:]
                elif flag<ind_c:
                    del psbl_c[:flag]
                
                if i.clr==self.clr:
                    psbl_c.remove(i.pos)
        
        psbl_c.remove(self.pos)
        psbl_r.remove(self.pos)

        now=psbl_c+psbl_r+tot[0]+tot[1]+tot[2]+tot[3]

        if full:
            opp=Bps if self.clr=='white' else Wps
            king=wk if self.clr=='white' else bk
            og=self.pos
            for i in now.copy():
                self.pos=i
                for x in opp:
                    x.recon(False)
                    if king.pos in x.set:
                        if i==x.pos:
                            continue
                        now.remove(i)
                        break
                self.pos=og

        self.set= now

        
class King:
    def __init__(self,pos,clr):
        self.clr=clr
        self.pos=pos
        self.crop=king
        self.set=[]
        self.castle=True
        self.me='king'

    def recon(self,full=True):
        if self.pos not in ('E1','E8'):
            self.castle=False

        files='ABCDEFGH'

        if self.pos[0]=='A':
            psbl_r=[self.pos,files[files.index(self.pos[0])+1]+self.pos[1]]
        elif self.pos[0]=='H':
            psbl_r=[files[files.index(self.pos[0])-1]+self.pos[1],self.pos]
        else:
            psbl_r=[files[files.index(self.pos[0])+1]+self.pos[1],self.pos,files[files.index(self.pos[0])-1]+self.pos[1]]
        psbl_c=[self.pos[0]+str(int(self.pos[1])+1),self.pos,self.pos[0]+str(int(self.pos[1])-1)]

        for i in psbl_c:
            if i not in coord:
                psbl_c.remove(i)

        a=list(reversed(psbl_r[0:psbl_r.index(self.pos)]))
        b=psbl_r[psbl_r.index(self.pos)+1:]
        c=list(reversed(psbl_c[:psbl_c.index(self.pos)]))
        d=psbl_c[psbl_c.index(self.pos)+1:]

        first=[]
        second=[]
        third=[]
        fourth=[]

        x=b if len(b)<len(d) else d
        for i in range(len(x)):
            first.append(b[i][0]+d[i][1])

        x=b if len(b)<len(c) else c
        for i in range(len(x)):
            second.append(b[i][0]+c[i][1])

        x=a if len(a)<len(c) else c
        for i in range(len(x)):
            third.append(a[i][0]+c[i][1])

        x=a if len(a)<len(d) else d
        for i in range(len(x)):
            fourth.append(a[i][0]+d[i][1])

        tot=[first,second,third,fourth]

        for i in tot:
            for x in AP:
                if x.pos in i:
                    del i[i.index(x.pos)+1:]
                    if x.clr==self.clr:
                        i.remove(x.pos)

        rooks=[wr1,wr2] if self.clr=='white' else [br1,br2]
        cm=[]
        for i in rooks:
            if i.castle:
                for x in AP:
                    if x.pos=='taken' or i.pos=='taken':
                        continue
                    if x.pos not in coord:
                        continue
                    truth=files.index(self.pos[0])>files.index(x.pos[0])>files.index(i.pos[0]) or files.index(self.pos[0])<files.index(x.pos[0])<files.index(i.pos[0])
                    if x.pos[1]==self.pos[1] and truth:
                        break
                else:
                    if i.pos[0]=='A':
                        cm.append('C'+self.pos[1])
                    elif i.pos[0]=='H':
                        cm.append('G'+self.pos[1])

        for i in AP:
            ind_r,ind_c=psbl_r.index(self.pos),psbl_c.index(self.pos)
            if i.pos in psbl_r:
                flag=psbl_r.index(i.pos)
                if i.pos==self.pos:
                    continue
                elif ind_r<flag:
                    del psbl_r[flag+1:]
                elif flag<ind_r:
                    del psbl_r[:flag]

                if i.clr==self.clr:
                    psbl_r.remove(i.pos)
            if i.pos in psbl_c:
                flag=psbl_c.index(i.pos)
                if flag==ind_c:
                    continue
                elif ind_c<flag:
                    del psbl_c[flag+1:]
                elif flag<ind_c:
                    del psbl_c[:flag]
                
                if i.clr==self.clr:
                    psbl_c.remove(i.pos)


        psbl_c.remove(self.pos)
        psbl_r.remove(self.pos)

        now=psbl_c+psbl_r+tot[0]+tot[1]+tot[2]+tot[3]+cm
        if self.pos in now:
            now.remove(self.pos)

        if full:
            opp=Bps if self.clr=='white' else Wps
            king=wk if self.clr=='white' else bk
            og=self.pos
            temp=False
            for i in now.copy():
                self.pos=i
                for x in opp:
                    if x.pos==self.pos:
                        x.pos='taken'
                        temp=x
                        continue
                    x.recon(False)

                    if king.pos in x.set:
                        if i==x.pos:
                            continue
                        now.remove(i)
                        break
                if temp:
                    temp.pos=i
                temp=False
                self.pos=og
            
        self.set= now

    def castling(self,cur):
        if cur[0]=='G':
            other=wr2 if self.clr=='white' else br2
            other.pos='F'+self.pos[1]
        elif cur[0]=='C':
            other=wr1 if self.clr=='white' else br1
            other.pos='D'+self.pos[1]

        
            

def select(x,y):
    zone=py.Rect(x-97,y-97,97,97)
    for i in coord:
        if zone.collidepoint(coord[i] ):
            return(i)      
        
        
def move(i,opp,moves):
    while True:
        for event in py.event.get():
            if event.type==quit:
                py.QUIT
            if event.type==py.MOUSEBUTTONDOWN:
                if event.button==1:
                    x,y=event.pos
                    cur=select(x,y)
                    i.recon()

                    if moves==[] :
                        return True
                    if cur in moves:
                        if type(i)==type(wk) and i.castle and (i.pos=='E1' if i.clr=='white' else i.pos=='E8'):
                            i.castling(cur)

                        og=i.pos
                        i.pos=cur    

                        if type(wn1)==type(i):
                            i.recon()
                        
                        for x in opp:
                            if x.pos==i.pos:
                                x.pos='taken'

                        if i in pawns and cur[1] in ('1','8'):
                            i=i.promotion()

                        if type(i)==type(wk):
                            for x in opp:
                                x.recon(False)
                                if i.pos in x.set:
                                    i.set.remove(i.pos)
                                    i.pos=og
                                    return True

                        grid(i,opp)

                        return False                    
                    else:
                        return True
                    
def check(king,rn,opp):
    for i in AP:
        if type(i)==type(wk):
            continue
        else:
            if i.pos!='taken':
                break
    else:
        return'Draw'

    for i in opp:
        i.recon()
        if i.pos=='taken':
            continue
        if i.set!=[]:
            break
    else:
        for x in rn:
            x.recon()
            if king.pos in x.set:
                return 'checkmate'
        return 'stalemate'

def grid(piece=False,opp=[],high=False,next=[]):
    if piece:
        for i in opp:
            if i.pos==piece.pos:
                i.pos='taken'

    cnt=1
    for i in range(0,776,97):
        cnt-=1
        for x in range(0,776,97):
            if cnt%2==0:
                color=(255,255,255)
            else:
                color=(115, 149, 82)
            
            box=py.Rect(i,x,97,97)
            py.draw.rect(root,color,box)
            cnt+=1
            py.display.flip()
    
    if high:
        box=py.Rect(high[0]+1,high[1]+1,97,97)
        py.draw.rect(root,(250, 115, 44),box)
        for i in next:
            box=py.Rect(coord[i][0]+1,coord[i][1]+1,96,96)
            py.draw.rect(root,(185, 202, 67),box)

    
    
    cnt=-1
    for i in AP:
        img=py.image.load('.\\piece\\{}-{}.png'.format(i.clr,i.me))
        root.blit(img,coord[i.pos],i.crop)

    py.display.flip()


pieces=['rook','knight','bishop','queen','king','bishop','knight','rook']

w1,w2,w3,w4,w5,w6,w7,w8=Pawn('A2','white'),Pawn('B2','white'),Pawn('C2','white'),Pawn('D2','white'),Pawn('E2','white'),Pawn('F2','white'),Pawn('G2','white'),Pawn('H2','white')
b1,b2,b3,b4,b5,b6,b7,b8=Pawn('A7','black'),Pawn('B7','black'),Pawn('C7','black'),Pawn('D7','black'),Pawn('E7','black'),Pawn('F7','black'),Pawn('G7','black'),Pawn('H7','black')

wr1,wr2=Rook('A1','white'),Rook('H1','white')
br1,br2=Rook('A8','black'),Rook('H8','black')
wn1,wn2=Knight('B1','white'),Knight('G1','white')
bn1,bn2=Knight('B8','black'),Knight('G8','black')
wb1,wb2=Bishop('C1','white'),Bishop('F1','white')
bb1,bb2=Bishop('C8','black'),Bishop('F8','black')
wq,bq=Queen('D1','white'),Queen('D8','black')
wk,bk=King('E1','white'),King('E8','black')


ws=[w1,w2,w3,w4,w5,w6,w7,w8]
bs=[b1,b2,b3,b4,b5,b6,b7,b8]
wp=[wr1,wn1,wb1,wq,wk,wb2,wn2,wr2]
bp=[br1,bn1,bb1,bq,bk,bb2,bn2,br2]

pawns=ws+bs

Wps=ws+wp
Bps=bs+bp

AP=wp+ws+bp+bs                


root=py.display.set_mode((776,776))

py.display.set_caption('Chess')
root.fill((20,30,40))

L=[]
for i in 'ABCDEFGH':
    for x in range(8,0,-1):
        L.append(i+str(x))
coord=dict.fromkeys(L)

ind=0
for i in range(0,776,97):
    for x in range(0,776,97):
        coord[L[ind]]=(i,x)
        ind+=1
coord['taken']=(1000,1000)

out=False
grid()


py.display.flip()
white,black=0,0
while True:

    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
            sys.exit()


        if event.type==py.MOUSEBUTTONDOWN:
            if event.button==1:
                if white==black:
                    rn=Wps
                    opp=Bps
                    king=wk
                elif white>black:
                    rn=Bps
                    opp=Wps
                    king=bk
                x,y=event.pos
                cur=select(x,y)
                for i in rn:
                    if i.pos==cur:
                        #scout(king,opp,True)
                        i.recon()
                        moves=i.set 
                        for x in moves:
                            if x not in coord:
                                moves.remove(x)
                        grid(high=coord[cur],next=moves)                     
                        king=wk if rn==Wps else bk
                        s=move(i,opp,moves)
                        if s:
                            grid()
                            continue
                        if rn==Wps:
                            white+=1
                        elif rn==Bps:
                            black+=1
                        break

                king=wk if white==black else bk
                res=check(king,rn,opp)
                if res in ('checkmate','stalemate','draw'):
                    out=True
                    break
    if out:
        break

clr='Black' if white==black else 'White'

while True:
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
            sys.exit()

    if res=='checkmate':
        font=py.font.SysFont("Arial",69)
        text=font.render(f'{clr} wins by Checkmate!!!',True,(255,255,255))
        box=py.Rect(38,300,700,85)
        py.draw.rect(root,(0, 120, 212),box)
        surface=py.Surface((700,85))
        surface.fill((0, 120, 212))
        surface.blit(text,(0,0))
        root.blit(surface,(38,300))
        py.display.flip()
    else:
        font=py.font.SysFont("Arial",69)
        text=font.render(res.capitalize(),True,(42, 68, 152))
        root.blit(text,(300,300))
        py.display.flip()