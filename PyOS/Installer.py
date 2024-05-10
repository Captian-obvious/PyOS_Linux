from . import UI as uiw;
from . import LinuxUtils as linux;
from . import Filesystem as fs;
from . import libCommon as common;
import shutil as sh;
global mainwin;
mainwin=None;
ui=uiw.UI();

def init(win):
    global mainwin;
    mainwin=win;
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
    global mainwin;
    uiw.print_info('Loading UI...');
    root=ui.Frame(mainwin,bg='#333');
    root.place(relx=.5,rely=.5,relwidth=.8,relheight=.8,anchor=ui.CENTER);
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
    inst_win_p0_title=ui.Label(inst_win_p0,text='PyOS Installer',font=('Ubuntu',10));
    inst_win_p0_title.place(relx=.5,relwidth=1,relheight=.1,anchor=ui.N);
    inst_win_p1=ui.Frame(root);
    inst_win_p1_title=ui.Label(inst_win_p1,text='PyOS Installer',font=('Ubuntu',10));
    inst_win_p1_title.place(relx=.5,relwidth=1,relheight=.1,anchor=ui.N);
    inst_win_p2=ui.Frame(root);
    inst_win_p2_title=ui.Label(inst_win_p2,text='PyOS Installer',font=('Ubuntu',10));
    inst_win_p2_title.place(relx=.5,relwidth=1,relheight=.1,anchor=ui.N);
    inst_win_p3=ui.Frame(root);
    inst_win_p3_title=ui.Label(inst_win_p3,text='PyOS Installer',font=('Ubuntu',10));
    inst_win_p3_title.place(relx=.5,relwidth=1,relheight=.1,anchor=ui.N);
    inst_win_p0_msg=ui.Label(inst_win_p0,text='Choose an action.',font=('Ubuntu',10));
    inst_win_p0_msg.place(relx=.5,rely=.1,relwidth=1,relheight=.1,anchor=ui.N);
    inst_local_disk=ui.Button(inst_win_p0,text='Install to Local Disk',font=('Ubuntu',10));
    root.disk_icon=disk_icon=uiw.SvgImage(file='PyOS/assets/images/disk.svg');
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
        pass;
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
        root.update();
    ##end
    def handle_finish_config():
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
            root.update();
            linux.time.sleep(1);
            no_match_err.place_forget();
            inst_btn.place(relx=.5,rely=.8,relwidth=.5,relheight=.2);
            cancel_btn2.place(relx=0,rely=.8,relwidth=.5,relheight=.2);
            mainwin.update();
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
        install(config);
    ##end
    def on_cancel():
        quit();
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
    mainwin.mainloop();
    uiw.print_info('UI Loaded.');
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
    mainwin.update();
    mainwin.bootIcon=icon=ui.PhotoImage(file='PyOS/assets/BootLogo.png');
    InstallImage=ui.Label(mainwin,text='',font=('Ubuntu',15),fg='#fff',bg='#aaa',image=icon,width='128px',height='128px');
    InstallImage.place(relx=.5,rely=.5,anchor=ui.CENTER);
    def tween():
        start_c=(170,170,170);
        end_c=(51,51,51);
        for i in range(1,30):
            linux.time.sleep(.001);
            t=i/(30)  # Normalize t to [0, 1]
            r,g,b=common.interpolate_color(start_c,end_c,t);
            hxd=common.rgbtohex(r,g,b);
            mainwin.config(bg=hxd);
            InstallImage.config(bg=hxd);
            InstallMessage.config(bg=hxd);
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
        for i in range(1,230):
            linux.time.sleep(.3);
            hxd=linux.math.floor((i/200)*100);
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
        ##end
        msgOverride=False;
    ##end
    def install_root_setup():
        global mainwin,msgOverride,msgText;
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
        for i in range(1,330):
            linux.time.sleep(.3);
            hxd=linux.math.floor((i/300)*100);
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
        ##end
        if (updAvailable):
            #update the environment.
            #linux.run_command('apt upgrade');
            count=0;
            for i in range(1,630):
                linux.time.sleep(.3);
                hxd=linux.math.floor((i/600)*100);
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
            ##end
        ##endif
        msgOverride=False;
    ##end
    def install_main_settings():
        global main;
        count=0;
        for i in range(1,310):
            linux.time.sleep(.3);
            hxd=linux.math.floor((i/300)*100);
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
        ##end
        linux.write_cfg('PyOS/cfg/main.pycfg',config);
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
            mainwin.update();
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
    finished=True;
    InstallMessage.setText('Install Complete, Enjoy PyOS! :)');
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
            mainwin.update();
        ##end
    ##end
    tween2();
    InstallMessage.destroy();
    InstallImage.destroy();
    run_stage2(config);
##end
def run_stage2(config):
    global mainwin,finished;
    from . import SetupExe as stage2;
    stage2.init(mainwin,config);
    stage2.main(2,['./SetupExe','--live']);
##end