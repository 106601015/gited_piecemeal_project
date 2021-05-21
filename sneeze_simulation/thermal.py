#from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math

#3D droplet trajectories using the initial velocity, angle and height of a sneeze, as well as droplet parameters and air resistance.
def drop_plot():
    #constant
    g=9.8 #m/s**2

    #Duration(0~2), cut to 30 point
    tgo=0 #s
    tend=2 #s
    cut=30 #cut

    #Define the initial velocity and angle and height of sneezing
    V0=177000/3600 #m/s
    theta=0*(math.pi/180) #angle(do)
    u0=V0*math.cos(theta) #m/s
    v0=0
    w0=V0*math.sin(theta) #m/s
    height=1.8 #m

    #Calculate drop parameters
    r=1.6/10**6 #m
    volume=(4/3)*math.pi*r**3
    mass=volume

    #calculate air resistance(air resistance=0.5* zo * v**2 * cd * a)(zo is air density, cd is constant, a is cross-sectional area)
    zo=1.293 #kg/m**3
    cd=0.47 #circle air resistance constant
    a=r*r*math.pi #m**2
    fd=0.5*zo*V0**2*cd*a #kg*m/s
    vend=(8*r*g/3/zo/cd)**0.5

    print('for drop radius=', r, ', terminal V=', vend)

    #road is droplet path, set 3D projection and limit x and z
    road=[]
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlim3d(0, 10)
    ax.set_zlim3d(0,2)

    #def Duration, x and z is function of t, np.array's +-*/ needs to be in a different form
    del_t = np.linspace(tgo, tend, cut)
    x_line = np.multiply(u0, del_t)
    z_line = np.add(np.add(height, np.subtract(0, np.divide(np.multiply(np.power(del_t, 2), g), 2))), np.multiply(del_t, w0))
    for i in range(10):
        y_line = np.linspace(float(i/10), float(i/10), cut)
        road.append(ax.plot3D(x_line, y_line, z_line, 'b'))

    plt.show()

#Show parcel horizontal distance over time
def show_parcel_horizontal(fr_magnification, u01, u02):
    #constant
    g=9.8 #m/s**2
    mu=18.5/10**6 #for air it is constant
    zo=1.293 #kg/m**3
    fr=mu/zo *10**5 * fr_magnification

    t1,t2,d1,d2,a1,a2=[],[],[],[],[],[] #time and distance

    u0=u01 #m/s
    for i in range(31): #for 3s
        t=float(i/10)
        t1.append(t)
        d1.append(u0/fr*(1-math.exp(-fr*t)))
        a1.append(9.7)

    u0=u02 #m/s
    for i in range(31): #for 3s
        t=float(i/10)
        t2.append(t)
        d2.append(u0/fr*(1-math.exp(-fr*t)))
        a2.append(3.5)

    #plot
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(t1, d1, label='V0=5m/s')
    ax.plot(t1, a1, 'r--')
    ax.plot(t2, d2, label='V0=14m/s')
    ax.plot(t2, a2, 'r--')
    plt.annotate('about 9.7m', (0,9.2))
    plt.annotate('about 3.5m', (0,3))
    ax.legend()
    plt.title('horizontal propagation distance', fontsize='large')
    ax.set_xlabel("time(s)", fontsize='large')
    ax.set_ylabel("distance(m)", fontsize='large')
    plt.show()

#input temp, return es
def cceq(T):
    return 2.53*10**11*math.exp(-5.42*1000/T)

#given parcel and environment parameters, calculate and plot how parcel go
def show_parcel_vertical(T, Te, rhp, rhe):
    #constant
    g=9.8 #m/s**2

    #parcel
    es=cceq(T) #Pa
    e=es*rhp #Pa
    q=0.622*e/101325
    Tv=T*(1+0.62*q) #virtual temperature
    #print('parcel:', T, 'K es=', es,', e=', e, ', q=', q, ', Tv=', Tv)

    #environment
    ese=cceq(Te) #Pa
    ee=ese*rhe #Pa
    qe=0.622*ee/101325
    Tve=Te*(1+0.62*qe) #virtual temperature
    #print('parcel:', Te, 'K es=', ese,', e=', ee, ', q=', qe, ', Tv=', Tve)

    deltaT=T-Te #init delta T
    cut=10 #how many cut in 1s
    accumulate=0.0

    t,d=[],[]
    for i in range(3*cut+1): #for 3s
        t1=float(i/cut)
        t.append(t1)

        accumulate+=((Tv-Tve)/Tve)*g*t1 / cut
        d.append(accumulate)
        #print('===>', t1, Tv, (Tv-Tve), ((Tv-Tve)/Tve)*g*t1 / cut, d[-1])
        if i<=cut: #in 1s
            T = T - deltaT/cut #Steady temperature drop
            es=cceq(T)
            if e>es: #if supersaturation, e=es
                e=es
            q=0.622*e/101325
            Tv=T*(1+0.62*q) #use new T and q to calculate Tv
            #print(T,es,e,Tv,Tve)

    #plot
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(t, d)
    plt.title('vertical propagation distance', fontsize='large')
    ax.set_xlabel("time(s)", fontsize='large')
    ax.set_ylabel("distance(m)", fontsize='large')
    plt.show()

#drop_plot()
show_parcel_horizontal(1,5,14)
show_parcel_vertical(300, 290, 0.9, 0.8)
print(cceq(300)/101325*0.622*1000)
print(cceq(339))