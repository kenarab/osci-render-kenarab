-- BVC-02/03/05. DSP reutilizable sin música. Coeficientes fuera del cálculo por muestra.
local function bvc_soft(x) return x/(1+math.abs(x)) end
local function bvc_biquad(kind,rate,hz,q)
 hz=math.max(20,math.min(rate*.37,hz))
 local w=2*math.pi*hz/rate;local c=math.cos(w);local alpha=math.sin(w)/(2*q);local den=1+alpha
 local b0,b1,b2
 if kind=='band' then b0=alpha/den;b1=0;b2=-b0
 else b0=(1-c)/(2*den);b1=2*b0;b2=b0 end
 return {b0,b1,b2,-2*c/den,(1-alpha)/den,0,0}
end
local function bvc_filter(s,x)
 local y=s[1]*x+s[6];s[6]=s[2]*x-s[4]*y+s[7];s[7]=s[3]*x-s[5]*y
 return y
end
local function bvc_vocoder(rate)
 local s={rate=rate,bands={},attack=1-math.exp(-1/(rate*.006)),release=1-math.exp(-1/(rate*.07))}
 local high=math.min(5500,rate*.34)
 for i=1,12 do
  local hz=90*(high/90)^((i-1)/11)
  s.bands[i]={hz=hz,carrier=bvc_biquad('band',rate,hz,2.6),carrier2=bvc_biquad('band',rate,hz,2.6),
   modulator=bvc_biquad('band',rate,hz,2.6),modulator2=bvc_biquad('band',rate,hz,2.6),env=0}
 end
 return s
end
local function bvc_vocode(s,carrier,modulator)
 local sum=0
 for i=1,#s.bands do
  local b=s.bands[i];local m=math.abs(bvc_filter(b.modulator2,bvc_filter(b.modulator,modulator)))
  b.env=b.env+(m>b.env and s.attack or s.release)*(m-b.env)
  local c=bvc_filter(b.carrier2,bvc_filter(b.carrier,carrier))
  sum=sum+c*math.max(0,b.env-.0002)
 end
 return 12*sum -- compensación fija; salida final lleva saturación/margen.
end
local function bvc_blep(p,dt)
 if p<dt then local u=p/dt;return u+u-u*u-1 end
 if p>1-dt then local u=(p-1)/dt;return u*u+u+u+1 end
 return 0
end
local function bvc_saw(p,dt) return 2*p-1-bvc_blep(p,dt) end
local function bvc_lowpass(s,hz,q)
 local a=bvc_biquad('low',s.rate,hz,q);local b=bvc_biquad('low',s.rate,hz,.70710678)
 -- Conservar memoria de ambos filtros al actualizar coeficientes.
 if s.low1 then a[6],a[7]=s.low1[6],s.low1[7];b[6],b[7]=s.low2[6],s.low2[7] end
 s.low1,s.low2=a,b
end
local function bvc_engine(rate)
 local s={rate=rate,p=0,p2=0,pm=0,dcx=0,dcy=0,dc=math.exp(-2*math.pi*15/rate),vocoder=bvc_vocoder(rate)}
 bvc_lowpass(s,1100,1.1);return s
end
local function bvc_highpass(s,x)
 local y=x-s.dcx+s.dc*s.dcy;s.dcx=x;s.dcy=y;return y
end
