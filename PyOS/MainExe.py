from . import UI as uiw;
from . import LinuxUtils as linux;
from . import Filesystem as fs;
from . import libCommon as com;
ui=uiw.UI();
#Live Boot Check
global main,for_install,c_auth_user;
main=0;
c_auth_user=None;
for_install=False;
def init():
    global for_install;
    if (linux.is_live_boot()==True):
        for_install=True
    ##endif
##end
def create_spinner(canvas,extent):
    canvas.create_arc(4, 4, 44, 44, start=0, extent=extent, width=2);
##end
def animate_spinner(canvas,angle=0):
    # Update the spinner angle
    canvas.delete("all");  # Clear the canvas
    extent=(angle%360); # Calculate the extent based on the angle
    create_spinner(canvas,extent);
    angle=(angle+10)%360;
    canvas.after(100,animate_spinner,canvas,angle);
##end
def load():
    global main,for_install,c_auth_user;
    main=ui.Window();
    main.config(bg='#333');
    main.setAttribute('fullscreen',True);
    main.attributes('-topmost',0);
    LoadMsg=ui.Label(main,text='...',font=('Ubuntu',20),fg='#fff',bg='#333',height=1);
    LoadMsg.place(relx=.5,rely=1,relwidth=1,anchor=ui.S);
    main.update(); #fixes the window size values for future use
    main.attributes('-topmost',0);
    main.bootIcon=icon=ui.PhotoImage(file='PyOS/assets/BootLogo.png');
    LoadImg=ui.Label(main,text='',font=('Ubuntu',20),fg='#fff',bg='#333',height='128px',width='128px',image=icon);
    LoadImg.place(relx=.5,rely=.5,anchor=ui.CENTER);
    main.update();
    count=0;
    for i in range(0,30):
        count+=1;
        if (count>3):
            count=0;
        ##endif
        ct='.'*count;
        LoadMsg.setText(f'{ct}Loading{ct}');
        main.update();
        linux.time.sleep(.35);
    ##end
    main.update();
    LoadImg.destroy();
    LoadMsg.destroy();
    if (for_install==True):
        from . import Installer as inst;
        from . import Desktop as desk;
        #If live boot, begin installation.
        uiw.print_info("Live Boot Detected. Running Installer+Live Desktop...");
        #Initialize installer
        inst.init(main,desk);
        #Run the installer
        inst.main(2,['./Installer','--live']);
        #Exit
        uiw.print_info("Live Boot Detected. Exiting...");
        exit();
    else:
        from . import Desktop as desk;
        #If not live boot, begin desktop.
        uiw.print_info("Not Live Boot. Running Desktop...");
        #Initialize desktop
        def desktop_init(main,cfg,logged):
            global c_auth_user;
            desk.init(main,cfg,logged);
            c_auth_user=logged;
            #Run the desktop
            if (cfg['setup_has_ran']==False):
                desk.startSessionAfterInit(IsLive=True);
            else:
                desk.startSessionAfterInit(IsLive=False);
            ##endif
        ##end
        authorize(main,linux.read_cfg('PyOS/cfg/main.pycfg'),com.bindFn(desktop_init));
    ##endif
##end
def open_terminal(path=linux.os.getcwd()):
    global c_auth_user;
    try:
        from .programs import Terminal as term;
        term.main(path,linux.usrndecode(c_auth_user['username']).decode('utf-8'));
    except Exception as err:
        uiw.print_info('Error: '+str(err));
    ##endtry
##end
processes=[];
proc_descs=[];
def run_application(cmd,icon=None):
    global main;
    process=linux.runner.Popen(cmd,shell=False);
    processes.append(process.pid);
    proc_descs.append({
        "pid":process.pid,
        "name":cmd,
        "icon":icon,
    });
    while process.poll()==None:
        linux.time.sleep(.1);
    ##end
    proc_descs.remove(proc_descs[processes.index(process.pid)]);
    processes.remove(process.pid);
    if (process.returncode!=0):
        uiw.print_info('Application exited with code '+str(process.returncode));
    ##endif
##end
def authorize(main,cfg,callback):
    global for_install;
    #Create the user page
    root=ui.Canvas(main,bg='#333');
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    root.update();
    canvasheight=root.winfo_height();
    canvaswidth=root.winfo_width();
    centerX=canvaswidth/2;
    centerY=canvasheight/2;
    com.create_bg_img(main,root,'PyOS/assets/backgrounds/background.png');
    root.update();
    global texts;
    texts=[];
    mainstyle=ui.Style(root);
    mainstyle.theme_use('clam');
    mainstyle.configure('TEntry',background='#333',foreground='#fff',fieldbackground='#333',border="#fff",insertbackground="#fff",highlightbackground='#f80',highlightcolor="#f80");
    if len(cfg['users'])==0:
        uiw.print_info('No users found. Running setup EXE.');
        from . import SetupExe as setup;
        setup.init(main,cfg);
        setup.main(2,['./SetupExe','--live']);
    ##endif
    def draw_usr(i):
        global texts,cur;
        cur=i-1;
        root.delete(*texts);
        texts=[];
        user=cfg['users'][i-1];
        userName=root.create_text(centerX,centerY,text=linux.usrndecode(user['username']).decode('utf-8'),font=('Ubuntu',20),anchor=ui.CENTER,fill='#fff');
        next_btn=root.create_text(canvaswidth,centerY,text='>',font=('Ubuntu',20),anchor=ui.E,fill="#fff");
        prev_btn=root.create_text(0,centerY,text='<',font=('Ubuntu',20),anchor=ui.W,fill="#fff");
        pw_ent=ui.CEntry(root,font=('Ubuntu',25),show="⋅");
        pw_ent.focus();
        pw_ent.place(relx=.5,rely=.6,relwidth=.35 if (root.winfo_width()<640) else .25,relheight=.05,anchor=ui.CENTER);
        pw_ent.update();
        etr_btn=root.create_text(centerX+(pw_ent.winfo_width()/2),canvasheight*.6,text='>',font=('Ubuntu',20),fill="#fff",anchor=ui.W);
        incorrect_err=root.create_text(centerX,canvasheight*.8,text='Incorrect Password',font=('Ubuntu',10),fill="#f00",state="hidden");
        no_pw_err=root.create_text(centerX,canvasheight*.8,text='Please type a password.',font=('Ubuntu',10),fill="#f00",state="hidden");
        texts.append(userName);
        texts.append(next_btn);
        texts.append(prev_btn);
        texts.append(etr_btn);
        texts.append(no_pw_err);
        texts.append(incorrect_err);
        root.update();
        def enter_fn(ev=None):
            global texts,cur;
            root.itemconfigure(no_pw_err,state="hidden");
            root.itemconfigure(incorrect_err,state="hidden");
            linux.time.sleep(.1);
            if (pw_ent.get()==''):
                root.itemconfigure(no_pw_err,state="normal");
                root.update();
                return;
            elif (com.obfescate(pw_ent.get())==user['password']):
                print('Welcome.');
                callback(main,cfg,user);
                root.update();
                root.destroy();
                return;
            else:
                print('Incorrect Password.');
                root.itemconfigure(incorrect_err,state="normal");
                root.update();
                return;
            ##endif
        ##end
        def next_btn_fn(ev):
            print('next');
            if (i<len(cfg['users'])):
                pw_ent.destroy();
                draw_usr(i+1);
                return;
            else:
                print('no more users to show');
                return;
            ##endif
        ##end
        def prev_btn_fn(ev):
            print('prev');
            if (cur>0):
                pw_ent.destroy();
                draw_usr(cur-1);
                return;
            else:
                print('no more users to show');
                return;
            ##endif
        ##end
        root.tag_bind(next_btn,'<Button-1>',com.bindFn(next_btn_fn));
        root.tag_bind(prev_btn,'<Button-1>',com.bindFn(prev_btn_fn));
        root.tag_bind(etr_btn,'<Button-1>',com.bindFn(enter_fn));
        pw_ent.bind('<Return>',com.bindFn(enter_fn));
    ##end
    draw_usr(1);
    main.mainloop();
##end

def restart(config):
    global main,msg,count;
    main.bootIcon=icon=ui.PhotoImage(file='PyOS/assets/BootLogo.png');
    root=ui.Frame(main,bg='#333');
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    img=ui.Label(main,text='',font=('Ubuntu',20),fg='#fff',bg='#333',height='128px',width='128px',image=icon);
    img.place(relx=.5,rely=.5,anchor=ui.CENTER);
    msg=ui.Label(main,text='...',font=('Ubuntu',20),fg='#fff',bg='#333',height=1);
    msg.place(relx=.5,rely=1,relwidth=1,anchor=ui.S);
    count=0;
    def restart_msg():
        global count,main,msg;
        for i in range(0,30):
            count+=1;
            if (count>3):
                count=0;
            ##endif
            ct='.'*count;
            msg.setText(f'Restarting{ct}');
            main.update();
            linux.time.sleep(.35);
        ##end
    ##end
    def restart_fn():
        global main;
        linux.write_cfg('PyOS/cfg/main.pycfg',config);
        linux.restart();
    ##end
    restart_task=linux.task.Thread(target=restart_msg);
    restart_task.start();
    restart_msg();
    #__NOT YET FULLY IMPLEMENTED__
    quit();
##end
def shutdown(config):
    global main,msg,count;
    main.bootIcon=icon=ui.PhotoImage(file='PyOS/assets/BootLogo.png');
    root=ui.Frame(main,bg='#333');
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    img=ui.Label(main,text='',font=('Ubuntu',20),fg='#fff',bg='#333',height='128px',width='128px',image=icon);
    img.place(relx=.5,rely=.5,anchor=ui.CENTER);
    msg=ui.Label(main,text='...',font=('Ubuntu',20),fg='#fff',bg='#333',height=1);
    msg.place(relx=.5,rely=1,relwidth=1,anchor=ui.S);
    count=0;
    def shutdown_msg():
        global count,main,msg;
        for i in range(0,30):
            count+=1;
            if (count>3):
                count=0;
            ##endif
            ct='.'*count;
            msg.setText(f'Shutting Down{ct}');
            main.update();
            linux.time.sleep(.35);
        ##end
    ##end
    def shutdown_fn():
        global main;
        linux.write_cfg('PyOS/cfg/main.pycfg',config);
        linux.shutdown();
    ##end
    shutdown_task=linux.task.Thread(target=shutdown_fn);
    shutdown_task.start();
    shutdown_msg();
    quit();
##end
