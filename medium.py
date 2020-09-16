import time # use as: tic = time.time(); elapsedTime = time.time() - tic
    # numerical modules
import numpy as np
from numpy import pi,sin,cos,sqrt
from scipy import integrate
    # for plotting (with latex)
import matplotlib.pyplot as plt # main plotting module
plt.rc('text',usetex=True) # for latex
plt.rc('font',family='serif') # for latex
    # for sending data to MATLAB
import scipy.io as sio

# treating division by 0
np.seterr(divide='ignore')

################  SOLVE ODE WITH FINITE DIFFERENCES + ITERATION ################
##### FOR NOW, ASSUME KNOWN VALUES OF DRAG COEFFICIENTS
ct = 0.5 # tangential drag coefficient
cn = 1.0 # normal drag coefficient

##### universal constants
g = 9.81 # gravity constant, m/s^2

##### plate details
W = 0.05 # width (m)
L = 0.15 # length (m)
h = 0.00005 # thickness (m)
B = 10**(-5) # bending stiffness
rhoPlate = 1.3*10**3 # density of plate, kg/m^3

##### towing velocity
U = 0.1 # m/s

##### fluid details
rhoFluid = 10**3 # density of fluid, kg/m^3
mu = 10**(-1) # dynamic viscosity, kg/(m s)

##### non-dimensional parameters
beta = (rhoPlate-rhoFluid)*g*h*L**3 / B # buyoancy constant
D = np.sqrt(L**5/W)*U*mu / B # drag constant
print('beta = ',beta,' and D = ',D,sep='')

    # initiate timer
tic = time.time()
    # set up grid
sBar = np.linspace(0,1,num=100)
dsBar = sBar[1]-sBar[0]
    # set up LHS
matSize = np.array([np.size(sBar),np.size(sBar)])
LHS = np.zeros(matSize, dtype=float)
        # boundary conditions
LHS[0,0] = 1 # BC at sBar = 0: theta = 0
LHS[-1,-3:] = np.array([1, -4, 3]) / (2*dsBar) # at sBar = 1: dtheta_dsBar = 0
        # second-order central finite difference
for n in range(1,np.size(sBar)-1):
    LHS[n,n-1] = 1/dsBar**2
    LHS[n,n] = -2/dsBar**2
    LHS[n,n+1] = 1/dsBar**2
    # set up RHS
RHS = np.zeros(np.size(sBar))
        # bondary conditions
RHS[0] = 0 # at sBar = 0: theta = 0
RHS[-1] = 0 # at sBar = 1: dtheta_dsBar = 0
    # set up iteration
thetaOld = np.linspace(0,1,num=np.size(sBar)) # initial guess
itErr = 1 # initiate error
itCount = 0 # iteration count
weightOld = 7 # relaxation factor, in favor of thetaOld
while (itErr > dsBar**2):
    itCount = itCount + 1 # update iteration count
    # set up RHS with thetaOld
        # normal vector in inertial frame (x,y)
    nx = cos(thetaOld)
    ny = sin(thetaOld)
        # external forcing / length
    Px = D * ( cn*cos(thetaOld)**2 + ct*sin(thetaOld)**2 )
    Py = D * ( (cn-ct)*sin(thetaOld)*cos(thetaOld) ) - beta*np.ones(np.size(sBar))
        # integrated external force / length -> internal force
    Fx0 = integrate.trapz(Px,sBar)
    Fy0 = integrate.trapz(Py,sBar)
    Fx = Fx0 - integrate.cumtrapz(Px,sBar,initial=0)
    Fy = Fy0 - integrate.cumtrapz(Py,sBar,initial=0)
        # fill up RHS
    for ns in range(1,np.size(sBar)-1): # internal ode, edges use BC's
        RHS[ns] = -( nx[ns]*Fx[ns] + ny[ns]*Fy[ns] )
    # solve for thetaNew
    thetaNew = np.linalg.solve(LHS,RHS)
    # check error and convergence criteria
    err = np.divide( (thetaNew-thetaOld) , thetaOld ) * dsBar/sBar[-1]
    err[np.isnan(err)] = 0 # remove NaN's from err, if divided by 0 for example
    err[np.isinf(err)] = 0
    itErr = sqrt(np.sum(np.dot(err,err)))
    # update for next iteration
    if itCount > 500:
        plt.plot(sBar,thetaNew,'-',sBar,thetaOld,'--')
        thetaOld = ( thetaNew + weightOld*thetaOld ) / (1+weightOld)
        break
    thetaOld = ( thetaNew + weightOld*thetaOld ) / (1+weightOld)

elapsedTime = time.time() - tic
print('Time to complete', itCount,'iterations is {:4.3f}'.format(elapsedTime),'seconds.')
theta = thetaNew
    # computing the derivative of the solution
dtheta_dsBar0 = ( -theta[2] + 4*theta[1] - 3*theta[0] ) / (2*dsBar)
dtheta_dsBar = ( theta[2:] - theta[:-2] ) / (2*dsBar)
dtheta_dsBarEND = ( 3*theta[-1] - 4*theta[-2] + theta[-3] ) / (2*dsBar)
dtheta_dsBar = np.insert(dtheta_dsBar,0,dtheta_dsBar0)
dtheta_dsBar = np.append(dtheta_dsBar,dtheta_dsBarEND)

############# kinematics to get xBar and yBar from theta ################
xBar = integrate.cumtrapz(sin(theta),sBar,initial=0)
yBar = integrate.cumtrapz(-cos(theta),sBar,initial=0)
dydx = np.diff(yBar) / np.diff(xBar)
dxdy = np.diff(xBar) / np.diff(yBar)
dyds = np.diff(yBar) / np.diff(sBar)
dxds = np.diff(xBar) / np.diff(sBar)
length_sBar = integrate.trapz( np.ones(np.size(sBar)), sBar)
length_dydx = integrate.trapz( sqrt(1+dydx**2), np.abs(xBar[1:]) ) # error when dydx = inf
length_dxdy = integrate.trapz( sqrt(1+dxdy**2), np.abs(yBar[1:]) ) # error when dxdy = inf
length_dthetads = integrate.trapz( 1/dtheta_dsBar[0:-2], theta[0:-2]) # ignore dt/ds = 0 at end
length_dds = integrate.trapz( sqrt(dxds**2 + dydx**2), sBar[1:])
print('length_sBar = ',length_sBar,'. \nlength_dydx = ',length_dydx,'. \nlength_dxdy = ',length_dxdy,'.',sep='')
print('length_dthetads = ',length_dthetads,'. \nlength_dds = ',length_dds,'.',sep = '')

########################## plotting the solution ##########################
fig = plt.figure()
#axes = plt.subplot(5,1,range(1,2))
axes = plt.subplot2grid((3,2), (0,0), colspan=2)
axes.plot(sBar,theta,sBar,dtheta_dsBar,'--')
axes.legend((r'$\theta$',r'$\mathrm{d}\theta/\mathrm{d}\overline{s}$'),loc=0)
axes.grid(True)
axes.set_xlabel(r'$\overline{s}$')
axes.set_title('solution to ODE')

#axes = plt.subplot(5,1,5)
axes = plt.subplot2grid((3,2), (1,0), colspan=2, rowspan=2)
axes.plot(xBar,yBar)
axes.set_xlabel(r'$\overline{x}$');
axes.set_ylabel(r'$\overline{y}$')
axes.grid(True)
axes.set_ylim(-1,0) #if yBar[-1] > 0 else axes.set_ylim(-1,0)
axes.set_xlim(-1,1) #if xBar[-1] > 0 else axes.set_xlim( np.ndarray.min(xBar),1)
axes.set_title('deformation of rod / uniform plate')

#plt.suptitle('this is a master title')
plt.tight_layout()
plt.savefig('statics.jpg',foramt='jpg')
plt.show()

########## save data to compare to experiments ##########
yExp = L*xBar.copy()
xExp = L*yBar.copy()
sio.savemat( 'np_xy.mat', { 'x':xExp ,'y':yExp } )