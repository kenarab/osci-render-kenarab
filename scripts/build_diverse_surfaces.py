"""VIV-03: cuatro superficies XYZ, referencia con caras y galería sin audio."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from performance.geometry import IDENTITIES,point,field
from algebraic_surfaces.core import panel
from PIL import Image,ImageDraw,ImageFont
OUT=ROOT/'experiments/016-superficies-diversas';LIB=ROOT/'library/performance'
TEMPLATE='''-- @NAME@. F=0 y controles en README; coordenadas XYZ sin proyeccion previa.
-- A giro (0 pausa), B portadora 80–160 Hz, C cobertura 4–12 Hz. Preset ignora sliders.
local LIVE=@LIVE@
@GEOMETRY@
local ID='@NAME@-'..tostring(LIVE)
if not diverse_surface or diverse_surface.id~=ID or diverse_surface.rate~=sample_rate or step<diverse_surface.last then
 diverse_surface={id=ID,rate=sample_rate,last=step,u=0,v=0,angle=.65,hz=110,cover=7}
end
local s=diverse_surface;s.last=step;local dt=1/sample_rate;local k=1-math.exp(-dt/.08)
local function control(v,d) if not LIVE or type(v)~='number' or v~=v then return d end;return math.max(0,math.min(1,v)) end
s.hz=s.hz+k*(80+80*control(slider_b,.375)-s.hz)
s.cover=s.cover+k*(4+8*control(slider_c,.375)-s.cover)
s.angle=s.angle+.2*control(slider_a,.5)*dt
s.u=(s.u+s.hz*dt)%1;s.v=(s.v+s.cover*dt)%1
local x,y,z=geometry(@KIND@,2*math.pi*s.u,2*math.pi*s.v)
s.raw={x,y,z};s.kind=@KIND@;s.gain=.7/bounds[@KIND@]
return orient(x,y,z,s.angle,s.gain)
'''
def main():
 models=[];reports=[];image=Image.new('RGB',(1680,540),(10,17,27));draw=ImageDraw.Draw(image);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23)
 geo=(LIB/'geometry.lua').read_text()
 for kind,item in enumerate(IDENTITIES):
  n,m=48,96;vertices=[point(kind,2*math.pi*j/m,-math.pi/2+math.pi*i/n) for i in range(n+1) for j in range(m)]
  # Toro requires full minor angle; other maps use latitude in [-pi/2,pi/2].
  if kind==0:vertices=[point(kind,2*math.pi*j/m,2*math.pi*i/n) for i in range(n+1) for j in range(m)]
  faces=[]
  for i in range(n):
   for j in range(m):
    a=i*m+j;b=i*m+(j+1)%m;c=(i+1)*m+j;d=(i+1)*m+(j+1)%m
    faces.extend([[a,b,c],[b,d,c]])
  residual=max(abs(field(kind,p)) for p in vertices);assert residual<1e-12
  trace=[point(kind,2*math.pi*110*j/14000,2*math.pi*7*j/14000) for j in range(2000)]
  models.append(dict(id=item['id'],vertices=vertices,faces=faces,bound=item['bound'],trace=trace,source=item['equation']))
  reports.append(dict(id=item['id'],residual=residual,vertices=len(vertices),faces=len(faces),equation=item['equation'],parameters=item['parameters']))
  image.paste(panel(vertices,faces,item['bound'],(80,200,185),size=420),(420*kind,50));draw.text((420*kind+20,15),item['name'],font=font,fill='white')
  for live in (False,True):
   code=TEMPLATE.replace('@NAME@',item['id']).replace('@LIVE@',str(live).lower()).replace('@GEOMETRY@',geo).replace('@KIND@',str(kind+1))
   (OUT/(item['id']+('-control' if live else '')+'.lua')).write_text(code)
 draw.text((20,488),'Referencia con caras: no captura del host. Lua devuelve XYZ; cono recortado en |z| <= 0.7.',font=font,fill='white')
 image.save(ROOT/'recordings/016-superficies-diversas.png')
 (OUT/'models.js').write_text('window.XYZ_MODELS='+json.dumps(models,separators=(',',':'))+';\n')
 (OUT/'validacion.json').write_text(json.dumps(reports,indent=2,ensure_ascii=False)+'\n')
 # Reutilizar el visor existente sin modificarlo ni cargar repertorio anterior.
 stage=(ROOT/'apps/xyz-stage/stage.js').read_text().replace("['esfera']","[models[0].id]").replace('Recorrido del Lua y malla de la misma ecuación.','Malla y recorrido analítico de referencia; sin audio ni conexión al host.')
 (OUT/'gallery.js').write_text(stage)
 html=(ROOT/'apps/xyz-stage/index.html').read_text().replace('<option value="bach">Bach · violín solo</option><option value="oblivion">Oblivion · flauta sola</option>','').replace('src="../../library/algebraic_surfaces/geometry3d.js"','src="models.js"').replace('<script src="../../recordings/012-solos.js"></script>','').replace('src="stage.js"','src="gallery.js"').replace('Los timbres anteriores no se presentan como sonido de estos objetos.','Los timbres de 015 y 017 se derivan de estas ecuaciones; su mezcla sonora no conserva F=0.')
 html=html.replace('<label>Ejercicio<select', '<label hidden>Ejercicio<select').replace('<label>Instrumentos visibles<select','<label hidden>Instrumentos visibles<select').replace('<button id="play">','<button hidden id="play">').replace('<label>Tiempo <output','<label hidden>Tiempo <output').replace('La actividad musical cambia el brillo, no los vértices.','Caras y recorrido se pueden mostrar por separado.').replace('label{display:block;', 'label[hidden]{display:none}label{display:block;')
 (OUT/'index.html').write_text(html)
 print('4 superficies, ocho Lua y referencia con caras; F=0 <1e-12')
if __name__=='__main__':main()
