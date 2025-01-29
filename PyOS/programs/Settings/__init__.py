import tkinter as tk;
import tkinter.ttk as ttk;
from PIL import Image,ImageTk;
import tkinter.messagebox as dialogs;
import threading as task;
import configparser,os,sys,time;
from . import pages as pg;
global config,desktopWin,desktops,bgImg,imported;
config={};
desktopWin=None;
desktops=None;
imported=False;
thisdir=os.path.dirname(os.path.realpath(__file__));
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
def init(win,cfg,desks):
    global config,desktopWin,desktops;
    config=cfg;
    desktopWin=win;
    desktops=desks;
##end
def main(argc,argv):
    root=tk.Tk();
    root.title("Settings");
    root.geometry("720x576");
    root.focus_force();
    root.iconphoto(True,tk.PhotoImage(master=root,file=thisdir+"/favicon.png"));
    root.config(bg="#333");
    valid_terminal_settings=['brightness','background','font','accent1','accent2','accent3'];
    current_config=read_conf(os.path.expanduser("~")+"/pyde/main.conf");
    if argc>1:
        if (argv[1]=='--cfg'):
            if argc>3:
                if (argv[2]=='-set'):
                    keyv=argv[3];
                    vals=keyv.split('=');
                    key=vals[0];
                    val=vals[1];
                    if key in valid_terminal_settings:
                        pass;
                    ##endif
                ##endif
            ##endif
        ##endif
    ##endif
    s=ttk.Style(master=root);
    s.configure('dark.Treeview',rowheight=32,font=('Ubuntu',11),background='#333',fieldbackground="#333",foreground='#fff');
    settings_sidebar=ttk.Treeview(root,columns=("#0"),style='dark.Treeview',show='tree');
    settings_sidebar.place(relx=0,rely=.5,relwidth=.25,relheight=1,anchor=tk.W);
    settings_sidebar.i3=icon3=tk.PhotoImage(master=root,file=thisdir+'/assets/bluetooth.png');
    settings_sidebar.i4=icon4=tk.PhotoImage(master=root,file=thisdir+'/assets/background.png');
    settings_sidebar.i5=icon5=tk.PhotoImage(master=root,file=thisdir+'/assets/appearance.png');
    settings_sidebar.i6=icon6=tk.PhotoImage(master=root,file=thisdir+'/assets/notifications.png');
    settings_sidebar.i7=icon7=tk.PhotoImage(master=root,file=thisdir+'/assets/search.png');
    settings_sidebar.i8=icon8=tk.PhotoImage(master=root,file=thisdir+'/assets/applications.png');
    settings_sidebar.i9=icon9=tk.PhotoImage(master=root,file=thisdir+'/assets/privacy.png');
    settings_sidebar.i10=icon10=tk.PhotoImage(master=root,file=thisdir+'/assets/accounts.png');

    settings_sidebar.i11=icon11=tk.PhotoImage(master=root,file=thisdir+'/assets/sharing.png');
    settings_sidebar.i12=icon12=tk.PhotoImage(master=root,file=thisdir+'/assets/sound.png');
    settings_sidebar.i13=icon13=tk.PhotoImage(master=root,file=thisdir+'/assets/power.png');
    settings_sidebar.i14=icon14=tk.PhotoImage(master=root,file=thisdir+'/assets/displays.png');
    settings_sidebar.i15=icon15=tk.PhotoImage(master=root,file=thisdir+'/assets/mouse_touchpad.png');
    settings_sidebar.i16=icon16=tk.PhotoImage(master=root,file=thisdir+'/assets/keyboard.png');
    settings_sidebar.i17=icon17=tk.PhotoImage(master=root,file=thisdir+'/assets/printers.png');
    settings_sidebar.i18=icon18=tk.PhotoImage(master=root,file=thisdir+'/assets/removable.png');
    settings_sidebar.i19=icon19=tk.PhotoImage(master=root,file=thisdir+'/assets/colors.png');
    settings_sidebar.i20=icon20=tk.PhotoImage(master=root,file=thisdir+'/assets/colors.png');
    settings_sidebar.i21=icon21=tk.PhotoImage(master=root,file=thisdir+'/assets/colors.png');
    settings_sidebar.update();
    settings_sidebar.heading('#0',text='Settings');
    settings_sidebar.column('#0',anchor=tk.W);
    settings_sidebar.insert('',tk.END,text='Wi-Fi');
    settings_sidebar.insert('',tk.END,text='Network');
    settings_sidebar.insert('',tk.END,text='Bluetooth',image=icon3);
    settings_sidebar.insert('',tk.END,text='Background',image=icon4);
    settings_sidebar.insert('',tk.END,text='Appearance',image=icon5);
    settings_sidebar.insert('',tk.END,text='Notifications',image=icon6);
    settings_sidebar.insert('',tk.END,text='Search',image=icon7);
    settings_sidebar.insert('',tk.END,text='Applications',image=icon8);
    settings_sidebar.insert('',tk.END,text='Privacy',image=icon9);
    settings_sidebar.insert('',tk.END,text='Accounts',image=icon10);
    settings_sidebar.insert('',tk.END,text='Sharing',image=icon11);
    settings_sidebar.insert('',tk.END,text='Sound',image=icon12);
    settings_sidebar.insert('',tk.END,text='Power',image=icon13);
    settings_sidebar.insert('',tk.END,text='Displays',image=icon14);
    settings_sidebar.insert('',tk.END,text='Mouse & Touchpad',image=icon15);
    settings_sidebar.insert('',tk.END,text='Keyboard Shortcuts',image=icon16);
    settings_sidebar.insert('',tk.END,text='Printers',image=icon17);
    settings_sidebar.insert('',tk.END,text='Removables',image=icon18);
    settings_sidebar.insert('',tk.END,text='Color',image=icon19);
    settings_sidebar.insert('',tk.END,text='Region & Language',image=icon20);
    settings_sidebar.insert('',tk.END,text='Universal Access',image=icon21);
    def settings_sidebar_select(event):
        selected=settings_sidebar.selection()[0];
        if selected=='':
            return;
        ##endif
        pg.load_page(settings_sidebar.item(selected)["text"],root,desktopWin,desktops,config);
    ##end
    settings_sidebar.bind('<Double-1>',lambda e:settings_sidebar_select(e));
##end
def configure_(name,value):
    if name=='brightness':
        pass;
    elif name=='background' and value!='':
        pass;
    ##endif
##end