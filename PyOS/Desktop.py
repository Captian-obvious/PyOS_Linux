from os.path import exists
from . import UI as uiw;
from . import Filesystem as fs;
from . import LinuxUtils as linux;
from . import Pointer as pt;
from . import libCommon as com;
from . import MainExe as lib_main;
#DESKTOP SYSTEM
ui=uiw.UI();
net_util=pt.Network_Utils();
global mainwin,config;
mainwin=None;
config={};
current_usr={};
sessionId=0;

def bindFn(fn,*args,**kwargs):
    return com.bindFn(fn,*args,**kwargs);
##end

def init(win,cfg,usr):
    global mainwin,config;
    mainwin=win;
    config=cfg;
    current_usr=usr;
    default_conf={
        "Main":{
            "background":thisdir+"/assets/backgrounds/background.png",
        },
        "Appearance":{
            "dock_orientation":"horizontal",
        },
        "Dock":{
            "color":"#333",
            "theme":"dark",
            "icon_size":"48",
            "extra_screens":True,
        }
    };
    homedir=linux.os.path.expanduser("~");
    if not (linux.os.path.exists(homedir+"/pyde/main.conf")):
        if not linux.os.path.exists(homedir+"/pyde"):
            linux.os.mkdir(homedir+"/pyde");
        ##endif
        linux.write_conf(homedir+"/pyde/main.conf",default_conf);
    ##endif
    if not (linux.os.path.exists(homedir+"/Desktop")):
        linux.os.mkdir(homedir+"/Desktop");
    ##endif
##end

def welcome_to_PyOS(root):
    global mainwin,config;
    #create a welcome message box with the text "Welcome to PyOS" and then (will continue)
    uiw.print_info('Welcome to PyOS');
    cvs=ui.Canvas(root,bg='#333');
    cvs.place(relx=.5,rely=.5,relwidth=.6,relheight=.8,anchor=ui.CENTER);
    cvs.update();
    canvaswidth=cvs.winfo_width();
    canvasheight=cvs.winfo_height();
    texts=[];
    def draw_p1():
        texts.append(cvs.create_text(canvaswidth*.5,0,text='Welcome to PyOS!',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.2,text='An operating system written entirely in Python!',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.4,text='With help from some basic Linux utilities, this operating system is quite lightweight and even comes with a UI!',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.6,text='Note: This is a major work in progress. Not everything functions yet.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
    ##end
    def draw_p2():
        texts.append(cvs.create_text(canvaswidth*.5,0,text='Welcome to PyOS!',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.2,text='This operating system is based on Ubuntu Linux\n and written with Tk and Qt.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.4,text='When this operating system was first envisioned.\n It was quite difficult to actually write, but eventually a team was assembled\n and work began.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.6,text='Note: This is a major work in progress. Not everything functions yet.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
    ##end
    def draw_p3():
        texts.append(cvs.create_text(canvaswidth*.5,0,text='Welcome to PyOS!',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.2,text='Once work began\n, it was made bootable in 2 years and now we have this!',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.4,text='As of now it is currently version 3.45.0',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.6,text='Note: This is a major work in progress.\n Not everything functions yet.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
    ##end
    def draw_p4():
        texts.append(cvs.create_text(canvaswidth*.5,0,text='Welcome to PyOS!',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.2,text='Setup will start.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(cvs.create_text(0,canvasheight*.6,text='Note: This is a major work in progress.\n Not everything functions yet.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
    ##end
    draw_p1();
    global part;
    part=1;
    next_btn=ui.Button(cvs,text='Next',font=('Ubuntu',15),fg="#fff",bg="#333");
    next_btn.place(relx=.5,rely=.9,relwidth=.5,relheight=.1);
    skip_btn=ui.Button(cvs,text='Skip',font=('Ubuntu',15),fg="#fff",bg="#333");
    skip_btn.place(rely=.9,relwidth=.5,relheight=.1);
    def next_btn_fn():
        global mainwin,config,part;
        cvs.delete(*texts);
        part+=1;
        if (part==2):
            draw_p2();
            root.update();
            cvs.update();
            mainwin.update();
        elif (part==3):
            draw_p3();
            root.update();
            cvs.update();
            mainwin.update();
        elif (part==4):
            draw_p4();
            skip_btn.place_forget();
            root.update();
            cvs.update();
            mainwin.update();
        else:
            cvs.delete(*texts);
            skip_btn.destroy();
            next_btn.destroy();
            live_setup(root,cvs);
            root.update();
            cvs.update();
            mainwin.update();
        ##endif
    ##end
    def skip_btn_fn():
        cvs.delete(*texts);
        skip_btn.destroy();
        next_btn.destroy();
        live_setup(root,cvs);
        root.update();
        cvs.update();
        mainwin.update();
    ##end
    skip_btn.setCommand(com.bindFn(skip_btn_fn));
    next_btn.setCommand(com.bindFn(next_btn_fn));
    root.update();
    cvs.update();
    mainwin.update();
##end

def live_setup(root,canvas):
    global mainwin,config,part;
    config['preinstalled']={};
    canvas.update();
    canvaswidth=canvas.winfo_width();
    canvasheight=canvas.winfo_height();
    texts=[];
    part=0;
    ui_style=ui.Style(root);
    ui_style.theme_use('clam');
    ui_style.configure('Color.Horizontal.TProgressbar',background='#f90',foreground="#333");
    var1=ui.IntVar(root,0);
    var2=ui.IntVar(root,0);
    var3=ui.IntVar(root,0);
    var4=ui.StringVar(root,'');
    var5=ui.IntVar(root,0);
    inst_progress=ui.IntVar(root,0);
    def cancel_cmd():
        #For now also just quits the program, there isnt any shutdown system yet. - :X: there is
        lib_main.shutdown(config);
    ##end
    def draw_p1():
        global part;
        part=1;
        texts.append(canvas.create_text(canvaswidth*.5,0,text='Lets get you set up.',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(canvas.create_text(0,canvasheight*.2,text='Which applications that are included\n would you like preinstalled?',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
        texts.append(canvas.create_text(0,canvasheight*.3,text='Applications will be installed in the "/usr/bin" folder.',font=('Ubuntu',10),anchor=ui.NW,fill='#fff'));
    ##end
    def draw_p2():
        global part;
        part=2;
        texts.append(canvas.create_text(canvaswidth*.5,0,text='Lets get you connected to the internet.',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(canvas.create_text(0,canvasheight*.2,text='Choose your local Wifi network.',font=('Ubuntu',15),anchor=ui.NW,fill='#fff'));
        available_networks=net_util.get_available_networks();
        if (len(available_networks)>0):
            print(f'There are {len(available_networks)} available networks.')
        ##endif
        root.update();
        canvas.update();
        mainwin.update();
    ##end
    def draw_p3():
        global part;
        part=3;
        texts.append(canvas.create_text(canvaswidth*.5,0,text='Lets get you set up.',font=('Ubuntu',20),anchor=ui.N,fill='#fff'));
        texts.append(canvas.create_text(0,canvasheight*.2,text='Installing selected packages...',font=('Ubuntu',15),anchor=ui.NW,fill='#fff'));
        progress=ui.Progressbar(canvas,orient=ui.HORIZONTAL,length=canvaswidth*.9,mode='determinate',variable=inst_progress,maximum=100,style="Color.Horizontal.TProgressbar");
        progress.place(relx=.5,rely=.7,relwidth=.9,relheight=.1,anchor=ui.N);
        def install_selected():
            global part;
            part=4;
            install_msg=canvas.create_text(canvaswidth*.5,canvasheight*.65,text='Initializing...',font=('Ubuntu',10),anchor=ui.N,fill="#fff");
            continue_btn.place_forget();
            cancel_btn.place_forget();
            texts.append(install_msg);
            root.update();
            canvas.update();
            mainwin.update();
            packages=config['preinstalled'];
            percent=0;
            #progress.start(50);
            for pkgname,v in packages.items():
                #For now we pretend to install bc the installer is not fully implemented yet.
                percent=0;
                pkg_str=v['name']+" v: "+v['version'];
                inst_progress.set(percent);
                progress.update();
                for i in range(410):
                    linux.time.sleep(.05);
                    percent=linux.math.floor((i/400)*100);
                    if (percent>100):
                        percent=100;
                    ##endif
                    if (percent<0):
                        percent=0;
                    ##endif
                    canvas.itemconfigure(install_msg,text="Extracting package "+pkg_str+"... "+str(percent)+"%");
                    inst_progress.set(percent);
                    progress.update();
                    root.update();
                    canvas.update();
                    mainwin.update();
                ##end
                linux.time.sleep(1);
                percent=0;
                inst_progress.set(percent);
                progress.update();
                for i in range(410):
                    linux.time.sleep(.1);
                    percent=linux.math.floor((i/400)*100);
                    if (percent>100):
                        percent=100;
                    ##endif
                    if (percent<0):
                        percent=0;
                    ##endif
                    canvas.itemconfigure(install_msg,text="Installing package "+pkg_str+"... "+str(percent)+"%");
                    inst_progress.set(percent);
                    progress.update();
                    root.update();
                    canvas.update();
                    mainwin.update();
                ##end
                linux.time.sleep(1);
            ##end
            percent=0;
            inst_progress.set(percent);
            progress.update();
            for i in range(205):
                linux.time.sleep(.2);
                percent=linux.math.floor((i/200)*100);
                if (percent>100):
                    percent=100;
                ##endif
                if (percent<0):
                    percent=0;
                ##endif
                canvas.itemconfigure(install_msg,text="Finalizing... "+str(percent)+"%");
                inst_progress.set(percent);
                progress.update();
                root.update();
                canvas.update();
                mainwin.update();
            ##end
            linux.time.sleep(1);
            canvas.itemconfigure(install_msg,text="Installation complete!");
            root.update();
            canvas.update();
            mainwin.update();
        ##end
        install_selected();
        continue_btn.place(relx=.5,rely=.9,relwidth=.5,relheight=.1);
        cancel_btn.place(rely=.9,relwidth=.5,relheight=.1);
        progress.place_forget();
        root.update();
        canvas.update();
        mainwin.update();
    ##end
    global textide_cb,browser_cb,media_cb;
    textide_cb=ui.Checkbutton(canvas,text='Textide (Text Editor)',font=('Ubuntu',10),fg='#fff',bg="#333",selectcolor="#333",variable=var1);
    textide_cb.place(relx=.5,rely=.4,relwidth=.8,relheight=.1,anchor=ui.N);
    browser_cb=ui.Checkbutton(canvas,text='Firefox (Mozilla)',font=('Ubuntu',10),fg='#fff',bg="#333",selectcolor="#333",variable=var2);
    browser_cb.place(relx=.5,rely=.5,relwidth=.8,relheight=.1,anchor=ui.N);
    media_cb=ui.Checkbutton(canvas,text='VLC (Media Player)',font=('Ubuntu',10),fg='#fff',bg="#333",selectcolor="#333",variable=var3);
    media_cb.place(relx=.5,rely=.6,relwidth=.8,relheight=.1,anchor=ui.N);
    continue_btn=ui.Button(canvas,text='Continue',font=('Ubuntu',15),fg="#fff",bg="#333");
    continue_btn.place(relx=.5,rely=.9,relwidth=.5,relheight=.1);
    cancel_btn=ui.Button(canvas,text='Cancel',font=('Ubuntu',15),fg="#fff",bg="red");
    cancel_btn.place(rely=.9,relwidth=.5,relheight=.1);
    def continue_btn_fn():
        global mainwin,config,part,textide_cb,browser_cb,media_cb;
        canvas.delete(*texts);
        if (textide_cb):
            textide_cb.destroy();
            textide_cb=None;
        ##endif
        if (browser_cb):
            browser_cb.destroy();
            browser_cb=None;
        ##endif
        if (media_cb):
            media_cb.destroy();
            media_cb=None;
        ##endif
        if (var1.get()==1):
            config['preinstalled']['textide']={"name":"Textide","version":"3.0.48.0","description":"Text Editor","license":"MIT"};
        ##endif
        if (var2.get()==1):
            config['preinstalled']['firefox']={"name":"Firefox","version":"125.0.2.0","description":"Mozilla Web Browser","license":"MIT"};
        ##endif
        if (var3.get()==1):
            config['preinstalled']['vlc']={"name":"VLC Media Player","version":"3.0.17.3","description":"General Purpose Media Player","license":"MIT"};
        ##endif
        if (part==1):
            linux.write_cfg("PyOS/cfg/main.pycfg",config);
            draw_p2();
        elif (part==2):
            linux.write_cfg("PyOS/cfg/main.pycfg",config);
            draw_p3();
        elif (part==4):
            config['setup_has_ran']=True;
            linux.write_cfg("PyOS/cfg/main.pycfg",config);
            root.destroy();
            canvas.destroy();
            goto_desktop();
        ##endif
        root.update();
        canvas.update();
        mainwin.update();
    ##end
    cancel_btn.setCommand(com.bindFn(cancel_cmd));
    continue_btn.setCommand(com.bindFn(continue_btn_fn));
    draw_p1();
    root.update();
    canvas.update();
    mainwin.update();
##end

def handle_shortcut_click(name,event):
    global mainwin,config,part;
    if (name=='firefox'):
        path='/usr/bin/firefox';
        if (linux.os.path.exists(path)):
            lib_main.run_application(path);
        ##endif
    elif (name=='vlc'):
        path=linux.os.path.join(linux.os.getcwd(),'usr','bin','vlc');
        if (linux.os.path.exists(path)):
            lib_main.run_application(path);
        ##endif
    ##endif
##end

def startSessionAfterInit(IsLive=False):
    global mainwin,config;
    #Create initial start ui
    uiw.print_info('Loading UI...');
    root=ui.Canvas(mainwin,bg='#333');
    homedir=linux.os.path.expanduser("~");
    conf=linux.read_conf(homedir+"/pyde/main.conf");
    com.create_bg_img(mainwin,root,conf['Main']["background"]);
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    mainwin.update();
    root.update();
    if (not IsLive):
        mainwin.destroy();
        goto_desktop();
        mainwin.mainloop();
    else:
        #Show the welcome message.
        welcome_to_PyOS(root);
    ##endif
##end
# opens files app
def open_files(path=linux.os.getcwd()):
    try:
        if linux.os.name=="nt":
            linux.runner.run(f"pythonw {thisdir}/programs/Files/main.pyw {path}");
        else:
            compilerThread=linux.task.Thread(target=lib_main.run_application,args=([f"{thisdir}/programs/Files/main.pyw",path],""));
            compilerThread.start();
        ##endif
    except Exception as err:
        uiw.print_info('Error: '+str(err));
    ##endtry
##end
def open_textide(path=linux.os.getcwd()):
    try:
        if linux.os.name=="nt":
            linux.runner.run(f"pythonw {thisdir}/programs/Textide/main.pyw {path}");
        else:
            compilerThread=linux.task.Thread(target=lib_main.run_application,args=([f"{thisdir}/programs/Textide/main.pyw",path],""));
            compilerThread.start();
        ##endif
    except Exception as err:
        uiw.print_info('Error: '+str(err));
    ##endtry
##end
def open_application(path,args): #Launch a non-builtin application using its path
    try:
        compilerThread=linux.task.Thread(target=lib_main.run_application,args=([path,*args],));
        compilerThread.start();
    except Exception as err:
        uiw.print_info('Error: Unable to launch application.');
    ##endtry
##end
global desktop_force_show;
desktop_force_show=False;

class DesktopWin(ui.Window):
    def __init__(self,screenName=None,width=400,height=300,title="Window",icon=None,**kwargs):
        ui.Window.__init__(self,screenName=screenName,width=width,height=height,title=title,icon=icon,**kwargs);
    ##end
##end

class Desktop(ui.Canvas):
    def __init__(self,master,cnf={},screenName=None,*a,**kwargs):
        ui.Canvas.__init__(self,master,cnf,*a,**kwargs);
        self.background_image=None
        self.currentBackground="";
        self.root=master;
        self.Screen=screenName;
    ##end
    def set_background(self,img):
        if (self.background_image!=None):
            self.currentBackground=img;
            centerX=self.winfo_width()/2;
            centerY=self.winfo_height()/2;
            width=self.winfo_width();
            self.ogn_img=ogn_img=uiw.Image.open(img);
            aspect_ratio=ogn_img.width/ogn_img.height;
            new_height=int(width/aspect_ratio);
            self.bgimg=bgimg=uiw.tkImg.PhotoImage(ogn_img.resize((width, new_height)));
            self.itemconfig(self.background_image,image=bgimg);
        else:
            self.currentBackground=img;
            self.background_image=com.create_bg_img(self.root,self,img);
        ##endif
        self.update();
    ##end
    def reload(self,dock):
        dock_icons_to_readd=dock.icons;
        dock.destroy();
        canvaswidth=self.winfo_width();
        canvasheight=self.winfo_height();
        # Fetch updated configuration
        homedir = linux.os.path.expanduser("~");
        conf = linux.read_conf(homedir + "/pyde/main.conf");
        # Determine canvas dimensions
        #canvaswidth = self.winfo_width();
        #canvasheight = self.winfo_height();
        # Initialize variables
        dockheight=int(conf["Dock"]["icon_size"] if conf["Dock"]["icon_size"] else 48);
        dwidth, dheight, doffset = 0, 0, dockheight;
        geom1 = True;  # Determine geometry orientation
        # Adjust dock dimensions based on configuration
        if conf["Appearance"]["dock_orientation"] == "horizontal":
            dwidth = canvaswidth - 96;
            dheight = dockheight;
            doffset = 48;
        elif conf["Appearance"]["dock_orientation"] == "vertical":
            dwidth = dockheight;
            dheight = canvasheight - 48;
            doffset = 0;
            geom1 = False;
        ##endif
        # Create a new Dock instance
        dock = Dock(self, self, bg='#333', width=dwidth, height=dheight);
        # Retrieve pinned apps and reload dock state
        dock.retrieve_pinned();
        dock.icons=dock_icons_to_readd;
        dock.reload();  # Call the reload method to refresh dock contents
        # Set dock geometry
        if geom1:
            dock.geometry(f"{dwidth}x{dheight}+{doffset}+{canvasheight-dheight}");
        else:
            dock.geometry(f"{dwidth}x{dheight}+0+{doffset}");
        ##end
        # Update the desktop appearance
        dock_handler(dock,self);
        dock.update();
        return dock;
    ##end
##end
desktops=[];
def open_settings(desktops,args):
    global mainwin,cfg;
    from .programs import Settings as s;
    s.imported=True;
    s.init(mainwin,config,desktops);
    cmdargs=['./Settings'];
    for i in range(len(args)):
        cmdargs.append(args[i-1]);
    ##end
    s.main(len(cmdargs),cmdargs);
##end

def new_desktop(show_dock=True,screenname=None):
    newroot=ui.Window(screenName=screenname);
    newroot.setAttribute('fullscreen',True);
    newroot.update();
    global mainwin,config,desktop_force_show;
    homedir=linux.os.path.expanduser("~");
    conf=linux.read_conf(homedir+"/pyde/main.conf");
    #Create the desktop
    desktop=Desktop(newroot,screenName=screenname,bg='#333');
    canvaswidth=newroot.winfo_width();
    canvasheight=newroot.winfo_height();
    print(canvasheight,canvaswidth);
    desktop.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    theimg=conf["Main"]["background"];
    desktop.set_background(theimg);
    desktops.append(desktop);
    dockheight=int(conf["Dock"]["icon_size"] if conf["Dock"]["icon_size"] else 48);
    desktop.di=dock_img=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/dock.png');
    desktop.dhi=dock_hover_img=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/dock_hover.png');
    desktop.dci=dock_click_img=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/dock_click.png');
    desktop.di2=dash_img=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/dash.png');
    global img;
    img=desktop.background_image;
    #img=com.create_bg_img(mainwin,desktop,thisdir+'/assets/backgrounds/background.png');
    power_menu=ui.Menu(newroot,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    power_menu.add_command(label='Shutdown',command=lambda:lib_main.shutdown(config));
    power_menu.add_command(label='Restart',command=lambda:lib_main.restart(config));
    application_menu=ui.Menu(newroot,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    application_menu.add_command(label="Terminal",command=bindFn(lib_main.open_terminal));
    application_menu.add_command(label="Files",command=open_files);
    right_click_menu=ui.Menu(newroot,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    right_click_menu.add_command(label='Create new');
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Paste");
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Select all");
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Arrange all");
    right_click_menu.add_command(label="Arrange by");
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Open in files",command=bindFn(open_files,linux.os.path.join(linux.os.path.expanduser("~"),"/Desktop") if linux.os.path.exists(linux.os.path.join(linux.os.path.expanduser("~"),"/Desktop")) else linux.os.getcwd()));
    right_click_menu.add_command(label='Open in Terminal',command=bindFn(lib_main.open_terminal,linux.os.path.join(linux.os.path.expanduser("~"),"/Desktop") if linux.os.path.exists(linux.os.path.join(linux.os.path.expanduser("~"),"/Desktop")) else linux.os.getcwd()));
    right_click_menu.add_cascade(label="Applications",menu=application_menu);
    right_click_menu.add_separator();
    right_click_menu.add_command(label='Change background',command=bindFn(open_settings,desktops,args=['--cfg','background']));

    right_click_menu.add_separator();
    right_click_menu.add_command(label="Display Settings",command=bindFn(open_settings,desktops,args=['--cfg','display']));
    right_click_menu.add_command(label="Desktop Symbol Settings");
    right_click_menu.add_separator();
    right_click_menu.add_cascade(label="Power",menu=power_menu);
    def desktop_clicked(event):
        global desktop_force_show;
        #after that we would usually check whats near the click point and if its a shortcut we open it
        desktop_stacking_order_override(newroot)
    ##end
    def on_desktop_focus(event):
        global desktop_force_show;
        desktop_stacking_order_override(newroot)
    ##end
    def desktop_back_if_not_shown(event):
        newroot.lower();
    ##end
    def dock_btn_hover(event):
        desktop.itemconfig(dock_btn,image=dock_hover_img);  
        desktop.config(cursor="hand2");
        desktop.update();
    ##end
    def dock_btn_hover_leave(event):
        desktop.itemconfig(dock_btn,image=dock_img);
        desktop.config(cursor="");
        desktop.update();
    ##end
    global debounce,dock_shown,opendb2;
    debounce=False;
    opendb2=False;
    dock_shown=False;
    def toggle_dock():
        global dock_shown,opendb2,desktop_force_show;
        if not opendb2:
            opendb2=True;
            if dock_shown:
                dock_shown=False;
                for i in range(dockheight):
                    if conf["Appearance"]["dock_orientation"]=="horizontal":
                        dock.geometry(f"{dwidth}x{dheight}+{doffset}+{canvasheight-(dockheight-i)}");
                    else:
                        dock.geometry(f"{dwidth}x{dheight}+{0-i}+{doffset}");
                    ##endif
                    newroot.update();
                    dock.update();
                    if not desktop_force_show:
                        newroot.attributes('-topmost',0);
                    ##endif
                ##end
            else:
                dock_shown=True;
                for i in range(dockheight):
                    if conf["Appearance"]["dock_orientation"]=="horizontal":
                        dock.geometry(f"{dwidth}x{dheight}+{doffset}+{canvasheight-i}");
                    else:
                        dock.geometry(f"{dwidth}x{dheight}+{0-(dockheight-i)}+0");
                    ##endif
                    newroot.update();
                    dock.update();
                    if not desktop_force_show:
                        newroot.attributes('-topmost',0);
                    ##endif
                ##end
            ##endif
            opendb2=False;
        ##endif
    ##end
    def dock_btn_click(event):
        global debounce;
        if debounce!=True:
            desktop.itemconfig(dock_btn,image=dock_click_img);
            debounce=True;
            toggle=linux.task.Thread(target=toggle_dock);
            toggle.start();
            newroot.lower();
            linux.time.sleep(.1);
            debounce=False;
            desktop.itemconfig(dock_btn,image=dock_hover_img);
        ##endif
    ##end
    def dash_btn_click(event):
        pass;
    ##end
    def rc_menu_fn(event):
        right_click_menu.tk_popup(event.x_root,event.y_root);
        right_click_menu.focus_force();
    ##end
    dock_btn=desktop.create_image(0,canvasheight,image=dock_img,anchor=ui.SW);
    dwidth=0;
    dheight=0;
    doffset=48;
    geom1=True;
    if conf["Appearance"]["dock_orientation"]=="horizontal":
        dwidth=canvaswidth-96;
        dheight=dockheight;
        doffset=48;
    ##endif
    if conf["Appearance"]["dock_orientation"]=="vertical":
        dwidth=dockheight;
        dheight=canvasheight-48;
        doffset=0;
        geom1=False;
    ##endif
    global dock;
    dock=Dock(desktop,desktop,bg='#333',width=dheight,height=dheight);
    dock.retrieve_pinned();
    dock.update();
    if geom1:
        dock.geometry(f"{dwidth}x{dheight}+{doffset}+{canvasheight-dockheight}");
    else:
        dock.geometry(f"{dwidth}x{dheight}+0+{doffset}");
    ##endif
    dash_btn=dock.canvas.create_image(0,0,image=dash_img,anchor=ui.NW);
    def reload_desk():
        global dock;
        dock=desktop.reload(dock);
    ##end
    desktop.update();
    right_click_menu.add_command(label="Reload Desktop",command=reload_desk);
    desktop.tag_bind(dock_btn,'<Button-1>',dock_btn_click);
    desktop.tag_bind(dock_btn,'<Enter>',dock_btn_hover);
    desktop.tag_bind(dock_btn,'<Leave>',dock_btn_hover_leave);
    desktop.bind('<Button-1>',bindFn(desktop_clicked));
    desktop.bind('<Button-3>',bindFn(rc_menu_fn));
    desktop.bind('<FocusIn>',bindFn(on_desktop_focus));
    newroot.bind('<FocusIn>',bindFn(on_desktop_focus));
    dock.bind('<FocusIn>',bindFn(on_desktop_focus));
    dock.bind('<Button-1>',bindFn(on_desktop_focus));
    dock_handler(dock,desktop);
    return desktop,newroot;
##end

def get_tasks():
    global mainwin,config;
    
##end

def desktop_stacking_order_override(deskWin):
    deskWin.update();
    if not desktop_force_show:
        deskWin.attributes('-topmost',0);
    ##endif
##end

def goto_desktop():
    global mainwin,config,desktop_force_show,active_screens;
    active_screens=[];
    try:
        screens=com.get_screens();
        if (len(screens)>1):
            for i in range(len(screens)):
                active_screens.append(screens[i].name);
            ##end
        ##endif
    except Exception as err:
        uiw.print_info('Unable to get screens: '+str(err));
    ##endtry
    #Create the desktop
    desktop,mainwin=new_desktop();
    lib_main.set_current_window(mainwin);
    for i in range(len(active_screens)):
        if (active_screens[i]!=desktops[0].Screen):
            new_desktop(conf["Dock"]["extra_screens"],active_screens[i]);
        ##endif
    ##end
##end
global dash_active,dash_canvas,dash_objects,opendb,thisdir;
thisdir=linux.os.path.dirname(linux.os.path.realpath(__file__));
dash_active=False;
dash_canvas=None;
opendb=False;
class Dock(ui.Toplevel):
    def __init__(self,master,desktop=None,bg=None,width=400,height=300,**kwargs):
        ui.Toplevel.__init__(self,master,width=width,height=height,**kwargs);
        self.master=master;
        self.linked_desktop=desktop;
        self.thestyle=ui.Style(self);
        self.thestyle.theme_use('clam');
        self.iconsize=48;
        self.faviconsize=32;
        self.padding=8;
        self.icons=[];
        self.themenu=None;
        self.selected_icon=None;
        if linux.os.name=='nt':
            self.overrideredirect(True);
            self.attributes('-topmost',1);
        else:
            self.attributes('-type','dock');
        ##endif
        self.setTitle('Dock');
        self.canvas=ui.Canvas(self,bg=bg,width=width,height=height);
        self.canvas.pack(expand=1,fill=ui.BOTH);
    ##end
    def add_icon(self,icon_path,name='',appid=0,exec=None,isPinned=False,pid=None,opened=False):
        homedir=linux.os.path.expanduser("~");
        conf=linux.read_conf(homedir+"/pyde/main.conf");
        orientation=conf["Appearance"]["dock_orientation"];
        width=self.faviconsize;
        self.ogn_img=ogn_img=uiw.Image.open(icon_path);
        aspect_ratio=ogn_img.width/ogn_img.height;
        new_height=int(width/aspect_ratio);
        self.tmp_icon=icon=uiw.tkImg.PhotoImage(ogn_img.resize((width,new_height)));
        id=len(self.icons)+1;
        x1=48+(id-1)*self.iconsize;
        y1=0;
        if orientation=='vertical':
            x1=0;
            y1=48+(id-1)*self.iconsize;
        ##endif
        x2=x1+self.iconsize;
        y2=y1+self.iconsize;  # Fixed y position with padding
        y3=self.linked_desktop.winfo_height()-48;
        if orientation=='vertical':
            y3=y2-self.iconsize//2;
        ##end
        font_size=9;
        background=self.canvas.create_rectangle(x1,y1,x2,y2,fill='#333',outline='#333');
        icon_widget=self.canvas.create_image(x1+self.iconsize//2,y1+self.iconsize//2,image=icon,anchor=ui.CENTER);
        label_width=int(len(name)*font_size);  # Calculate text width
        label_height=int(font_size*1.7);
        # Create the Toplevel window
        name_widget=ui.Toplevel(self.linked_desktop);
        name_widget.title("Toplevel");
        name_widget.config(bg="#333");
        if linux.os.name=='nt':
            name_widget.overrideredirect(True);
            name_widget.attributes('-topmost',1);
        else:
            name_widget.attributes('-type','dock');
        ##endif
        name_widget.geometry(f"{label_width}x{label_height}+{(x1+48+self.iconsize//2)-label_width//2}+{y3-label_height}");
        name_label=ui.Label(name_widget,text=name,bg='#333',fg='#fff',font=("Ubuntu",font_size));
        name_label.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
        name_widget.update();
        name_widget.update_idletasks();
        name_widget.deiconify();
        name_widget.geometry(f"{label_width}x{label_height}+{(x1+48+self.iconsize//2)-label_width//2}+{y3-label_height}");
        if linux.os.name=='nt':
            name_widget.overrideredirect(False);
        ##endif
        name_widget.iconify();
        #name_widget=self.linked_desktop.create_text(x1+48+self.iconsize//2,y3,text=name,anchor=ui.S,fill="#fff",font=("Ubuntu",9),state=ui.HIDDEN);
        ico_desc={
            'id':id,
            'img':icon_widget,
            'bg_widget':background,
            'name_widget':name_widget,
            'x':x1,
            'y':y1,
            'w':self.iconsize,
            'h':self.iconsize,
            'icon':icon,
            'icon_path':icon_path,
            'app_id':appid,
            'name':name,
            'exec':exec, #command ran when clicked
            'selected':False,
            'pinned':isPinned,
            'opened':opened, #if true prevents 'exec' from running.
            'pid':pid,
            'open_bar':None,
        };
        global icon_debounce;
        icon_debounce=False;
        def move_to_pos():
            name_widget.geometry(f"{label_width}x{label_height}+{(x1+48+self.iconsize//2)-label_width//2}+{y3-label_height}");
        ##end
        def on_hover(event):
            self.canvas.itemconfig(background,fill="#444",outline="#444");
            #self.linked_desktop.itemconfig(name_widget,state=ui.NORMAL);
            if linux.os.name=='nt':
                name_widget.overrideredirect(True);
            ##endif
            name_widget.deiconify();
            move_to_pos();
            self.config(cursor="hand2");
            self.selected_icon=id;
        ##end
        def on_leave(event):
            self.canvas.itemconfig(background,fill="#333",outline="#333");
            #self.linked_desktop.itemconfig(name_widget,state=ui.HIDDEN);
            move_to_pos();
            if linux.os.name=='nt':
                name_widget.overrideredirect(False);
            ##endif
            name_widget.iconify();
            #name_widget.geometry(f"{label_width}x{int(font_size*1.7)}+{x1+48+label_width//2}+{y3}");
            name_widget.update();
            self.config(cursor="");
            self.selected_icon=None;
        ##end
        def on_click(event):
            global icon_debounce;
            if not icon_debounce:
                icon_debounce=True;
                self.canvas.itemconfig(background,fill="#555",outline="#555");
                theicon=self.get_icon_by_exec(exec);
                if not theicon['opened']:
                    self.open_app(exec);
                else:
                    linux.focus_process(theicon['pid']);
                ##endif
                linux.time.sleep(.1);
                icon_debounce=False;
            ##endif
        ##end
        def on_rclick(event):
            global icon_debounce;
            if not icon_debounce:
                icon_debounce=True;
                self.open_icon_rclick_menu(event);
                linux.time.sleep(.1);
                icon_debounce=False;
            ##endif
        ##end
        self.canvas.tag_bind(background,'<Button-1>',on_click);
        self.canvas.tag_bind(icon_widget,'<Button-1>',on_click);
        self.canvas.tag_bind(background,'<Button-3>',on_rclick);
        self.canvas.tag_bind(icon_widget,'<Button-3>',on_rclick);
        self.canvas.tag_bind(background,'<Enter>',on_hover);
        self.canvas.tag_bind(icon_widget,'<Enter>',on_hover);
        self.canvas.tag_bind(background,'<Leave>',on_leave);
        self.canvas.tag_bind(icon_widget,'<Leave>',on_leave);
        self.icons.append(ico_desc);
    ##end
    def reload(self):
        # Clear the canvas
        self.canvas.delete("all")
        # Retain previous icons for reuse
        previcons=self.icons;
        self.icons=[];
        # Reload configuration
        homedir=linux.os.path.expanduser("~");
        conf=linux.read_conf(homedir + "/pyde/main.conf");
        # Update dock settings
        # Re-add icons based on the updated configuration
        for icon in previcons:
            if icon["opened"]:
                self.add_icon(
                    icon_path=icon["icon_path"],
                    name=icon["name"],
                    appid=icon["app_id"],
                    exec=icon["exec"],
                    isPinned=icon["isPinned"],
                    pid=icon["pid"],
                    opened=icon["opened"]
                );
            ##endif
        ##end
        # Refresh the dock's appearance
        self.update()
    ##end
    def on_unpin(self,event):
        global icon_debounce;
        if not icon_debounce:
            icon_debounce=True;
            self.unpin_icon(self.selected_icon);
            linux.time.sleep(.1);
            icon_debounce=False;
        ##endif
    ##end
    def on_pin(self,event):
        global icon_debounce;
        if not icon_debounce:
            icon_debounce=True;
            self.pin_icon(self.selected_icon);
            linux.time.sleep(.1);
            icon_debounce=False;
        ##endif
    ##end
    def get_icon_by_id(self,id):
        for i in range(len(self.icons)):
            if (self.icons[i]['id']==id):
                return self.icons[i];
            ##endif
        ##end
        return None;
    ##end
    def get_icon_by_name(self,name):
        for i in range(len(self.icons)):
            if (self.icons[i]['name']==name):
                return self.icons[i];
            ##endif
        ##end
        return None;
    ##end
    def get_icon_by_appid(self,appid):
        for i in range(len(self.icons)):
            if (self.icons[i]['app_id']==appid):
                return self.icons[i];
            ##endif
        ##end
        return None;
    ##end
    def get_icon_by_exec(self,exec):
        for i in range(len(self.icons)):
            if (self.icons[i]['exec']==exec):
                return self.icons[i];
            ##endif
        ##end
        return None;
    ##end
    def open_icon_rclick_menu(self,event):
        if not self.themenu:
            self.themenu=ui.Menu(self.master,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
        ##endif
        self.themenu.delete(0,ui.END);
        if self.selected_icon:
            selected=self.get_icon_by_id(self.selected_icon);
            if selected['pinned']:
                self.themenu.add_command(label='Unpin',command=bindFn(self.on_unpin,event));
            else:
                self.themenu.add_command(label='Pin',command=bindFn(self.on_pin,event));
            ##endif
            self.themenu.tk_popup(event.x_root,event.y_root);
            self.themenu.focus_force();
        ##endif
    ##end
    def open_rclick_menu(self,event):
        if not self.themenu:
            self.themenu=ui.Menu(self.master,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
        ##endif
        self.themenu.delete(0,ui.END);
        if self.selected_icon:
            selected=self.get_icon_by_id(self.selected_icon);
            if selected['pinned']:
                self.themenu.add_command(label='Unpin',command=bindFn(self.on_unpin,event));
            else:
                self.themenu.add_command(label='Pin',command=bindFn(self.on_pin,event));
            ##endif
            self.themenu.tk_popup(event.x_root,event.y_root);
            self.themenu.focus_force();
        ##endif
    ##end
    def open_app(self,cmd):
        global h,i;
        i=self.get_icon_by_exec(cmd);
        h=None;
        if i:
            h=i['opened'];
        ##endif
        if cmd!=None and callable(cmd) and not h:
            if i:
                oldindex=self.icons.index(i);
                self.icons.remove(i);
                i['opened']=True;
                self.icons.insert(oldindex,i);
                self.update_icons();
            ##endif
            process_thread=linux.task.Thread(target=cmd);
            process_thread.start();
            while process_thread.is_alive():
                self.update_icons();
                self.update();
                if not desktop_force_show:
                    mainwin.attributes('-topmost',0);
                ##endif
            ##end
            i=self.get_icon_by_exec(cmd);
            if i:
                oldindex=self.icons.index(i);
                self.icons.remove(i);
                i['opened']=False;
                self.icons.insert(oldindex,i);
                if not i['pinned']:
                    self.remove_icon(i['id']);
                ##endif
                self.update_icons();
                self.update();
                desktop_stacking_order_override(mainwin);
            ##endif
        elif cmd!=None:
            if i:
                oldindex=self.icons.index(i);
                self.icons.remove(i);
                i['opened']=True;
                self.icons.insert(oldindex,i);
                self.update_icons();
                desktop_stacking_order_override(mainwin);
            ##endif
            print("Command is a shell command, running via libMain");
            process_thread=linux.task.Thread(target=lib_main.run_application,args=(cmd,));
            process_thread.start();
            if i:
                oldindex=self.icons.index(i);
                self.icons.remove(i);
                i['pid']=linux.get_pid_by_name(cmd);
                self.icons.insert(oldindex,i);
                self.update_icons();
            ##endif
            while process_thread.is_alive():
                self.update_icons();
                self.update();
                desktop_stacking_order_override(mainwin);
            ##end
            i=self.get_icon_by_exec(cmd);
            if i:
                oldindex=self.icons.index(i);
                self.icons.remove(i);
                i['opened']=False;
                i['pid']=None;
                self.icons.insert(oldindex,i);
                if not i['pinned']:
                    self.remove_icon(i['id']);
                ##endif
                self.update_icons();
                self.update();
                desktop_stacking_order_override(mainwin);
            ##endif
        ##endif
    ##end
    def pin_icon(self,id=0):
        pinned_path="~/.local/share/applications/dock";
        theicon=self.get_icon_by_id(id);
        if theicon:
            oldindex=self.icons.index(theicon);
            self.icons.remove(theicon);
            theicon['pinned']=True;
            self.icons.insert(oldindex,theicon);
            self.update_icons();
            if not linux.os.path.exists(pinned_path):
                linux.os.makedirs(pinned_path);
            ##endif
            pinned_file=linux.os.path.join(pinned_path,str(id)+'.desktop' if id!=0 else 'default.desktop');
            thedata={
                'name':theicon['name'],
                'exec':theicon['exec'],
                'icon':theicon['icon_path'],
                'appid':theicon['appid'],
                'type':'pinned_icon',
            };
            linux.create_desktop_file(thedata,pinned_file);
        ##endif
    ##end
    def unpin_icon(self,id=0):
        pinned_path="~/.local/share/applications/dock";
        theicon=self.get_icon_by_id(id);
        if theicon:
            oldindex=self.icons.index(theicon);
            self.icons.remove(theicon);
            theicon['pinned']=False;
            self.icons.insert(oldindex,theicon);
            self.update_icons();
            if not theicon['opened']:
                self.remove_icon(id);
            ##endif
            if not linux.os.path.exists(pinned_path):
                linux.os.makedirs(pinned_path);
            ##endif
            pinned_file=linux.os.path.join(pinned_path,str(id)+'.desktop' if id!=0 else 'default.desktop');
            linux.os.remove(pinned_file);
        ##endif
    ##end
    def retrieve_pinned(self):
        pinned_path="~/.local/share/applications/dock";
        if linux.os.path.exists(pinned_path):
            for i in linux.os.listdir(pinned_path):
                if i.endswith('.desktop'):
                    thedata=linux.parse_desktop_file(linux.os.path.join(pinned_path,i));
                    if thedata:
                        try:
                            self.add_icon(thedata['icon'],thedata['name'],thedata['appid'],thedata['exec'],True);
                        except Exception as e:
                            print('error while parsing dock file: '+str(e));
                        ##endtry
                            
                    ##endif
                ##endif
            ##end
        ##endif
    ##end
    def remove_icon(self,id):
        the_desc=self.get_icon_by_id(id);
        if the_desc:
            self.icons.remove(the_desc);
            self.canvas.delete(the_desc['bg_widget']);
            self.canvas.delete(the_desc['img']);
            #self.linked_desktop.delete(the_desc['name_widget']);
            the_desc['name_widget'].destroy();
            self.update_icons();
        ##endif
    ##end
    def update_icons(self):
        for i in self.icons:
            if (i['opened']):
                if i['open_bar']:
                    self.canvas.delete(i['open_bar']);
                    i['open_bar']=None;
                ##endif
                i['open_bar']=self.canvas.create_rectangle(i['x']+2,i['y']+i['h']+2,i['x']+i['w']-2,i['y']+i['h']+2,fill="#fff",outline="#fff");
            ##endif
        ##end
    ##end
##end
class Dash_Menu(ui.Canvas):
    def __init__(self,master,dock=None,width=500,height=500,*args,**kwargs):
        global thisdir;
        ui.Canvas.__init__(self,master,width=width,height=height,*args,**kwargs);
        self.update();
        self.update_idletasks();
        self.icons=[];
        self.icon_imgs=[];
        self.icon_padding=8;
        self.tile_padding=16;
        self.icon_size=96;
        self.callerDock=dock;
        self.root=master;
        self.__HEIGHT__=height;
        self.__WIDTH__=width;
        self.thestyle=ui.Style(self);
        self.thestyle.theme_use('clam');
        self.thestyle.configure('TEntry',background='#333',foreground='#fff',fieldbackground='#333',border="#fff",insertbackground="#fff");
        self.search_icon=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/search.png');
        self.search_entry=ui.CEntry(self,font=("Ubuntu",12));
        self.search_entry.place(height=48,relwidth=1,anchor=ui.NW);
        self.columns=5;
        preinstalled_path=thisdir+"/programs";
        self.add_icon("Files",thisdir+"/programs/Files/favicon.png",open_files);
        self.add_icon("Terminal",thisdir+"/programs/Terminal/fi_48x48.png",bindFn(lib_main.open_terminal));
        self.add_icon("Textide",thisdir+"/programs/Textide/fi_48x48.png",bindFn(open_textide));
        linux.populate_dash(bindFn(self.add_icon));
        #self.add_icon('Firefox','/nix/store/gsbl1123dy7dil3vayj0w9irn0f2d4rf-firefox-124.0.2/share/icons/hicolor/48x48/apps/firefox.png','firefox');
    ##end
    def add_icon(self,app_name,icon_path,application=None):
        icon_image=ui.PhotoImage(file=icon_path);
        id=len(self.icons);
        self.update();
        # Calculate row and column
        centerx=self.__WIDTH__//2;
        row=id//self.columns;
        column=id%self.columns;
        #number_center = (self.icon_padding + (self.columns - column) * self.icon_size) + self.icon_size // 2
        # Calculate the difference between the center of the number and centerx
        #difference = centerx - number_center
        # Adjust the position of the base
        #base = self.icon_padding + (self.columns - column) * self.icon_size + difference
        #x1 = base
        base=self.icon_padding+(self.columns-column)*self.icon_size;
        x1=base;
        y1=48+self.icon_padding+row*self.icon_size;
        x2=x1+self.icon_size;
        y2=y1+self.icon_size;
        background=self.create_rectangle(x1,y1,x2,y2,fill="#333",outline="#333");
        # Create an image widget with the icon
        icon_widget=self.create_image(x1+self.icon_size//2,y1+self.icon_size//2,image=icon_image,anchor=ui.CENTER);
        
        # Create a text label for the icon name
        name_widget=self.create_text(x1+self.icon_size//2,y1+self.icon_size-15,text=app_name,anchor=ui.N,fill="#fff",font=("Ubuntu",9));
    
        # Store the icon image (you can keep track of icons if needed)
        global icon_debounce;
        icon_debounce=False;
        def on_hover(event):
            self.itemconfig(background,fill="#444",outline="#444");
            self.config(cursor="hand2");
        ##end
        def on_leave(event):
            self.itemconfig(background,fill="#333",outline="#333");
            self.config(cursor="");
        ##end
        def on_click(event):
            global icon_debounce;
            if not icon_debounce:
                icon_debounce=True;
                self.itemconfig(background,fill="#555",outline="#555");
                linux.time.sleep(.1);
                self.open_app(application,icon_path,appid=id,app_name=app_name);
                icon_debounce=False;
            ##endif
        ##end
        self.tag_bind(background,'<Button-1>',on_click);
        self.tag_bind(icon_widget,'<Button-1>',on_click);
        self.tag_bind(name_widget,'<Button-1>',on_click);
        self.tag_bind(background,'<Enter>',on_hover);
        self.tag_bind(icon_widget,'<Enter>',on_hover);
        self.tag_bind(name_widget,'<Enter>',on_hover);
        self.tag_bind(background,'<Leave>',on_leave);
        self.tag_bind(icon_widget,'<Leave>',on_leave);
        self.tag_bind(name_widget,'<Leave>',on_leave);
        self.icon_imgs.insert(0,icon_image);
        self.icons.insert(0,
            {
                "id":id,
                "icon_widget":icon_widget,
                "icon_image":icon_image,
                "app_name":app_name,
                "name_widget":name_widget,
                "row":row,
                "column":column,
                "icon_path":icon_path,
                "application":application if not callable(application) else "run_function:Fn()",
                # the command that the icon runs when clicked
            }
        );
    ##end
    def open_app(self,cmd,icon="",appid=0,app_name=""):
        global dash_shown;
        if self.callerDock is not None:
            close_dash(self.callerDock,self.master);
            dash_shown=False;
            self.callerDock.add_icon(icon,name=app_name,appid=appid,exec=cmd,isPinned=False);
            self.callerDock.open_app(cmd);
        ##endif
        """
        if cmd!=None and callable(cmd):
            process_thread=linux.task.Thread(target=cmd);
            process_thread.start();
        else:
            print("Command is a shell command, running via libMain");
            process_thread=linux.task.Thread(target=lib_main.run_application,args=(cmd,));
            process_thread.start();
        ##endif
        """
    ##end
##end
def open_dash(dock,desktop):
    global mainwin,config,dash_active,dash_canvas,dash_objects,opendb,desktop_force_show;
    desktop.update();
    canvasheight=desktop.winfo_height();
    canvaswidth=desktop.winfo_width();
    print(canvasheight,canvaswidth);
    #Dash ui
    if (not dash_active and not opendb):
        dash_active=True;
        opendb=True;
        if (not dash_canvas):
            dash_canvas=Dash_Menu(desktop,dock,bg='#333',width=canvaswidth-96,height=canvasheight-48);
        ##endif
        for i in range((canvasheight-48)//5):
            dash_canvas.place(relx=.5,y=i*5,anchor=ui.S);
            dash_canvas.update();
            desktop.update();
            mainwin.update();
            if not (desktop_force_show):
                mainwin.attributes('-topmost',0);
            ##endif
        ##end
        opendb=False;
        dash_canvas.place(relx=.5,y=canvasheight-48,anchor=ui.S);
    ###endif
##end
def close_dash(dock,desktop):
    global mainwin,config,dash_active,dash_canvas,dash_objects,opendb,desktop_force_show;
    desktop.update();
    canvasheight=desktop.winfo_height();
    canvaswidth=desktop.winfo_width();
    #Dash ui
    if (dash_active and not opendb):
        dash_active=False;
        opendb=True;
        if (dash_canvas):
            for i in range((canvasheight-48)//5):
                dash_canvas.place(relx=.5,y=(canvasheight-48)-(i*5),anchor=ui.S);
                dash_canvas.update();
                if not (desktop_force_show):
                    mainwin.attributes('-topmost',0);
                ##endif
            ##end
            dash_canvas.place_forget();
        ##endif
        opendb=False;
    ##endif
##end
def dock_handler(dock,desktop):
    global mainwin,config,icons,desktop_force_show,dock_shown;
    dock.e=test=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/test_icon.png');
    dock.e2=dash_icon=com.ImageTk.PhotoImage(file=thisdir+'/assets/images/dash.png');
    dash_btn=dock.canvas.create_image(0,0,image=dash_icon,anchor=ui.NW);
    desktop.update();
    dockheight=48;
    canvasheight=desktop.winfo_height();
    canvaswidth=desktop.winfo_width();
    global dash_shown;
    dash_shown=False;
    def toggle_dock_internal(shown=None,event=None):
        global dock_shown,opendb2,desktop_force_show;
        if not opendb2 and shown==None:
            opendb2=True;
            if (dock_shown):
                dock_shown=False;
                for i in range(dockheight):
                    dock.place(x=48,y=canvasheight-(dockheight-i),anchor=ui.NW);
                    mainwin.update();
                    dock.update();
                    if not (desktop_force_show):
                        mainwin.attributes('-topmost',0);
                    ##endif
                ##end
                dock.place_forget();
                opendb2=False;
            else:
                dock_shown=True;
                for i in range(dockheight):
                    dock.geometry(f"{canvaswidth-96}x{dockheight}+48+{canvasheight-i}");
                    mainwin.update();
                    dock.update();
                    if not (desktop_force_show):
                        mainwin.attributes('-topmost',0);
                    ##endif
                ##end
                opendb2=False;
            ##endif
        elif shown!=None:
            opendb2=True;
            if (not shown):
                dock_shown=False;
                for i in range(dockheight):
                    dock.geometry(f"{canvaswidth-96}x{dockheight}+48+{canvasheight-(dockheight-i)}");
                    mainwin.update();
                    dock.update();
                    if not (desktop_force_show):
                        mainwin.attributes('-topmost',0);
                    ##endif
                ##end
                dock.place_forget();
                opendb2=False;
            else:
                dock_shown=True;
                for i in range(dockheight):
                    dock.geometry(f"{canvaswidth-96}x{dockheight}+48+{canvasheight-i}");
                    mainwin.update();
                    dock.update();
                    if not (desktop_force_show):
                        mainwin.attributes('-topmost',0);
                    ##endif
                ##end
                opendb2=False;
            ##endif
        ##endif
    ##end
    def dash_btn_hover(event):
        dock.canvas.itemconfig(dash_btn,image=dash_icon);  
        dock.config(cursor="hand2");
        dock.update();
    ##end
    def dash_btn_hover_leave(event):
        dock.canvas.itemconfig(dash_btn,image=dash_icon);
        dock.config(cursor="");
        dock.update();
    ##end
    def dash_btn_click(is_superkey,event):
        global dash_shown;
        if (dash_shown):
            dash_shown=False;
            if (dock_shown and is_superkey):
                toggle_dock_internal(False,event);
            ##endif
            close_dash(dock,desktop);
        else:
            dash_shown=True;
            if (not dock_shown and is_superkey):
                toggle_dock_internal(True,event);
            ##endif
            open_dash(dock,desktop);
        ##endif
    ##end
    dock.canvas.tag_bind(dash_btn,'<Button-1>',bindFn(dash_btn_click,False));
    dock.canvas.tag_bind(dash_btn,'<Enter>',dash_btn_hover);
    dock.canvas.tag_bind(dash_btn,'<Leave>',dash_btn_hover_leave);
    desktop.bind('<Super_L>',bindFn(dash_btn_click,True));
    desktop.bind('<Super_R>',bindFn(dash_btn_click,True));
    desktop.bind('<XF86Search>',bindFn(dash_btn_click,True));
    dock.update_icons();
##end