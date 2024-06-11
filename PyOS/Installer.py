from . import UI as uiw;
from . import LinuxUtils as linux;
from . import Filesystem as fs;
from . import libCommon as common;
from .MainExe import MaterialSpinner,shutdown;
import shutil as sh;
thisdir=linux.os.path.dirname(linux.os.path.realpath(__file__));
global mainwin,desk_init;
mainwin=None;
desk_init=None;
temp_desk=None;
ui=uiw.UI();
def init(win,desktop_init):
    global mainwin,desk_init;
    mainwin=win;
    desk_init=desktop_init;
##end
def installer_desk():
    global mainwin,desk_init,temp_desk;
    width=mainwin.winfo_screenwidth();
    height=mainwin.winfo_screenheight();
    desktop=ui.Canvas(mainwin,height=height,width=width,bg="#333");
    temp_desk=desktop;
    desktop.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor="center");
    common.create_bg_img(mainwin,desktop,thisdir+"/assets/backgrounds/background.png");
    desktop.bind("<Button-1>",lambda e:mainwin.attributes("-topmost",False));
    desktop.bind("<Button-3>",lambda e:mainwin.attributes("-topmost",False));
    desktop.bind("<Button-2>",lambda e:mainwin.attributes("-topmost",False));
    desktop.bind("<FocusIn>",lambda e:mainwin.attributes("-topmost",False));
##end
def main(argc:int,argv:list[str]):
    if (argc>1):
        if (argv[1]=='--live'):
            #Install from Live Boot
            uiw.print_info('Installing from Live Boot...');
            load_ui();
        ##endif
    ##endif
##end

def load_ui():
    global mainwin,desk_init,temp_desk;
    rootWin=ui.Window(title='PyNux Installer');
    rootWin.setSize(640,480);
    rootWin.focus_force();
    uiw.print_info('Loading UI...');
    installer_desk();
    root=ui.Frame(rootWin,bg='#333');
    root.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    config={};
    config['users']=[];
    var1=ui.IntVar(root,1);
    var2=ui.IntVar(root,0);
    var3=ui.StringVar(root,'/PyOS');
    var4=ui.IntVar(root,1);
    var5=ui.IntVar(root,1);
    var6=ui.IntVar(root,0);
    var7=ui.StringVar(root,'');
    var8=ui.StringVar(root,'');
    var9=ui.IntVar(root,0);
    var10=ui.IntVar(root,0);
    inst_win_p0=ui.Frame(root);
    inst_win_p0.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    inst_win_p1=ui.Frame(root);
    inst_win_p2=ui.Frame(root);
    inst_win_p3=ui.Frame(root);
    inst_win_p0_msg=ui.Label(inst_win_p0,text='Choose an action.',font=('Ubuntu',10));
    inst_win_p0_msg.place(relx=.5,rely=.1,relwidth=1,relheight=.1,anchor=ui.N);
    inst_local_disk=ui.Button(inst_win_p0,text='Install to Local Disk',font=('Ubuntu',10));
    root.disk_icon=disk_icon=uiw.SvgImage(master=root,file=thisdir+'/assets/images/disk.svg');
    inst_local_disk.config(image=disk_icon);
    inst_local_disk.place(relx=.5,rely=.2,relwidth=.5,relheight=.8);
    try_pyos_btn=ui.Button(inst_win_p0,text='Try PyOS',font=('Ubuntu',10));
    try_pyos_btn.place(relx=0,rely=.2,relwidth=.5,relheight=.8);
    root_inst_cb=ui.Checkbutton(inst_win_p1,text='Install to root directory (/PyOS) [Recommended]',font=('Ubuntu',10),variable=var1);
    root_inst_cb.place(relx=.5,rely=.1,relwidth=1,relheight=.2,anchor=ui.N);
    inst_directory_entry=ui.Entry(inst_win_p1,font=('Ubuntu',10),textvariable=var3);
    inst_py_int_cb=ui.Checkbutton(inst_win_p1,text='Install Python Interpreter',font=('Ubuntu',10),variable=var2);
    inst_py_int_cb.place(relx=.5,rely=.3,relwidth=1,relheight=.2,anchor=ui.N);
    auto_detect_cb=ui.Checkbutton(inst_win_p1,text='Auto-Detect Connected Devices',font=('Ubuntu',10),variable=var4);
    auto_detect_cb.place(relx=.5,rely=.5,relwidth=1,relheight=.2,anchor=ui.N);
    run_smartscan_cb=ui.Checkbutton(inst_win_p1,text='Run SmartScan before installing (Recommended)',font=('Ubuntu',10),variable=var5);
    run_smartscan_cb.place(relx=.5,rely=.7,relwidth=1,relheight=.15,anchor=ui.N);
    continue_btn=ui.Button(inst_win_p1,text='Continue',font=('Ubuntu',10));
    continue_btn.place(relx=.5,rely=.85,relwidth=.5,relheight=.15);
    cancel_btn=ui.Button(inst_win_p1,text='Cancel',font=('Ubuntu',10));
    cancel_btn.place(relx=0,rely=.85,relwidth=.5,relheight=.15);
    root_usr_cb=ui.Checkbutton(inst_win_p2,text='Enable root user.',font=('Ubuntu',10));
    root_usr_cb.place(relx=.5,rely=.1,relwidth=1,relheight=.1,anchor=ui.N);
    root_pw_entry=ui.Entry(inst_win_p2,font=('Ubuntu',10),show='*',textvariable=var7);
    root_pw_entry.place(relx=.5,rely=.3,relwidth=.8,relheight=.1,anchor=ui.N);
    root_pw_lbl=ui.Label(inst_win_p2,text='Root password',font=('Ubuntu',10));
    root_pw_lbl.place(relx=.5,rely=.2,relwidth=.8,relheight=.1,anchor=ui.N);
    confirm_pw_entry=ui.Entry(inst_win_p2,font=('Ubuntu',10),show='*',textvariable=var8);
    confirm_pw_entry.place(relx=.5,rely=.5,relwidth=.8,relheight=.1,anchor=ui.N);
    confirm_pw_lbl=ui.Label(inst_win_p2,text='Confirm root password',font=('Ubuntu',10));
    confirm_pw_lbl.place(relx=.5,rely=.4,relwidth=.8,relheight=.1,anchor=ui.N);
    debug_en_cb=ui.Checkbutton(inst_win_p2,text='Enable debugging features.',font=('Ubuntu',10),variable=var10);
    debug_en_cb.place(relx=.5,rely=.6,relwidth=1,relheight=.1,anchor=ui.N);
    auto_conn_on_boot_cb=ui.Checkbutton(inst_win_p2,text='Enable auto-connect on boot.',font=('Ubuntu',10),variable=var9);
    auto_conn_on_boot_cb.place(relx=.5,rely=.7,relwidth=1,relheight=.1,anchor=ui.N);
    inst_btn=ui.Button(inst_win_p2,text='Install',font=('Ubuntu',10));
    inst_btn.place(relx=.5,rely=.8,relwidth=.5,relheight=.2);
    cancel_btn2=ui.Button(inst_win_p2,text='Cancel',font=('Ubuntu',10));
    cancel_btn2.place(relx=0,rely=.8,relwidth=.5,relheight=.2);
    no_match_err=ui.Label(inst_win_p3,text='Passwords do not match.',font=('Ubuntu',10),fg='#f00');
    no_pw_err=ui.Label(inst_win_p3,text='Please provide a password.',font=('Ubuntu',10),fg='#f00');
    def on_local_inst():
        inst_win_p0.place_forget();
        inst_win_p1.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
        mainwin.update();
        root.update();
        inst_win_p1.update();
    ##end
    def on_try_pyos():
        global desk_init,temp_desk;
        default_config={"users":[{"username":"dH50fIA=","password":"BwcHBwc=","root":False,"prof_pic":["PyOS/assets/images/default_person.svg",True], "desktop":["PyOS/assets/backgrounds/background.png",False],"privs": {"debug": False}}],"system_path": "/PyOS","install_python_interpreter":True,"python_path":"/usr/bin/python3","auto_detect_devices":True,"run_smartscan_install":False,"root_user_enabled":False,"auto_connect_enabled":True,"root_password":"BwcHBwc=","debug_enabled":True,"setup_has_ran":True};
        pynux_user=default_config['users'][0];
        from . import MainExe as mainexe;
        mainexe.c_auth_user=pynux_user;
        rootWin.destroy();
        temp_desk.destroy();
        desk_init.init(mainwin,default_config,pynux_user);
        desk_init.startSessionAfterInit(IsLive=False);
    ##end
    def root_dir_cb_cmd():
        if (var1.get()==1):
            var3.set('/PyOS');
            inst_directory_entry.place_forget();
            inst_py_int_cb.place(relx=.5,rely=.3,relwidth=1,relheight=.2,anchor=ui.N);
            auto_detect_cb.place(relx=.5,rely=.5,relwidth=1,relheight=.2,anchor=ui.N);
            run_smartscan_cb.place(relx=.5,rely=.7,relwidth=1,relheight=.1,anchor=ui.N);
            mainwin.update();
            root.update();
        else:
            inst_directory_entry.place(relx=.5,rely=.25,relwidth=1,relheight=.1,anchor=ui.N);
            inst_py_int_cb.place(relx=.5,rely=.35,relwidth=1,relheight=.2,anchor=ui.N);
            auto_detect_cb.place(relx=.5,rely=.55,relwidth=1,relheight=.2,anchor=ui.N);
            run_smartscan_cb.place(relx=.5,rely=.75,relwidth=1,relheight=.1,anchor=ui.N);
            mainwin.update();
            rootWin.update();
            root.update();
        ##endif
    ##end
    def on_continue():
        if (var1.get()==1):
            config['system_path']='/PyOS';
        else:
            config['system_path']=var3.get();
        ##endif
        if (var2.get()==1):
            config['install_python_interpreter']=True;
            config['python_path']='/usr/bin/python3';
        else:
            config['install_python_interpreter']=False;
        ##endif
        if (var4.get()==1):
            config['auto_detect_devices']=True;
        else:
            config['auto_detect_devices']=False;
        ##endif
        if (var5.get()==1):
            config['run_smartscan_install']=True;
        else:
            config['run_smartscan_install']=False;
        ##endif
        inst_win_p1.place_forget();
        inst_win_p2.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
        mainwin.update();
        rootWin.update();
        root.update();
    ##end
    def handle_finish_config():
        global mainwin,desk_init,temp_desk;
        if (var6.get()==1):
            config['root_user_enabled']=True;
        else:
            config['root_user_enabled']=False;
        ##endif
        if (var9.get()==1):
            config['auto_connect_enabled']=True;
        else:
            config['auto_connect_enabled']=False;
        ##endif
        if (var7.get()!='' and var8.get()!=''):
            if (var7.get()==var8.get()):
                config['root_password']=obfescate(var7.get());
            else:
                cancel_btn2.place_forget();
                inst_btn.place_forget();
                no_pw_err.place(relx=.5,rely=.8,relwidth=1,relheight=.2,anchor=ui.N);
                mainwin.update();
                rootWin.update();
                root.update();
                linux.time.sleep(1);
                no_pw_err.place_forget();
                inst_btn.place(relx=.5,rely=.8,relwidth=.5,relheight=.2);
                cancel_btn2.place(relx=0,rely=.8,relwidth=.5,relheight=.2);
                mainwin.update();
                root.update();
                return;
            ##endif
        else:
            no_match_err.place(relx=.5,rely=.8,relwidth=1,relheight=.2,anchor=ui.N);
            mainwin.update();
            rootWin.update();
            root.update();
            linux.time.sleep(1);
            no_match_err.place_forget();
            inst_btn.place(relx=.5,rely=.8,relwidth=.5,relheight=.2);
            cancel_btn2.place(relx=0,rely=.8,relwidth=.5,relheight=.2);
            mainwin.update();
            rootWin.update();
            root.update();
            return;
        ##end
        if (var10.get()==1):
            config['debug_enabled']=True;
        else:
            config['debug_enabled']=False;
        ##endif
        inst_win_p2.place_forget();
        root.place_forget();
        rootWin.destroy();
        temp_desk.destroy();
        install(config);
    ##end
    def on_cancel():
        shutdown(config);
    ##end
    inst_local_disk.setCommand(common.bindFn(on_local_inst));
    try_pyos_btn.setCommand(common.bindFn(on_try_pyos));
    root_inst_cb.config(command=common.bindFn(root_dir_cb_cmd));
    continue_btn.setCommand(common.bindFn(on_continue));
    inst_btn.setCommand(common.bindFn(handle_finish_config));
    cancel_btn.setCommand(common.bindFn(on_cancel));
    cancel_btn2.setCommand(common.bindFn(on_cancel));
    mainwin.update();
    root.update();
    rootWin.update();
    uiw.print_info('UI Loaded.');
    mainwin.mainloop();
    rootWin.mainloop();
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
def install(config):
    global mainwin,finished;
    finished=False;
    linux.time.sleep(.5);
    mainwin.config(bg="#aaa");
    uiw.print_info('Installing...');
    InstallMessage=ui.Label(mainwin,text='...',font=('Ubuntu',15),fg="#fff",bg="#aaa",height=1);
    InstallMessage.pack(expand=1,fill=ui.X,anchor='s');
    BootSpinner=MaterialSpinner(mainwin,canvas_size=96,animation_length=5.2,arc_width=6,arc_color=("#fff","#fff"),bg_color="#aaa");
    BootSpinner.place(relx=.5,rely=.9,anchor=ui.S);
    mainwin.update();
    mainwin.bootIcon=icon=ui.PhotoImage(file=thisdir+'/assets/BootLogo.png');
    InstallImage=ui.Label(mainwin,text='',font=('Ubuntu',15),fg='#fff',bg='#aaa',image=icon,width='128px',height='128px');
    InstallImage.place(relx=.5,rely=.5,anchor=ui.CENTER);
    def tween():
        start_c=(170,170,170);
        end_c=(51,51,51);
        for i in range(1,30):
            linux.time.sleep(.001);
            t=i/(30);  # Normalize t to [0, 1]
            r,g,b=common.interpolate_color(start_c,end_c,t);
            hxd=common.rgbtohex(r,g,b);
            mainwin.config(bg=hxd);
            InstallImage.config(bg=hxd);
            InstallMessage.config(bg=hxd);
            BootSpinner.config(bg=hxd,highlightbackground=hxd);
            mainwin.update();
        ##end
    ##end
    t1=linux.task.Thread(target=tween);
    t1.start();
    #Begin the install process
    global msgOverride,msgText;
    msgOverride=False;
    msgText='Installing';
    linux.time.sleep(1);
    def install_py_int(install_path):
        global mainwin,msgOverride;
        #set up python
        def cmds():
            global msgOverride,msgText;
            linux.sys_run(f'cd {install_path} && mkdir -p bin');
        ##end
        msgOverride=True;
        count=0;
        start_time=linux.time.time();
        update_time=start_time;
        total_updates=1;  # Keep track of the number of .35-second updates
        while total_updates < 230:  # Run for 30 updates
            current_time=linux.time.time();
            # Update the main every 50 milliseconds
            if (current_time - update_time) >= 0.05:
                mainwin.update()
                update_time=current_time;
            ##endif
            if (current_time - start_time) >= 0.3:
                hxd=linux.math.floor((total_updates/200)*100);
                count+=1;
                if (count>3):
                    count=1;
                ##endif
                if (hxd>100):
                    hxd=100;
                ##endif
                ct='.'*count;
                InstallMessage.setText(f'Installing Python Interpreter{ct} {hxd}%');
                mainwin.update();
                start_time=current_time;
                total_updates+=1;
            ##endif
            # Add a small delay to avoid busy-waiting
            linux.time.sleep(0.01);
        ##end
        msgOverride=False;
    ##end
    def install_root_setup():
        global mainwin,msgOverride,msgText;
        custom_hostname="pynux";
        try:
            with open('/etc/hostname','w') as f:
                f.write(custom_hostname);
                f.close();
            ##endwith
        except Exception as e:
            print('Error Creating hostname: '+str(e)+" No changes have been made to /etc/hostname.");
        ##endtry
        msgOverride=True;
        #This is essentially an update menu, automatically updates root env.
        #first step of install
        updAvailable=True;
        #gets around command race conditions
        count=0;
        def cmdFunc():
            linux.sys_run('mkdir -p /PyOS/.lib/bin');
            linux.sys_run('mkdir -p /PyOS/.lib/bin/.boot');
            linux.sys_run('mkdir -p /PyOS/.lib/.os');
            linux.sys_run('mkdir -p /PyOS/.lib/.os/boot');
            linux.sys_run('mkdir -p /PyOS/.lib/.os/boot/.cache');
        ##end
        cmdThread=linux.task.Thread(target=cmdFunc);
        cmdThread.start();
        start_time=linux.time.time();
        update_time=start_time;
        total_updates=1;  # Keep track of the number of .35-second updates
        while total_updates < 330:  # Run for 30 updates
            current_time=linux.time.time();
            # Update the main every 50 milliseconds
            if (current_time - update_time) >= 0.05:
                mainwin.update()
                update_time=current_time;
            ##endif
            if (current_time - start_time) >= 0.3:
                hxd=linux.math.floor((total_updates/300)*100);
                count+=1;
                if (count>3):
                    count=1;
                ##endif
                if (hxd>100):
                    hxd=100;
                ##endif
                ct='.'*count;
                InstallMessage.setText(f'Setting up root environment{ct} {hxd}%');
                mainwin.update();
                start_time=current_time;
                total_updates+=1;
            ##endif
            # Add a small delay to avoid busy-waiting
            linux.time.sleep(0.01);
        ##end
        if (updAvailable):
            #update the environment.
            #linux.run_command('apt upgrade');
            count=0;
            start_time=linux.time.time();
            update_time=start_time;
            total_updates=1;  # Keep track of the number of .35-second updates
            while total_updates < 630:  # Run for 630 updates
                current_time=linux.time.time();
                # Update the main every 50 milliseconds
                if (current_time - update_time) >= 0.05:
                    mainwin.update()
                    update_time=current_time;
                ##endif
                if (current_time - start_time) >= 0.3:
                    hxd=linux.math.floor((total_updates/600)*100);
                    count+=1
                    if(count>3):
                        count=1;
                    ##endif
                    if (hxd>100):
                        hxd=100;
                    ##endif
                    ct='.'*count;
                    InstallMessage.setText(f'Updating root environment{ct} {hxd}%');
                    mainwin.update();
                    start_time=current_time;
                    total_updates+=1;
                ##endif
                # Add a small delay to avoid busy-waiting
                linux.time.sleep(0.01);
            ##end
        ##endif
        msgOverride=False;
    ##end
    def install_main_settings():
        global main;
        count=0;
        start_time=linux.time.time();
        update_time=start_time;
        total_updates=1;  # Keep track of the number of .35-second updates
        while total_updates < 310:  # Run for 30 updates
            current_time=linux.time.time();
            # Update the main every 50 milliseconds
            if (current_time - update_time) >= 0.05:
                mainwin.update()
                update_time=current_time;
            ##endif
            if (current_time - start_time) >= 0.3:
                hxd=linux.math.floor((total_updates/300)*100);
                count+=1
                if(count>3):
                    count=1;
                ##endif
                if (hxd>100):
                    hxd=100;
                ##endif
                ct='.'*count;
                InstallMessage.setText(f'Configuring root environment{ct} {hxd}%');
                mainwin.update();
                start_time=current_time;
                total_updates+=1;
            ##endif
            # Add a small delay to avoid busy-waiting
            linux.time.sleep(0.01);
        ##end
        linux.write_cfg(thisdir+'/cfg/main.pycfg',config);
    ##end
    install_root_setup();
    if (config['install_python_interpreter']==True):
        #Probably the fastest part of the install.
        install_py_int(config['python_path']);
    ##endif
    if (config['auto_detect_devices']==True):
        pass;
    ##endif
    #installs main settings last as everything else has to finish beforehand.
    install_main_settings();
    #Run smartscan if enabled to verify install.
    if (config['run_smartscan_install']==True):
        def onprogress(percent):
            if percent>100:
                percent=100;
            elif percent<0:
                percent=0;
            ##endif
            InstallMessage.setText(f'Scanning files...{str(percent)}%');
            mainwin.update();
        ##end
        def oncount(count):
            InstallMessage.setText(f'Smartscan Starting... Items found {count}');
            #mainwin.update();
        ##end
        success=fs.disk_scan(onprogress,oncount);
        if (not success):
            InstallMessage.setText('Smartscan failed. Install canceled.');
            mainwin.update();
            return;
        elif (success):
            InstallMessage.setText('Smartscan complete. No errors found.');
            mainwin.update();
        ##endif
    ##endif
    count=0;
    for i in range(1,410):
        linux.time.sleep(.3);
        hxd=linux.math.floor((i/400)*100);
        count+=1
        if(count>3):
            count=1;
        ##endif
        if (hxd>100):
            hxd=100;
        ##endif
        ct='.'*count;
        InstallMessage.setText(f'Finalizing Install{ct} {hxd}%');
        mainwin.update();
    ##end
    BootSpinner.stop();
    finished=True;
    InstallMessage.setText('Install Complete, Enjoy PyNux! :)');
    mainwin.update();
    linux.time.sleep(1);
    def tween2():
        start_c=(51,51,51);
        end_c=(0,0,0);
        for i in range(1,20):
            linux.time.sleep(.001);
            t=i/(20)  # Normalize t to [0, 1]
            r,g,b=common.interpolate_color(start_c,end_c,t);
            hxd=common.rgbtohex(r,g,b);
            mainwin.config(bg=hxd);
            InstallImage.config(bg=hxd);
            InstallMessage.config(bg=hxd);
            BootSpinner.config(bg=hxd,highlightbackground=hxd);
            mainwin.update();
        ##end
    ##end
    tween2();
    InstallMessage.destroy();
    InstallImage.destroy();
    BootSpinner.destroy();
    run_stage2(config);
##end
def run_stage2(config):
    global mainwin,finished;
    from . import SetupExe as stage2;
    stage2.init(mainwin,config);
    stage2.main(2,['./SetupExe','--live']);
##end
