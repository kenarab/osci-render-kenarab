"""Regenera recursos de la biblioteca sin música: python3 -m algebraic_surfaces.build."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from .core import mesh,panel

HERE=Path(__file__).resolve().parent
COLORS=[(96,216,219),(238,180,99),(186,151,234),(128,204,154)]

def build_assets():
    source=json.loads((HERE/'catalog.json').read_text())
    (HERE/'catalog.js').write_text('// Generado desde catalog.json; sin descargas al abrir el editor.\nwindow.SURFACE_CATALOG='+json.dumps(source,ensure_ascii=False)+';\n')
    image=Image.new('RGB',(1680,530),(10,17,27));draw=ImageDraw.Draw(image)
    font=ImageFont.load_default(size=22);small=ImageFont.load_default(size=17);result=[]
    for i,item in enumerate(source['surfaces']):
        vertices,faces,samples,report=mesh(item,output_dir=HERE/'assets')
        image.paste(panel(vertices,faces,item['bound'],COLORS[i]),(i*420,55))
        draw.text((i*420+20,20),item['name'],font=font,fill=COLORS[i])
        result.append((item,samples,report));print(item['name'],report['faces'],'caras',flush=True)
    draw.text((20,491),'F=0, mallas con caras dentro de cajas finitas. Biblioteca geometrica independiente de la musica.',font=small,fill='white')
    image.save(HERE/'assets/superficies.png')
    (HERE/'assets/geometry.json').write_text(json.dumps([r for _,_,r in result],indent=2)+'\n')
    return result

if __name__=='__main__':build_assets()
