from django.shortcuts import render
import numpy as np

# Create your views here.
def home(request):
    return render(request, 'home.html')

def est(request):
    print(request)
    def dFac(r,T,t):
        return(np.exp(-r*(T-t)))
    
    def N(x):
        return(0.5*(1+np.erf(x/np.sqrt(2))))

    def C(S0,E,T,r,sigma,t):
        d1=(np.log(S0/E)+(r+sigma**2/2)*(T-t))/(sigma*np.sqrt(T-t))
        d2=(np.log(S0/E)+(r-sigma**2/2)*(T-t))/(sigma*np.sqrt(T-t))
        return(S0*N(d1)-E*dFac(r,T,t)*N(d2))

    def P(S0,E,T,r,sigma,t):
        d1=(np.log(S0/E)+(r+sigma**2/2)*(T-t))/(sigma*np.sqrt(T-t))
        d2=(np.log(S0/E)+(r-sigma**2/2)*(T-t))/(sigma*np.sqrt(T-t))
        return(E*dFac(r,T,t)*N(-d2)-S0*N(-d1))

    S0 = float(request.GET['spot_price'])
    E = float(request.GET['strike_price'])
    r = float(request.GET['rate'])
    sigma = float(request.GET['vol'])
    T = float(request.GET['expiry'])
    M = 100
    dt = T/M
    u = np.exp(r*dt)*(1+np.sqrt(np.exp(sigma**2*dt)-1))
    d = np.exp(r*dt)*(1-np.sqrt(np.exp(sigma**2*dt)-1))
    p = 1/2

    assetAtExpiry = (S0*d**np.arange(M,-1,-1))*(u**np.arange(0,M+1,1))
    putVal = np.maximum(E-assetAtExpiry,0) #put with strike E
    callVal = np.maximum(assetAtExpiry-E,0)  #call with strike E

    for i in range(int(M)-1,-1,-1):
        putVal= np.exp(-r*dt)*(p*putVal[range(1,i+2)]+(1-p)*putVal[range(0,i+1)])
        callVal= np.exp(-r*dt)*(p*callVal[range(1,i+2)]+(1-p)*callVal[range(0,i+1)])

    return render(request,'result.html', {'result1' : round(putVal[0],2), 'result2' : round(callVal[0],2)})
