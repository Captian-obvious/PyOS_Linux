from . import UI as uiw;
from . import LinuxUtils as linux;
from . import Filesystem as fs;
from . import libCommon as common;
global mainwin,config;
mainwin=None;
config={};
ui=uiw.UI();
thisdir=linux.os.path.dirname(linux.os.path.realpath(__file__));

def init(win,cfg):
    global mainwin,config;
    mainwin=win;
    config=cfg;
##end

def main(argc:int,argv:list[str]):
    if (argc>1):
        if (argv[1]=='--live'):
            #Install from Live Boot
            uiw.print_info('Running setup from Live Boot...');
            load_ui();
        ##endif
    ##endif
##end
def create_login_page(root):
    global mainwin,config;
    ui_theme=ui.Style(root);
    ui_theme.theme_use('clam');
    ui_theme.configure('TFrame',background='#333');
    ui_theme.configure('TLabel',background='#333',foreground='#fff');
    ui_theme.configure('TButton',background='#333',foreground='#fff');
    ui_theme.configure('TEntry',background='#333',foreground='#fff',fieldbackground='#333',border="#fff",highlightbackground='#f80',highlightcolor="#f80");
    ui_theme.configure('ERR.TLabel',background='#333',foreground="#f00");
    usrs=config['users'];
    var1=ui.StringVar(root);
    var2=ui.StringVar(root);
    var3=ui.StringVar(root);
    var4=ui.IntVar(root,0);
    swidth=.5 if mainwin.winfo_screenwidth()>640 else .6;
    sheight=.8;
    winc=ui.Canvas(root,bg='#333');
    winc.place(relx=.5,rely=.5,relwidth=swidth,relheight=sheight,anchor=ui.CENTER);
    winc.update();
    cwidth=winc.winfo_width();
    cheight=winc.winfo_height();
    winc.create_text(cwidth*.5,0,text='Welcome to PyNux\nTo Continue,\nAuthorization is required.',font=('Ubuntu',10),anchor=ui.N,fill='#fff');
    winc.create_text(cwidth*.1,cheight*.2,text='Username:',font=('Ubuntu',15),anchor=ui.NW,fill='#fff');
    uname_entry=ui.CEntry(winc,font=('Ubuntu',15),textvariable=var1);
    winc.create_window(cwidth*.5,cheight*.3,window=uname_entry);
    uname_entry.place(relx=.5,rely=.3,relwidth=.8,relheight=.1,anchor=ui.N);
    uname_entry.update();
    uname_entry.focus();
    winc.create_text(cwidth*.1,cheight*.4,text='Password:',font=('Ubuntu',15),anchor=ui.NW,fill='#fff');
    pw_entry=ui.CEntry(winc,font=('Ubuntu',15),show='*',textvariable=var2);
    pw_entry.place(relx=.5,rely=.5,relwidth=.8,relheight=.1,anchor=ui.N);
    winc.create_text(cwidth*.1,cheight*.6,text='Confirm Password:',font=('Ubuntu',15),anchor=ui.NW,fill='#fff');
    conf_pw_entry=ui.CEntry(winc,font=('Ubuntu',15),show='*',textvariable=var3);
    conf_pw_entry.place(relx=.5,rely=.7,relwidth=.8,relheight=.1,anchor=ui.N);
    
    conf_pw_entry.update();
    next_btn=ui.Button(winc,text='Next',font=('Ubuntu',15),fg="#fff",bg="#333");
    next_btn.place(relx=.5,rely=.9,relwidth=.5,relheight=.1);
    cancel_btn=ui.Button(winc,text='Cancel',font=('Ubuntu',15),fg="#fff",bg="#333");
    cancel_btn.place(rely=.9,relwidth=.5,relheight=.1);
    no_match_err=ui.CLabel(winc,text='Passwords do not match.',font=('Ubuntu',15),style='ERR.TLabel');
    no_uname_err=ui.CLabel(winc,text='Username is required.',font=('Ubuntu',15),style='ERR.TLabel');
    no_pw_err=ui.CLabel(winc,text='Password is required.',font=('Ubuntu',15),style='ERR.TLabel');
    def next_btn_fn():
        global mainwin,config;
        if (var1.get()==''):
            no_uname_err.place(relx=.1,rely=.8,relwidth=.8,relheight=.2);
            next_btn.place_forget();
            cancel_btn.place_forget();
            uname_entry.update();
            uname_entry.focus();
            mainwin.update();
            root.update();
            linux.time.sleep(1);
            no_uname_err.place_forget();
            next_btn.place(relx=.5,rely=.9,relwidth=.5,relheight=.1);
            cancel_btn.place(rely=.9,relwidth=.5,relheight=.1);
            mainwin.update();
            root.update();
            return;
        ##endif
        if (var2.get()=='' or var3.get()==''):
            no_pw_err.place(relx=.1,rely=.8,relwidth=.8,relheight=.2);
            next_btn.place_forget();
            cancel_btn.place_forget();
            uname_entry.update();
            uname_entry.focus();
            mainwin.update();
            root.update();
            linux.time.sleep(1);
            no_pw_err.place_forget();
            next_btn.place(relx=.5,rely=.9,relwidth=.5,relheight=.1);
            cancel_btn.place(rely=.9,relwidth=.5,relheight=.1);
            mainwin.update();
            root.update();
            return;
        ##endif
        if (var2.get()!=var3.get()):
            no_match_err.place(relx=.1,rely=.8,relwidth=.8,relheight=.2);
            next_btn.place_forget();
            cancel_btn.place_forget();
            uname_entry.update();
            uname_entry.focus();
            mainwin.update();
            root.update();
            linux.time.sleep(1);
            no_match_err.place_forget();
            next_btn.place(relx=.5,rely=.5,relwidth=.9,relheight=.1);
            cancel_btn.place(rely=.9,relwidth=.5,relheight=.1);
            mainwin.update();
            root.update();
            return;
        ##endif
        usr={
            "username":common.obfescate(var1.get(),mode="un"),
            "password":common.obfescate(var2.get(),mode="pw"),
            "root":False,
            "prof_pic":[thisdir+"/assets/images/default_person.svg",True],
            "desktop":[thisdir+"/assets/backgrounds/background.png",True],
            "privs":{
                "debug":False,
            },
        };
        linux.mkhome(usr['username']);
        usrs.append(usr);
        winc.update();
        root.update();
        winc.destroy();
        root.destroy();
        mainwin.update();
        config['setup_has_ran']=False;
        linux.write_cfg(thisdir+'/cfg/main.pycfg',config);
        stage3(usr);
    ##end
    def cancel_btn_fn():
        global mainwin,config;
        #just quits the installer for now
        quit();
    ##end
    next_btn.setCommand(common.bindFn(next_btn_fn));
    cancel_btn.setCommand(common.bindFn(cancel_btn_fn));
##end
def load_ui():
    global mainwin,config;
    uiw.print_info('Loading UI...');
    root=ui.Canvas(mainwin,bg='#333');
    common.create_bg_img(mainwin,root,thisdir+'/assets/backgrounds/background.png');
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    #create a login page/window for the default user and its name
    root.update();
    create_login_page(root);
    mainwin.update();
    root.update();
##end

def stage3(usr):
    global mainwin,config;
    from . import Desktop as desk;
    #Load the desktop application, and then exit.
    uiw.print_info('Loading Desktop...');
    desk.init(mainwin,config,usr);
    #start session
    desk.startSessionAfterInit(IsLive=True);
    mainwin.mainloop();
##end