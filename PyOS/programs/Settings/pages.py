import tkinter as tk;
import tkinter.ttk as ttk;
from PIL import Image,ImageTk;
import tkinter.messagebox as dialogs;
import threading as task;
import os,sys,time;
def read_conf(path):
    conf=configparser.ConfigParser();
    conf.read(path);
    conf_dict={};
    for section in conf.sections():
        conf_dict[section]={};
        for k,v in conf.items(section):
            conf_dict[section][k]=v;
        ##end
    ##end
    return conf_dict;
##end
def write_conf(path,newconf):
    conf=configparser.ConfigParser();
    # Update existing configuration with newconf values
    conf.read(path);
    for section,section_data in newconf.items():
        if not conf.has_section(section):
            conf.add_section(section);
        ##endif
        for key,value in section_data.items():
            conf.set(section,key,value);
        ##end
    ##end
    # Write the updated configuration back to the file
    with open(path,'w') as cfgfile:
        conf.write(cfgfile);
    ##endwith
##end
def create_bg_img(win,cvs,path):
    centerX=win.winfo_width()/2;
    centerY=win.winfo_height()/2;
    width=win.winfo_width();
    cvs.ogn_img=ogn_img=Image.open(path);
    aspect_ratio=ogn_img.width/ogn_img.height;
    new_height=int(width/aspect_ratio);
    cvs.bgimg=bgimg=ImageTk.PhotoImage(ogn_img.resize((width, new_height)),master=win);
    return cvs.create_image(centerX,centerY,image=bgimg,anchor=tk.CENTER);
##end
global page_;
page_=None;

def load_page(page,root,config):
    global page_;
    homedir=os.path.expanduser("~");
    conf=read_conf(homedir+"/pyde/main.conf");
    if page_!=None:
        page_.destroy();
        page_=None;
    ##endif
    if page=='Wi-Fi':
        pass;
    elif page=='Network':
        pass;
    elif page=='Bluetooth':
        pass;
    elif page=='Background':
        page_=tk.Frame(root,bg='#333');
        page_.place(relx=.25,rely=0,relwidth=0.75,relheight=1);
        currentDesktopBg=tk.Canvas(page_,bg='#333',highlightthickness=0,width=720,height=576);
        currentDesktopBg.place(relx=.5,rely=0,relwidth=.4,relheight=.3,anchor=tk.N);
        currentDesktopBg.update();
        currImgPath=conf["Main"]["background"];
        currImg=create_bg_img(currentDesktopBg,currentDesktopBg,currImgPath);
        
    ##endif
##end