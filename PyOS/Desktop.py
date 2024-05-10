from . import UI as uiw;
from . import Filesystem as fs;
from . import LinuxUtils as linux;
from . import Pointer as pt;
from . import libCommon as com;
from . import MainExe as lib_main;
import screeninfo;
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
        #For now also just quits the program, there isnt any shutdown system yet.
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
    com.create_bg_img(mainwin,root,'PyOS/assets/backgrounds/background.png');
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    mainwin.update();
    root.update();
    if (not IsLive):
        root.destroy();
        goto_desktop();
        mainwin.mainloop();
    else:
        #Show the welcome message.
        welcome_to_PyOS(root);
    ##endif
##end

def open_files():
    try:
        from .programs import Files as f;
        f.imported=True;
        f.main(1,[__file__]);
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

def new_desktop(screenname):
    newroot=ui.Window(screenName=screenname);
    newroot.setAttribute('fullscreen',True);
    newroot.update();
    global mainwin,config,desktop_force_show;
    #Create the desktop
    power_menu=ui.Menu(newroot,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    power_menu.add_command(label='Shutdown',command=lambda:lib_main.shutdown(config));
    power_menu.add_command(label='Restart',command=lambda:lib_main.restart(config));
    application_menu=ui.Menu(newroot,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    application_menu.add_command(label="Terminal",command=lib_main.open_terminal);
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
    right_click_menu.add_command(label="Open in files");
    right_click_menu.add_command(label='Open in Terminal',command=bindFn(lib_main.open_terminal));
    right_click_menu.add_cascade(label="Applications",menu=application_menu);
    right_click_menu.add_separator();
    right_click_menu.add_command(label='Change background');
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Display Settings");
    right_click_menu.add_command(label="Desktop Symbol Settings");
    right_click_menu.add_separator();
    right_click_menu.add_cascade(label="Power",menu=power_menu);
    def desktop_clicked(event):
        global desktop_force_show;
        #after that we would usually check whats near the click point and if its a shortcut we open it
        if not (desktop_force_show):
            newroot.attributes('-topmost',0);
        ##endif
    ##end
    def on_desktop_focus(event):
        global desktop_force_show;
        if not (desktop_force_show):
            newroot.attributes('-topmost',0);
        ##endif
    ##end
    def desktop_back_if_not_shown(event):
        newroot.lower();
    ##end
    def dock_btn_hover(event):
        global desktop_force_show;
        desktop.itemconfig(dock_btn,image=dock_hover_img);  
        desktop.config(cursor="hand2");
        desktop.update();
        if not (desktop_force_show):
            newroot.attributes('-topmost',0);
        ##endif
    ##end
    def dock_btn_hover_leave(event):
        global desktop_force_show;
        desktop.itemconfig(dock_btn,image=dock_img);
        desktop.config(cursor="");
        desktop.update();
        if not (desktop_force_show):
            newroot.attributes('-topmost',0);
        ##endif
    ##end
    global debounce,dock_shown,opendb2;
    debounce=False;
    opendb2=False;
    dock_shown=False;
    def toggle_dock():
        global dock_shown,opendb2,desktop_force_show;
        if not opendb2:
            opendb2=True;
            if (dock_shown):
                dock_shown=False;7
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
                    dock.place(x=48,y=canvasheight-i,anchor=ui.NW);
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
    def dock_btn_click(event):
        global debounce;
        if debounce!=True:
            desktop.itemconfig(dock_btn,image=dock_click_img);
            debounce=True;
            toggle=linux.task.Thread(target=toggle_dock);
            toggle.start();
            mainwin.lower();
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
    desktop=ui.Canvas(mainwin,bg='#333');
    desktop.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    desktop.update();
    canvaswidth=desktop.winfo_width();
    canvasheight=desktop.winfo_height();
    dockheight=48;
    desktop.di=dock_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dock.png');
    desktop.dhi=dock_hover_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dock_hover.png');
    desktop.dci=dock_click_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dock_click.png');
    desktop.di2=dash_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dash.png');
    global img;
    img=com.create_bg_img(mainwin,desktop,'PyOS/assets/backgrounds/background.png');
    dock_btn=desktop.create_image(0,canvasheight,image=dock_img,anchor=ui.SW);
    dock=ui.Canvas(desktop,bg='#333',width=canvaswidth-96,height=dockheight);
    dock.place(x=48,rely=1,anchor=ui.NW);
    dock.update();
    desktop.tag_bind(dock_btn,'<Button-1>',dock_btn_click);
    desktop.tag_bind(dock_btn,'<Enter>',dock_btn_hover);
    desktop.tag_bind(dock_btn,'<Leave>',dock_btn_hover_leave);
    desktop.tag_bind(img,"<Button-1>",bindFn(on_desktop_focus));
    desktop.bind('<Button-1>',bindFn(desktop_clicked));
    desktop.bind('<Button-3>',bindFn(rc_menu_fn));
    desktop.bind('<FocusIn>',bindFn(on_desktop_focus));
    mainwin.bind('<FocusIn>',bindFn(on_desktop_focus));
    dock.bind('<FocusIn>',bindFn(on_desktop_focus));
    dock.bind('<Button-1>',bindFn(on_desktop_focus));
    dock_handler(dock,desktop);
##end

def get_tasks():
    global mainwin,config;
    
##end

def get_screens():
    monitors=screeninfo.get_monitors();
    return monitors;
##end

def goto_desktop():
    global mainwin,config,desktop_force_show,active_screens;
    active_screens=[];
    try:
        screens=get_screens();
        if (len(screens)>1):
            for i in range(len(screens)):
                active_screens.append(screens[i].name);
            ##end
        ##endif
    except Exception as err:
        uiw.print_info('Unable to get screens: '+str(err));
    ##endtry
    #Create the desktop
    power_menu=ui.Menu(mainwin,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    power_menu.add_command(label='Shutdown',command=lambda:lib_main.shutdown(config));
    power_menu.add_command(label='Restart',command=lambda:lib_main.restart(config));
    application_menu=ui.Menu(mainwin,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    application_menu.add_command(label="Terminal",command=lib_main.open_terminal);
    application_menu.add_command(label="Files",command=open_files);
    right_click_menu=ui.Menu(mainwin,tearoff=0,cursor="",fg="#fff",bg="#333",font=("Ubuntu",10));
    right_click_menu.add_command(label='Create new');
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Paste");
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Select all");
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Arrange all");
    right_click_menu.add_command(label="Arrange by");
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Open in files");
    right_click_menu.add_command(label='Open in Terminal',command=bindFn(lib_main.open_terminal));
    right_click_menu.add_cascade(label="Applications",menu=application_menu);
    right_click_menu.add_separator();
    right_click_menu.add_command(label='Change background');
    right_click_menu.add_separator();
    right_click_menu.add_command(label="Display Settings");
    right_click_menu.add_command(label="Desktop Symbol Settings");
    right_click_menu.add_separator();
    right_click_menu.add_cascade(label="Power",menu=power_menu);
    def desktop_clicked(event):
        global desktop_force_show;
        #after that we would usually check whats near the click point and if its a shortcut we open it
        if not (desktop_force_show):
            mainwin.attributes('-topmost',0);
        ##endif
    ##end
    def on_desktop_focus(event):
        global desktop_force_show;
        if not (desktop_force_show):
            mainwin.attributes('-topmost',0);
        ##endif
    ##end
    def desktop_back_if_not_shown(event):
        mainwin.lower();
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
                    dock.place(x=48,y=canvasheight-i,anchor=ui.NW);
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
    def dock_btn_click(event):
        global debounce;
        if debounce!=True:
            desktop.itemconfig(dock_btn,image=dock_click_img);
            debounce=True;
            toggle=linux.task.Thread(target=toggle_dock);
            toggle.start();
            mainwin.lower();
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
    desktop=ui.Canvas(mainwin,bg='#333');
    desktop.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    desktop.update();
    canvaswidth=desktop.winfo_width();
    canvasheight=desktop.winfo_height();
    dockheight=48;
    desktop.di=dock_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dock.png');
    desktop.dhi=dock_hover_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dock_hover.png');
    desktop.dci=dock_click_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dock_click.png');
    desktop.di2=dash_img=com.ImageTk.PhotoImage(file='PyOS/assets/images/dash.png');
    global img;
    img=com.create_bg_img(mainwin,desktop,'PyOS/assets/backgrounds/background.png');
    dock_btn=desktop.create_image(0,canvasheight,image=dock_img,anchor=ui.SW);
    dock=ui.Canvas(desktop,bg='#333',width=canvaswidth-96,height=dockheight);
    dock.place(x=48,rely=1,anchor=ui.NW);
    dock.update();
    dash_btn=dock.create_image(0,0,image=dash_img,anchor=ui.NW);
    
    desktop.tag_bind(dock_btn,'<Button-1>',dock_btn_click);
    desktop.tag_bind(dock_btn,'<Enter>',dock_btn_hover);
    desktop.tag_bind(dock_btn,'<Leave>',dock_btn_hover_leave);
    desktop.tag_bind(img,"<Button-1>",bindFn(on_desktop_focus));
    desktop.bind('<Button-1>',bindFn(desktop_clicked));
    desktop.bind('<Button-3>',bindFn(rc_menu_fn));
    desktop.bind('<FocusIn>',bindFn(on_desktop_focus));
    mainwin.bind('<FocusIn>',bindFn(on_desktop_focus));
    dock.bind('<FocusIn>',bindFn(on_desktop_focus));
    dock.bind('<Button-1>',bindFn(on_desktop_focus));
    dock_handler(dock,desktop);
##end
global dash_active,dash_canvas,dash_objects,opendb,thisdir;
thisdir=linux.os.path.dirname(linux.os.path.realpath(__file__));
dash_active=False;
dash_canvas=None;
opendb=False;
class Dash_Menu(ui.Canvas):
    def __init__(self,master,dock=None,*args,**kwargs):
        global thisdir;
        super().__init__(master,*args,**kwargs);
        self.icons=[];
        self.icon_imgs=[];
        self.icon_padding=8;
        self.tile_padding=16;
        self.icon_size=96;
        self.callerDock=dock;
        self.master=master;
        self.mainstyle=ui.Style(self);
        self.mainstyle.theme_use('clam');
        self.mainstyle.configure('TEntry',background='#333',foreground='#fff',fieldbackground='#333',border="#fff",insertbackground="#fff");
        self.search_icon=com.ImageTk.PhotoImage(file='PyOS/assets/images/search.png');
        self.update();
        self.search_entry=ui.CEntry(self,font=("Ubuntu",12));
        self.search_entry.place(height=48,relwidth=1,anchor=ui.NW);
        preinstalled_path="PyOS/programs";
        self.add_icon('Firefox','/nix/store/7cib0r7590ldi5gblwmd43y5jrgq5gqg-firefox-120.0/share/icons/hicolor/48x48/apps/firefox.png','firefox');
        self.add_icon("Terminal",thisdir+"/programs/Terminal/fi_48x48.png",lib_main.open_terminal);
        self.add_icon("Files",thisdir+"/programs/Files/favicon.png",open_files);
    ##end
    def add_icon(self,app_name,icon_path,application=None):
        icon_image=ui.PhotoImage(file=icon_path);
        id=len(self.icons);
        self.update();
        # Calculate row and column
        row=id//8;
        column=id%8;
        x1=self.icon_padding+column*self.icon_size;
        y1=48+self.icon_padding+row*self.icon_size;
        x2=x1+self.icon_size;
        y2=y1+self.icon_size;
        background=self.create_rectangle(x1,y1,x2,y2,fill="#333",outline="#333");
        # Create an image widget with the icon
        icon_widget=self.create_image(self.icon_padding+column*self.icon_size+48,self.icon_padding+48+row*self.icon_size+48,image=icon_image,anchor=ui.CENTER);
    
        # Create a text label for the icon name
        name_widget=self.create_text(self.icon_padding+column*self.icon_size+48,self.icon_padding+32+row*self.icon_size+self.icon_size,text=app_name,anchor=ui.N,fill="#fff",font=("Ubuntu",8));
    
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
                self.open_app(application);
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
        self.icon_imgs.append(icon_image);
        self.icons.append({
            "id":id,
            "icon_widget":icon_widget,
            "icon_image":icon_image,
            "app_name":app_name,
            "name_widget":name_widget,
            "row":row,
            "column":column,
            "icon_path":icon_path,
            "application":application if not callable(application) else "run_function:Fn()", # the command that the icon runs when clicked
        });
    ##end
    def open_app(self,cmd):
        if self.callerDock is not None:
            close_dash(self.callerDock,self.master);
        ##endif
        if cmd!=None and callable(cmd):
            process_thread=linux.task.Thread(target=cmd);
            process_thread.start();
        else:
            print("Command is a shell command, running via libMain");
            process_thread=linux.task.Thread(target=lib_main.run_application,args=(cmd,));
            process_thread.start();
        ##endif
    ##end
##end
def open_dash(dock,desktop):
    global mainwin,config,dash_active,dash_canvas,dash_objects,opendb,desktop_force_show;
    desktop.update();
    canvasheight=desktop.winfo_height();
    canvaswidth=desktop.winfo_width();
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
class Dock(ui.Canvas):
    def __init__(self,master,desktop=None,*args,**kwargs):
        ui.Canvas.__init__(self,master,*args,**kwargs);
        self.master=master;
        self.linked_desktop=desktop;
        self.mainstyle=ui.Style(self);
        self.mainstyle.theme_use('clam');
        self.iconwidth=32;
        self.iconheight=32;
        self.padding=8;
        self.icons=[];
    ##end
    def draw_icon(self,icon,id,appid):
        x=48+self.padding+(id-1)*(self.iconwidth+self.padding);  # Calculate x based on id
        y=self.padding;  # Fixed y position with padding
        icon_img=self.create_image(x,y,image=icon, anchor=ui.NW);
        icons.append({
            'id':id,
            'img':icon_img,
            'x':x,
            'y':y,
            'w':self.iconwidth,
            'h':self.iconheight,
            'icon':icon,
            'app_id':appid,
            'name':None,
            'selected':False,
            'opened':False,
            'open_bar':None,
        });
    ##end
##end
def dock_handler(dock,desktop):
    global mainwin,config,icons,desktop_force_show;
    iconwidth=32;
    iconheight=32;
    padding=8;
    icons=[];
    def draw_icon(icon,id,appid):
        global icons
        x=48+padding+(id-1)*(iconwidth+padding);  # Calculate x based on id
        y=padding;  # Fixed y position with padding
        icon_img=dock.create_image(x,y,image=icon, anchor=ui.NW);
        icons.append({
            'id':id,
            'img':icon_img,
            'x':x,
            'y':y,
            'w':iconwidth,
            'h':iconheight,
            'icon':icon,
            'app_id':appid,
            'name':None,
            'selected':False,
            'opened':False,
            'open_bar':None,
        });
    ##end
    def update_icons():
        for i in icons:
            if (i['opened']):
                if i['open_bar']:
                    dock.delete(i['open_bar']);
                    i['open_bar']=None;
                ##endif
                i['open_bar']=dock.create_rectangle(i['x']+2,i['y']+i['h']+2,i['x']+i['w']-2,i['y']+i['h']+2,fill="#fff",outline="#fff");
            ##endif
        ##end
    ##end
    def draw_pinned_icon(icon):
        global icons;
        id=len(icons)+1;
        draw_icon(icon,id,0);
    ##end
    dock.e=test=com.ImageTk.PhotoImage(file='PyOS/assets/images/test_icon.png');
    for i in range(2):
        draw_pinned_icon(test);
    ##end
    dock.e2=dash_icon=com.ImageTk.PhotoImage(file='PyOS/assets/images/dash.png');
    dash_btn=dock.create_image(0,0,image=dash_icon,anchor=ui.NW);
    global dash_shown;
    dash_shown=False;
    def dash_btn_hover(event):
        dock.itemconfig(dash_btn,image=dash_icon);  
        dock.config(cursor="hand2");
        dock.update();
    ##end
    def dash_btn_hover_leave(event):
        dock.itemconfig(dash_btn,image=dash_icon);
        dock.config(cursor="");
        dock.update();
    ##end
    def dash_btn_click(event):
        global dash_shown;
        if (dash_shown):
            dash_shown=False;
            close_dash(dock,desktop);
        else:
            dash_shown=True;
            open_dash(dock,desktop);
        ##endif
    ##end
    dock.tag_bind(dash_btn,'<Button-1>',bindFn(dash_btn_click));
    dock.tag_bind(dash_btn,'<Enter>',dash_btn_hover);
    dock.tag_bind(dash_btn,'<Leave>',dash_btn_hover_leave);
    update_icons();
##end