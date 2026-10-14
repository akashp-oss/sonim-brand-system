# IR Scale Lock blog cover illustration (run from the repo root: python3 brand/make_scale_lock.py).
# Source: the real breaker-panel capture (white-hot palette = relative heat). A hot motor housing is added at the
# right edge; the same scene is then coloured with an auto range (motor sets the top) and a locked range (the panel).
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
I=np.asarray(Image.open('library/src/img/thermal_p2.jpg').convert('L').resize((424,708),Image.LANCZOS)).astype(float)/255
H,W=I.shape
stops=[(0,(0,0,10)),(.15,(32,0,90)),(.35,(140,0,150)),(.55,(220,40,60)),(.72,(250,120,0)),(.88,(255,210,40)),(1,(255,255,230))]
def lut(x):
    x=np.clip(x,0,1); out=np.zeros(x.shape+(3,))
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
        m=(x>=a)&(x<=b); t=((x-a)/(b-a))[m][:,None]
        out[m]=np.array(ca)*(1-t)+np.array(cb)*t
    return out.astype(np.uint8)
# motor housing entering from the right edge (upper cabinet area, clear of the breakers): hot core, falling off to the casing
yy,xx=np.mgrid[0:H,0:W].astype(float)
cx,cy,R=W*1.02,H*0.24,W*0.30
r=np.sqrt((xx-cx)**2+(yy-cy)**2)/R
heat=np.where(r<1,2.8-1.3*r**2,0)                       # 2.8x the panel's brightest at the core, 1.5x at the casing
edge=np.clip((1.04-r)/0.06,0,1)                        # soft casing edge
m=np.maximum(I,heat*edge+I*(1-edge))
soft=np.asarray(Image.fromarray(np.uint8(np.clip(m/3,0,1)*255)).filter(ImageFilter.GaussianBlur(5))).astype(float)/255*3
scene=np.where(edge>0.01,np.maximum(I,soft),I)          # the motor at the camera's resolution
lo,hi=np.percentile(I,1),np.percentile(I,99.7)
Image.fromarray(lut((scene-lo)/(scene.max()-lo))).save('library/src/img/scale_auto.jpg',quality=90)
Image.fromarray(lut((scene-lo)/(hi-lo))).save('library/src/img/scale_locked.jpg',quality=90)
Image.fromarray(lut(np.linspace(0,1,512)[None,:].repeat(16,0))).save('library/src/img/scale_bar.png')
