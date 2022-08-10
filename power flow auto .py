import numpy as np
import pandas as pd

No= int(input('Enter total bus: '))
Tr= int(input('Enter total transmission line: '))
F= []; T= []; Z= [] ;B= []
for i in range(Tr):
    print('===== Transmission line %d ====='%(i+1))
    f= int(input('Enter No.bus from: '));F.append(f)
    t= int(input('Enter No.bus to: '));T.append(t)
    z= complex(input('Enter impedance in format(R+Xj): '));Z.append(z)
    b= complex(input('Enter Shunt charging(Xj): ')) ;B.append(b)
print('F=',F)
print('T=',T)
print('Z=',Z)
print('B=',B)
cols1= [['No','From','To','Impedance','Shunt charging'],['','Bus','Bus',':',':']]
cn= np.arange(1,Tr+1)
L1= list(zip(cn,F,T,Z,B))
data1= pd.DataFrame(L1,columns=cols1).set_index(['No'])     ;print(data1)
y= 1/np.array(Z)                   ;print('y=',y)
Linedata= data1.values             #;print('Linedata=')      ;print(Linedata)
Y= np.zeros([No,No],dtype='complex')
Len= len(Linedata[:,0:1])           ;print('n=',Len)
F= np.array(np.array(F)-np.ones(Len),dtype='int')                    #;print(F)
T= np.array(np.array(T)-np.ones(Len),dtype='int')                     #;print(T)
for i in range(No):
    for j in range(Len):
        if F[j] == i or T[j] == i:
            Y[i,i]= Y[i,i] + y[j] + B[j]
for i in range(Len):
    if Y[F[i],T[i]] == 0:
        Y[F[i], T[i]] = Y[F[i], T[i]] - y[i]
        Y[T[i], F[i]] = Y[F[i], T[i]]
print('Y=');print(Y)
Ym= np.array(np.abs(Y)); YTheta= np.array(np.angle(Y))
print('Ym=');print(Ym)              ;print('YTheta=')       ;print(YTheta)
v= [];d= [];Pgen= [];Qgen= [];Pload= [];Qload= [];T= []
for i in range(No):
    print('========= Bus %d ========='%(i+1))
    v0= float(input('Enter valtage bus (p.u.) values ***: '));v.append(v0)
    d0= float(input('Enter angle bus (degree) values: '));d.append(d0)
    Pgen0= float(input('Enter Generation bus (MW) values: '));Pgen.append(Pgen0)
    Qgen0= float(input('Enter Generation bus (Mvar) values: '));Qgen.append(Qgen0)
    Pload0= float(input('Enter Load bus (MW) values: '));Pload.append(Pload0)
    Qload0= float(input('Enter Load bus (Mvar) values: '));Qload.append(Qload0)
    T0= int(input('Enter Type bus-> 1_(slack bus) 2_(PV bus) 3_(PQ bus) : '));T.append(T0)

cols2= ['No','Voltage','Angle','Pg','Qg','Pl','Ql','P','Q','Type']
L2= list(zip(cn,v,d,Pgen,Qgen,Pload,Qload,np.array(Pgen)-np.array(Pload),np.array(Qgen)-np.array(Qload),T))
data2= pd.DataFrame(L2,columns=cols2)   ;print(data2)
Sbase_MVA= 100
Vm= np.array(v); Delta= np.array(d)*(np.pi/180); Type= np.ndarray(T)
Pg= np.array(Pgen)/Sbase_MVA                                       ;print(Pg)
Qg= np.array(Qgen)/Sbase_MVA                                       ;print(Qg)
Pl= np.array(Pload)/Sbase_MVA                                      ;print(Pl)
Ql= np.array(Qload)/Sbase_MVA                                      ;print(Ql)
#P= np.array(data2[data2['P'] != 0].iloc[:,7].values)/Sbase_MVA     ;print(P)
#Q= np.array(data2[data2['Q'] != 0].iloc[:,8].values)/Sbase_MVA     ;print(Q)
P= np.array(data2.P.values)/Sbase_MVA  ;print('P=',P)
Q= np.array(data2.Q.values)/Sbase_MVA   ;print('Q=',Q)
pa= np.array(data2[data2['Type'] > 1].index.values)                ;print(pa)
o= len(pa)     ;print(o)
pv= np.array(data2[data2['Type'] > 2].index.values)                 ;print(pv)
l= len(pv)      ;print(l)
P=P[pa]         ;print('P=',P)
Q=Q[pv]         ;print('Q=',Q)
var= T.count(3)*2 + T.count(2) ;print(var)
Iter=0
R= 1

while True:
    Iter= Iter +1
    F= np.zeros([var])
    for i in range(o):
        SumP=0
        for j in range(No):
            SumP= SumP+Vm[pa[i]]*Vm[j]*Ym[pa[i],j]*np.cos(YTheta[pa[i],j] -Delta[pa[i]] +Delta[j])
            F[pa[i]]= SumP
            #print(F)
    F= F[pa] ;print(F)
    G= np.zeros([var])
    for i in range(l):
        SumQ=0
        for j in range(No):
            SumQ= SumQ-Vm[pv[i]]*Vm[j]*Ym[pv[i],j]*np.sin(YTheta[pv[i],j] -Delta[pv[i]] +Delta[j])
            G[pv[i]]= SumQ
            #print(G)
    G= G[pv] #;print(G)
    dP= P-F #;print(dP)
    dQ= Q-G #;print(dQ)
    Pm= np.concatenate([dP,dQ]) #;print(Pm)

    J11= np.zeros([T.count(3)+T.count(2),T.count(3)+T.count(2)]) #;print('J11=\n',J11)
    j1= J11
    J12= np.zeros([T.count(3)+T.count(2),T.count(3)]) #;print('J12=\n',J12)
    J21= np.zeros([T.count(3),T.count(3)+T.count(2)]) #;print('J21=\n',J21)
    J22= np.zeros([T.count(3),T.count(3)])            #;print('J22=\n',J22)
    J= np.hstack([ np.vstack([J11,J21]),np.vstack([J12,J22]) ]) #;print('J=\n',J);print('nj=',J.shape)
    #def J11():
    J1= np.zeros([o,No])
    for i in range(o): #0 Diagonal elements:
        for j in range(No): # 0,1       #p_i=[1,2] No_j= [0,1,2]  /pi != No_j
            if pa[i] != j :
                J1[i,j]= Vm[pa[i]]*Vm[j]*Ym[pa[i],j]*np.sin(YTheta[pa[i],j] +Delta[j] -Delta[pa[i]])
#                print('J1=\n',J1)
        for i in range(o): #Off-diagonal elements:
            for j in range(o):
                j1[i,j]= -Vm[pa[i]]*Vm[pa[j]]*Ym[pa[i],pa[j]]*np.sin(YTheta[pa[i],pa[j]] +Delta[pa[j]] -Delta[pa[i]])
                np.fill_diagonal(j1,J1.sum(axis=1))
#                print('j1=\n',j1)
    #def J12():
        j2= np.zeros([o,l])
        for i in range(o):
            for j in range(l):
                j2[i,j]= Vm[pa[i]]*Ym[pa[i],pv[j]]*np.cos(YTheta[pa[i],pv[j]] +Delta[pv[j]] -Delta[pa[i]])
#                 print('j2=\n',j2)
    #def J21():
        J3= np.zeros([No,No])
        for i in range(l):
            for k in range(No):
                if i != k:
                    J3[i,k]= Vm[pv[i]]*Vm[k]*Ym[pv[i],k]*np.cos(YTheta[pv[i],k] +Delta[k] -Delta[pv[i]])
#                    print(J3)
        j3= np.zeros([l,o])
        for i in range(l):
            for j in range(o):
                j3[i,j]= -Vm[pv[i]]*Vm[pa[j]]*Ym[pv[i],pa[j]]*np.cos(YTheta[pv[i],pa[j]] +Delta[pa[j]] -Delta[pv[i]])
#                print('j3=\n',j3)
    #def J22():
        j4= np.zeros([l,l])
        for i in range(l):
            for j in range(l):
                j4[i,j]= -Vm[pv[i]]*Ym[pv[i],pv[j]]*np.sin(YTheta[pv[i],pv[j]] +Delta[pv[j]] -Delta[pv[i]])
#                print('j4=',j4)
    #Jacobian
    J= np.hstack([ np.vstack([j1,j3]),np.vstack([j2,j4]) ]) #;print('J=\n',J);print('nj=',J.shape)
    Inv= np.linalg.inv(J)   #;print('Inv=\n',Inv)
    R= Inv.dot(Pm) #;print('R=\n',R)    #หรือR= np.dot(Inv,Pm) ;print('R=\n',R)
    RAngle= np.array(R[0:o])          #;print('RAngle=\n',RAngle)
    RVoltage= np.array(R[o+0:l+o])    #;print('RVoltage=\n',RVoltage)

    K=0
    for i in range(No):
        if T[i] == 2 or T[i] == 3:
            Delta[i]= RAngle[K] + Delta[i]
            K = K + 1
#            print('Delta=',Delta)
    K=0
    for i in range(No):
        if T[i] == 3:
            Vm[i]= RVoltage[K] + Vm[i]
            K = K + 1
#            print('Vm=',Vm)
    if  max(abs(R)) <= 0.00001:
        print('Results convergence ,Iteration = {}'.format(Iter))
        break
    elif Iter >= 60:
        print('Error: please check your system. [transmission line]')
        print('Iteration > {}'.format(Iter))
        break
#print('Iter=',Iter)
#print('Angle=',Delta*180/np.pi)
pp= np.array(data2[data2['Type'] == 1].index.values) #;print('pp=',pp)
s= len(pp)  #;print(s)               #how many quantaties to determine real power P(slack)
pq= np.array(data2[(data2['Type'] == 1) | (data2['Type'] == 2)].index.values)
#print('pq=',pq)                     #position to determine reactive power Q(PV bus...n)
r= len(pq)  #;print(r)
P_last= np.zeros(No)
Q_last= np.zeros(No)

for i in range(s):
    for j in range(No):
        P_last[pp[i]] = P_last[pp[i]] +Vm[pp[i]]*Vm[j]*Ym[pp[i],j]*np.cos(YTheta[pp[i],j]-Delta[pp[i]]+Delta[j])
P_last = P_last[pp]
#print('P_last=',P_last)

for i in range(r):
    for j in range(No):
        Q_last[pq[i]] = Q_last[pq[i]] -Vm[pq[i]]*Vm[j]*Ym[pq[i],j]*np.sin(YTheta[pq[i],j] -Delta[pq[i]] +Delta[j])
Q_last = Q_last[pq] + Ql[pq]
print('Q_last=',Q_last)

k=0
for i in range(No):
    if T[i] ==1 : # P slack
        Pg[i]=P_last[k]
        k = k+1
#        print('Pg=',Pg)
k=0
for i in range(No):
    if T[i] ==1 or T[i] ==2 : # total Q PV bus,PQ bus
        Qg[i]=Q_last[k]
        k = k+1
#        print('Qg=',Qg)

#calculate line loss
V= np.zeros(No,dtype='complex')
for i in range(No):
    V[i]= Vm[i]*(complex(np.cos(Delta[i]),np.sin(Delta[i])))
#print('V=\n',V) ;print(' ')
I= np.zeros([No,No],dtype='complex')
Sloss= np.zeros([No,No],dtype='complex')
for i in range(No):
    for j in range(No):
        I[i,j]= -Y[i,j]*(V[i]-V[j])
        Sloss[i,j]= V[i]*np.conj(I[i,j])*Sbase_MVA
#print(I);print('')
#print(Sloss)
#print('')
SL= np.zeros([No,No],dtype='complex')
for i in range(No):
    for j in range(No):
        if i !=j:
            SL[i,j]= (Sloss[i,j]+Sloss[j,i])
            SL[j,i]=SL[i,j]
#print('SL=');print(SL)
Total_loss= sum(np.unique(SL))

cols3= [['Bus','Voltage','Angle','Generation','Generation','Load','Load','Bus'],
        ['No','|V|(P.U)','δ(θ)','P(MW)','Q(Mvar)',' P(MW)','Q(Mvar)','Type']]
L3= list(zip(np.arange(1,No+1),Vm,Delta*180/np.pi,Pg*Sbase_MVA,Qg*Sbase_MVA,Pl*Sbase_MVA,Ql*Sbase_MVA,T))
data3= pd.DataFrame(L3,columns=cols3)
Total1= data3.iloc[:,3:7].sum() #;print(Total1)
Total1.name= 'Total'
data3= data3.append(Total1.transpose())
print('===========================================================================')
print('Iteration = {}'.format(Iter))
print('===========================================================================')
print(data1)
print('===========================================================================')
print(data2)
print('===========================================================================')
print(data3)
print('===========================================================================')
print(' ')
print('|====== Bus ======|=================== Line flow ====================|=================== Line loss ===================|== % Amps ==|')
for i in range(No):
    for j in range(No):
        if abs(Sloss[i,j]) != 0:
            print(f'| From {i+1:3} to {j+1:3} | {np.real(Sloss[i,j]):10.4f} MW | {np.imag(Sloss[i,j]):10.4f} Mvar | {abs(Sloss[i,j]):10.4f} MVA |'
                  f'{np.real(SL[i,j]):10.4f} MW | {np.imag(SL[i,j]):10.4f} Mvar | {abs(SL[i,j]):10.4f} MVA | {abs(I[i,j])*10:8.2f} % |')

print(f'|=== Total loss ==|==================================================|{np.real(Total_loss):10.4f} MW | {np.imag(Total_loss):10.4f} Mvar | {abs(Total_loss):10.4f} MVA |============|')



