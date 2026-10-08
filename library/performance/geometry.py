"""Superficies reutilizables; parametrizaciones exactas salvo redondeo."""
import math
IDENTITIES=[
 dict(id='toro',name='Toro',equation='(x^2+y^2+z^2+R^2-r^2)^2-4*R^2*(x^2+y^2)=0',parameters={'R':.62,'r':.25},bound=.9),
 dict(id='roman',name='Roman',equation='x^2*y^2+x^2*z^2+y^2*z^2-x*y*z=0',parameters={},bound=.55),
 dict(id='cono',name='Doble cono',equation='x^2+y^2-z^2=0',parameters={'z_limit':.7},bound=1.),
 dict(id='cassini',name='Cassini de dos lobulos',equation='((x-a)^2+y^2+z^2)*((x+a)^2+y^2+z^2)-b^4=0',parameters={'a':.65,'b':.68},bound=1.)]
def point(kind,u,v):
 c,s=math.cos,math.sin
 if kind==0:return ((.62+.25*c(v))*c(u),(.62+.25*c(v))*s(u),.25*s(v))
 if kind==1:
  a,b,z=c(v)*c(u),c(v)*s(u),s(v)
  return b*z,a*z,a*b
 if kind==2:
  z=.7*s(v);return z*c(u),z*s(u),z
 x=math.sqrt(.65**2+.68**2)*s(v)
 rho=math.sqrt(max(0,math.sqrt(.68**4+4*.65**2*x*x)-x*x-.65**2))
 return x,rho*c(u),rho*s(u)
def field(kind,p):
 x,y,z=p
 if kind==0:return (x*x+y*y+z*z+.62**2-.25**2)**2-4*.62**2*(x*x+y*y)
 if kind==1:return x*x*y*y+x*x*z*z+y*y*z*z-x*y*z
 if kind==2:return x*x+y*y-z*z
 return ((x-.65)**2+y*y+z*z)*((x+.65)**2+y*y+z*z)-.68**4
