from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math

def cceq(T):
    return 2.53*10**11*math.exp(-5.42*1000/T)

def show_parcel_3d():
    g=9.8 #m/s**2

    u0=14 #m/s
    mu=18.5/10**6 #for air it is constant
    zo=1.293 #kg/m**3
    fr=mu/zo *10**5
    T=300 #K
    es=cceq(T) #Pa
    e=es*0.9 #Pa
    q=0.622*e/101325
    Tv=T*(1+0.62*q) #virtual temperature
    #print('parcel:', T, 'K es=', es,', e=', e, ', q=', q, ', Tv=', Tv)

    #environment
    Te=295 #K
    ese=cceq(Te) #Pa
    ee=ese*0.6 #Pa
    qe=0.622*ee/101325
    Tve=Te*(1+0.62*qe) #virtual temperature
    #print('parcel:', Te, 'K es=', ese,', e=', ee, ', q=', qe, ', Tv=', Tve)

    deltaT=T-Te #init delta T
    cut=10 #how many cut in 1s
    accumulate=0.0

    road=[]
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlim3d(0, 10)
    ax.set_zlim3d(0,2)

    #def Duration, x and z is function of t, np.array's +-*/ needs to be in a different form
    tgo = 0
    tend = 3
    cut = 30
    del_t = np.linspace(tgo, tend, cut)
    x_line = np.multiply(u0/fr,np.subtract(1,np.exp(np.multiply(np.subtract(0,fr),del_t))))
    print(u0,np.multiply(fr,np.subtract(1,np.exp(np.multiply(np.subtract(0,fr),del_t)))))
    for i in range(3*cut+1): #for 3s
        #t1=float(i/cut)

        #z_line+=((Tv-Tve)/Tve)*g*del_t / cut
        accumulate += np.divide(np.multiply(((Tv-Tve)/Tve)*g, del_t),cut)
        z_line = np.add(1.7,accumulate)

        #print('===>', t1, Tv, (Tv-Tve), ((Tv-Tve)/Tve)*g*t1 / cut, d[-1])
        if i<=10: #in 1s
            T = T - deltaT/10 #Steady temperature drop
            es=cceq(T)
            if e>es: #if supersaturation, e=es
                e=es
            q=0.622*e/101325
            Tv=T*(1+0.62*q) #use new T and q to calculate Tv
            #print(T,es,e,Tv,Tve)
    
    y_line = np.linspace(1, 1, cut)
    road.append(ax.plot3D(x_line, y_line, z_line, 'b'))

    plt.show()


show_parcel_3d()