# POWER	FLOW ANALYSIS
### `NEWTON-RAPHSON	METHOD	FOR	10	BUS`

by `Sitthiwut T.`

This chapter deals with the steady-state analysis of an in terconnected power system during normal operation. The system is assumed to be operating under balanced condition and is represented by a single-phase network. The network contains hundreds of nodes and branches with impedances specified in per unit on a common *MVA base*.

Network equations can be formulated systematically in a variety of forms. However, the node-voltage method, which is the most suitable form for many power system analyses, is commonly used. The formulation of the network equa tions in the nodal admittance form results in complex linear simultaneous algebraic equations in terms of node currents. When node currents are specified, the set of linear equations can be solved for the node voltages. However, in a power system, powers are known rather than currents. Thus, the resulting equations in terms of power, known as the power flow equation, become nonlinear and must be solved by iterative techniques. Power flow studies, commonly referred to as load flow, are the backbone of power system analysis and design. They are necessary for plan ning, operation, economic scheduling and exchange of power between utilities. In addition, power flow analysis is required for many other analyses such as transient stability and contingency studies.
![](figures/diagram_10bus.png)
_ _ _ _
### BUS ADMITTANCE MATRIX
> In order to obtain the node-voltage equations, consider the simple power system shown in Figure below. where impedances are expressed in per unit on a common *MVA base* and   for simplicity resistances are neglected. Since the nodal solution is based upon `Kirchhoff's current law`, *impedances are converted to admittance*, i.e.
![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B80%7D%20%5Cbg_white%20%5Cfn_jvn%20y_%7Bij%7D%3D%5Cfrac%7B1%7D%7Bz_%7Bij%7D%7D%3D%5Cfrac%7B1%7D%7Br_%7Bij%7D&plus;jx_%7Bij%7D%7D)

![](figures/impedance_diagram.PNG) ![](figures/KVL.PNG) 
###### figure above show Apllying KCL to the indendent nodes 1 through 4 results.

![](figures/node_equation.PNG)
###### Extending the above relation to an *`n bus system`*, the node-voltage equation in matrix is ![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B100%7D%20%5Cbg_white%20%5Cfn_jvn%20I_%7Bbus%7D%3DY_%7Bbus%7D%5Ccdot%20V_%7Bbus%7D)

The `diagonal element` of each node is the *sum of admittances connected to it*. It is known as the `self-admittance` or driving point admittance,

![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B100%7D%20%5Cbg_white%20%5Cfn_jvn%20Y_%7Bii%7D%3D%5Csum_%7Bj%3D0%7D%5E%7Bn%7Dy_%7Bij%7D%20%5Ccdots%20j%5Cneq%20i)

![](figures/diagonal.PNG)

The `off-diagonal element` is equal to the *negative of the admittance between the nodes*. It is known as the mutual admittance or transfer admittance,

![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B100%7D%20%5Cbg_white%20%5Cfn_jvn%20Y_%7Bij%7D%3DY_%7Bji%7D%3D-y_%7Bij%7D)

![](figures/off_diagonal.PNG) 
![](figures/admittance3bus.PNG)
###### The bus admittance matrix for the network *3 bus* in above Figure obtained by inspection.

![](figures/admittance10bus.PNG)
###### figure above show bus admittance matrix for the network *10 bus*.


















