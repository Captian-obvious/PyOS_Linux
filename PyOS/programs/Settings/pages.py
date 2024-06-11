import tkinter as tk;
import tkinter.ttk as ttk;
from PIL import Image,ImageTk;
import tkinter.messagebox as dialogs;
import threading as task;
import os,sys,time;

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

def load_page(page,root,desktopWin,desktops,config):
    global page_;
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
        currImgPath=desktops[0].currentBackground;
        currImg=create_bg_img(currentDesktopBg,currentDesktopBg,currImgPath);
        
    ##endif
##end