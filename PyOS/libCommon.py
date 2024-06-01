from . import UI as uiw;
from . import LinuxUtils as linux;
from PIL import Image,ImageTk;
import screeninfo;
ui=uiw.UI();

def rgbtohex(r,g,b):
    return f"#{r:02x}{g:02x}{b:02x}";
##end
def get_screens():
    monitors=screeninfo.get_monitors();
    return monitors;
##end
def bindFn(fn,*args,**kwargs):
    def nfn(*args2,**kwargs2):
        return fn(*args,*args2,**kwargs,**kwargs2);
    ##end
    return nfn;
##end
def interpolate_color(start_color, end_color, t):
    # Linear interpolation between start_color and end_color
    r = int((1-t) * start_color[0] + t * end_color[0]);
    g = int((1-t) * start_color[1] + t * end_color[1]);
    b = int((1-t) * start_color[2] + t * end_color[2]);
    return r,g,b;
##end
def create_bg_img(win,cvs,path):
    centerX=win.winfo_width()/2;
    centerY=win.winfo_height()/2;
    width=win.winfo_width();
    cvs.ogn_img=ogn_img=uiw.Image.open(path);
    aspect_ratio=ogn_img.width/ogn_img.height;
    new_height=int(width/aspect_ratio);
    cvs.bgimg=bgimg=uiw.tkImg.PhotoImage(ogn_img.resize((width, new_height)));
    return cvs.create_image(centerX,centerY,image=bgimg,anchor=ui.CENTER);
##end
def obfescate(s,mode='pw'):
    if mode=='pw':
        bytes=s.encode('utf-8');
        b64bytes=linux.pwencode(bytes);
        b64str=b64bytes.decode('ascii');
        return b64str;
    elif mode=='un':
        bytes=s.encode('utf-8');
        b64bytes=linux.usrnencode(bytes);
        b64str=b64bytes.decode('ascii');
        return b64str;
    ##endif
##end