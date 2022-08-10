clc
clear
format short
No = input('Enter total bus: ');
n_Tr = input('Enter total transmission line: ');
for i = 1
  for j = 1:n_Tr
     i_n(j) = input('Enter No.bus from: ');
     j_n(j) = input('Enter No.bus to: ');
     Ri(j) = input('Enter R resistanace: ');
     Xi(j) = input('Enter X(i) reactance: ');
  end
end
Linedata = [i_n', j_n', Ri', imag(Xi)'];
printf('   | From |   |  To  |   |  R   |   |   X  |\n');
printf('   | Bus  |   |  Bus |   |  :   |   |   :  |\n');
disp(Linedata);

len = length(Linedata(:,1)) % length number in column1 or 2,3,4  =13
n = max(max(Linedata(:,1:2))); % number bus ,max value in column1,2  =10
Z = Ri + Xi;
y = 1./Z;                 %find admittance
Y_bus = zeros(No,No);
for i = 1:No   %1:10
  for j = 1:len   %1:13
    if i_n(j) == i | j_n(j) == i
      Y_bus(i,i) = Y_bus(i,i) + y(j);  % Y11= Y12 +Y13 +Y1n 
      fprintf(' ')
    else
      end
    end   
end
 
for i = 1:len    % 1:13
  if i_n > 0 & j_n > 0
    Y_bus(i_n(i),j_n(i)) = Y_bus(i_n(i),j_n(i)) -y(i);
    Y_bus(j_n(i),i_n(i)) = Y_bus(i_n(i),j_n(i));
    fprintf(' ')
  end
end
Y=Y_bus;     % Admittance matrix
Ym=abs(Y_bus)         %Magnitude of Admittance matrix
YTheta=angle(Y_bus)
%______________________________________________________________________________________%
v0 = zeros(No,1);
d0 = zeros(No,1);
Pgen = zeros(No,1);
Qgen = zeros(No,1);
Pload = zeros(No,1);
Qload = zeros(No,1);
T  = zeros(No,1);
for i = 1:No
  v0(i) = input('Enter valtage bus value**: ');
  d0(i) = input('Enter degree bus value: ');
  Pgen(i) = input('Enter MW Generator value: ');
  Qgen(i) = input('Enter Mvar Generator value: ');
  Pload(i) = input('Enter MW Load value: ');
  Qload(i) = input('Enter Mvar Load value: ');
  T(i) = input('Enter Type bus 1_(slack bus) 2_(PV bus) 3_(PQ bus) : ');
end
printf('     |No.  |  |Voltage|   |Angle|   |Gen.  |   |Gen.  |   |Load  |   |Load  |    |Type  |\n');
printf('     |of   |  |Per    |   |Per  |   |Pg    |   |Qg    |   |PL    |   |QL    |    |of    |\n');
printf('     |Bus  |  |Unit   |   |Unit |   |Power |   |Power |   |Power |   |Power |    |Bus   |\n');
disp([(1:No)' , v0 , d0 , Pgen ,  Qgen , Pload , Qload , T])
Busdata = [ v0 , d0 , Pgen ,  Qgen , Pload , Qload , T];


Vm=Busdata(:,1);  %Known voltage magnitude
Delta=Busdata(:,2); %Known angle in radian
type=Busdata(:,7); %Type of buses 1 for slack bus, 2 for P-V bus, 3 for P-Q bus
Pg=Busdata(:,3)/100; %Generated real power in per unit, base is 100 Watt
Pl=Busdata(:,5)/100; %real power for  load in per unit, base is 100 Watt
Qg=Busdata(:,4)/100; %Reactive power for generation in per unit, Base is 100 MVA
Ql=Busdata(:,6)/100; %Reactive power for load in per unit, base is 100 MVA
P=Pg-Pl; %Real power
Q=Qg-Ql; %Reactive power
pa=find(type>1) %Position to determine angle 
o=length(pa) %How many quantaties to determine angle
pv=find(type>2) %position to determine voltage
l=length(pv) %How many quantaties to determine voltage
P=P(pa,:)
Q=Q(pv,:)
Iter=0;
R = 1;

while max(abs(R))>=0.000001  

 
%___________________________________________________________________________________________%
Iter = Iter + 1;
SumP=0;
for ii=1:o
  SumP=0;
  for t=1:n %There is one slack bus
    SumP=SumP+Vm(pa(ii))*Vm(t)*Ym(pa(ii),t)*cos(YTheta(pa(ii),t)-Delta(pa(ii))+Delta(t));
    F(pa(ii),1)=SumP;
  end
end
F=F(pa,:);
for ii=1:l
  SumQ=0;  %Calculation of reactive power
  for t=1:n
     SumQ=SumQ-Vm(pv(ii))*Vm(t)*Ym(pv(ii),t)*sin(YTheta(pv(ii),t)-Delta(pv(ii))+Delta(t));
     G(pv(ii),1)=SumQ;
  end
end
G=G(pv,:);
dP=P-F;
dQ=Q-G;
Pm=[dP;dQ] % Power mismatch
for ii=1:o %Calculation of Jacobian matrix
    for k=1:o
        for u=1:l
            for v=1:l
                if (pa(ii)~=pa(k)|pa(ii)~=pv(u)|pv(u)~=pa(ii)|pv(u)~=pv(v)) %Off-diagonal element
                    H(pa(ii),pa(k))=-Vm(pa(ii))*Vm(pa(k))*Ym(pa(ii),pa(k))*sin(YTheta(pa(ii),pa(k))-Delta(pa(ii))+Delta(pa(k)));
                    L(pa(ii),pv(u))=Vm(pa(ii))*Ym(pa(ii),pv(u))*cos(YTheta(pa(ii),pv(u))-Delta(pa(ii))+Delta(pv(u)));
                    M(pv(u),pa(ii))=-1*Vm(pv(u))*Vm(pa(ii))*Ym(pv(u),pa(ii))*cos(YTheta(pv(u),pa(ii))-Delta(pv(u))+Delta(pa(ii)));
                    N(pv(u),pv(v))=-1*Vm(pv(u))*Ym(pv(u),pv(v))*sin(YTheta(pv(u),pv(v))-Delta(pv(u))+Delta(pv(v)));
                    else
                    sumH=0; sumL=0; sumM=0; sumN=0;  % Diagonal Element
                    for t=1:n
                      if (t~=pa(ii)|t~=pv(u))
                        sumH=sumH+Vm(pa(ii))*Vm(t)*Ym(pa(ii),t)*sin(YTheta(pa(ii),t)-Delta(pa(ii))+Delta(t));
                        H(pa(ii),pa(k))=sumH;
                        sumL=sumL+Vm(t)*Ym(pa(ii),t)*cos(YTheta(pa(ii),t)-Delta(pa(ii))+Delta(t));
                        L(pa(ii),pv(u))=sumL+2*Vm(pa(ii))*Ym(pa(ii),pa(ii))*cos(YTheta(pa(ii),pa(ii)));
                        sumM=sumM+Vm(pv(u))*Vm(t)*Ym(pv(u),t)*cos(YTheta(pv(u),t)-Delta(pv(u))+Delta(t));
                        M(pv(u),pa(ii))=sumM;
                        sumN=sumN+Vm(t)*Ym(pv(u),t)*sin(YTheta(pv(u),t)-Delta(pv(u))+Delta(t));
                        N(pv(u),pv(v))=-(sumN)-2*Vm(pv(u))*Ym(pv(u),pv(u))*sin(YTheta(pv(u),pv(u)));
                      end
                   end
                end
            end
        end
    end
end
H
L
M
N
H=H(:,pa);
H=H(pa,:);   % H Matrix
L=L(pa,:);
L=L(:,pv);   % L Matrix
M=M(pv,:);
M=M(:,pa);   % M Matrix
N=N(pv,:);
N=N(:,pv);

disp(Pm)    % N Matrix
J=[H L;M N]
R=J\Pm       % Result
RAngle=R(1:o); %Result angle in radian 
RVoltage=R(o+1:l+o); % Result Voltage 
k=1;
for ii=1:n;   %part delta
    if (type(ii)==2 | type(ii)==3)
        Delta(ii)=RAngle(k) + Delta(ii);
        k=k+1;
    end
end
k=1;
for ii=1:n    %part voltage
  if type(ii)==3
    Vm(ii)=RVoltage(k)+Vm(ii);
    k=k+1;
  end
end

%____________________________________________________________________________________________%
end
Iter
J
Delta
Vm
TR = [(1:No)' T , Vm , Delta*180/pi];
disp('  |  Bus | | Bus | |Voltage| |Angle|  ')  ;
disp('  |  No. | | Type| |Unit.  | |Deg. |  ')  ;
disp(TR); 
disp(' ');
%_________________________real power & reactive power_______________________________________%
pp=find(type==1)  %position to determine real power
s =length(pp) %how many quantaties to determine real power P(slack)
pq=find(type==1 | type==2) %position to determine reactive power Q(PV bus...n)
r =length(pq)

for i = 1:s
  sump=0;
  for t = 1:n   %1:totalbus
    sump = sump +Vm(pp(i))*Vm(t)*Ym(pp(i),t)*cos(YTheta(pp(i),t)-Delta(pp(i))+Delta(t));
    P_last(pp(i),1)=sump;
   end
end
P_last=P_last(pp,:)

for i = 1:r
  sumq=0;
  for t = 1:n  %1:totalbus
    sumq = sumq -Vm(pq(i))*Vm(t)*Ym(pq(i),t)*sin(YTheta(pq(i),t) -Delta(pq(i)) +Delta(t));
    Q_last(pq(i),1)=sumq;
  end
end
Q_last=Q_last(pq,:)

%__________________________________________generator(P)________________________________________%
k=1;
for i =1:n
  if type(i) ==1  % P slack 
    Pg(i)=P_last(k);
    k = k+1;
   end
end
%__________________________________________Load(Q)_____________________________________________�
k=1;
for i =1:n
  if type(i) ==1 | type(i) ==2 % total Q PV bus,PQ bus
    Qg(i)=Q_last(k);
    k = k+1;
  end
end
disp('')
  %| T->total ,G->Gen ,L->load ,P->real power, Q->reactive power |
TGP = sum(Pg)*100;TGQ = sum(Qg)*100;TLP = sum(Pl)*100;TLQ = sum(Ql)*100;
printf('     Bus        Voltage    Angle    ----Generation-----   -------Load--------     Bus   (1_Slack,2_PV,3_PQ) \n');
printf('     NO.        Unit       Deg.      MW            Mvar    MW            Mvar     Type  \n\n');
disp([(1:No)',Vm,Delta*180/pi,Pg*100,Qg*100,Pl*100,Ql*100,type]);
printf('     Total       Power     ------   %.4f   %.4f   %.4f   %.4f     ------ \n',TGP,TGQ,TLP,TLQ);
printf('     Total       Loss      ------   --------   --------    %.4f    %.4f     ------  \n\n',TGP-TLP,TGQ-TLQ);
disp('')
printf('_____________________________PROJECT_NEWTON_-_RAPHSON_LOAD_FLOW__AUTOMATIC_SYSTEM:_________________________________\n\n')%

printf('_____________________________________________BAM__KARFU__FIRN______________________________________________________\n\n')%

printf('_________________________________________62100540__62110002__62109855______________________________________________\n\n')%

printf('____________________________________________________END____________________________________________________________\n\n')%


