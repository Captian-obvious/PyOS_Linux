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
class MaterialSpinner(ui.Canvas):
    def __init__(self,root,canvas_size=200,animation_length=2.0,arc_width=6,arc_color:tuple|str='blue',bg_color='white'):
        super().__init__(root,width=canvas_size,height=canvas_size,bg=bg_color,highlightbackground=bg_color);
        self.root=root;
        self.frame_num=0;
        self.canvas_size=canvas_size;
        self.arc_color=arc_color if isinstance(arc_color,tuple) else (arc_color,);
        self.bg_color=bg_color;
        self.arc_duration=animation_length/len(self.arc_color);
        self.start_angle=0;
        self.arc_width=arc_width;
        self.extent=0;
        self.elapsed=0;
        self.stopped=False;
        self.draw_arc();
    ##end
    def ease_quad_in_out(self,t):
        return 2*t*t if t < 0.5 else -1+(4-2*t)*t;
    ##end
    def get_rgb(self,color_str):
        return self.winfo_rgb(color_str);
    ##end
    def interpolate_color(self,start_color,end_color,t,interpolate_start=0.95):
        if t < interpolate_start:
            return start_color;  # Use the start color until 95% of the duration
        else:
            # Normalize t to the range [0,1] within the interpolation interval
            t=(t - interpolate_start) / (1 - interpolate_start);
            start_r,start_g,start_b=self.get_rgb(start_color);
            end_r,end_g,end_b=self.get_rgb(end_color);
            new_r=int(start_r+(end_r - start_r)*t);
            new_g=int(start_g+(end_g - start_g)*t);
            new_b=int(start_b+(end_b - start_b)*t);
            return f'#{new_r:04x}{new_g:04x}{new_b:04x}';
        ##endif
    ##end
    def draw_arc(self):
        self.frame_num+=1;
        self.elapsed+=50;
        num_colors=len(self.arc_color);
        self.delete("arc"+str(self.frame_num-1));
        current_time=linux.time.time();
        t=(current_time%self.arc_duration) / self.arc_duration;
        eased_t=self.ease_quad_in_out(t);
        self.extent=eased_t*360;
        self.start_angle=(current_time*(360 / self.arc_duration))*1.35%360;
        # Determine the current color
        span=self.arc_duration;
        index=int(current_time//span)%num_colors;
        next_index=(index+1)%num_colors;
        local_t=(current_time%span) / span;
        interpolated_color=self.interpolate_color(self.arc_color[index],self.arc_color[next_index],local_t);
        #max(0,min(self.extent,270))
        self.create_arc(self.canvas_size*0.2,self.canvas_size*0.2,self.canvas_size*0.8,self.canvas_size*0.8,start=self.start_angle,extent=max(0,min(self.extent,270)),outline=interpolated_color,width=self.arc_width,style="arc",tags="arc"+str(self.frame_num));
        if not self.stopped:
            self.root.after(50,self.draw_arc);
        else:
            self.delete("all");
        ##endif
    ##end
    def stop(self):
        self.stopped=True;
    ##end
##end
class BootupSpinner(ui.Canvas):
    def __init__(self,root,canvas_size=200,animation_length=2.0,arc_width=6,arc_color='blue',bg_color='white',arc_extent=75):
        super().__init__(root, width=canvas_size, height=canvas_size, bg=bg_color, highlightbackground=bg_color);
        self.root=root;
        self.frame_num=0;
        self.canvas_size=canvas_size;
        self.arc_color=(arc_color,) if isinstance(arc_color, str) else arc_color;
        self.bg_color=bg_color;
        self.arc_duration=animation_length / len(self.arc_color);
        self.start_angle=0;
        self.start_angle2=180;
        self.arc_width=arc_width;
        self.extent1=arc_extent;
        self.extent=0;
        self.elapsed=0;
        self.stopped=False;
        self.draw_arc();
    ##end
    def ease_quad_in_out(self,t):
        return 2*t*t if t < 0.5 else -1+(4 - 2*t)*t;
    ##end
    def interpolate_color(self,start_color,end_color,t,interpolate_start=0.95):
        if t < interpolate_start:
            return start_color;
        else:
            t=(t - interpolate_start) / (1 - interpolate_start);
            start_r,start_g,start_b=self.winfo_rgb(start_color);
            end_r, end_g, end_b=self.winfo_rgb(end_color);
            new_r=int(start_r+(end_r - start_r)*t);
            new_g=int(start_g+(end_g - start_g)*t);
            new_b=int(start_b+(end_b - start_b)*t);
            return f'#{new_r:04x}{new_g:04x}{new_b:04x}';
        ##endif
    ##end
    def draw_arc(self):
        self.frame_num+=1;
        self.elapsed+=50;
        num_colors=len(self.arc_color);
        self.delete("arc"+str(self.frame_num - 1));
        current_time=linux.time.time();
        t=(current_time%self.arc_duration) / self.arc_duration;
        eased_t=self.ease_quad_in_out(t);
        self.extent=eased_t*360;
        self.start_angle=(current_time*(360 / self.arc_duration))*1.35%360;
        self.start_angle2=(self.start_angle+180)%360;
        span=self.arc_duration;
        index=int(current_time//span)%num_colors;
        next_index=(index+1)%num_colors;
        local_t=(current_time%span)/span;
        interpolated_color=self.interpolate_color(self.arc_color[index],self.arc_color[next_index],local_t);
        self.create_arc(self.canvas_size*0.2,self.canvas_size*0.2,self.canvas_size*0.8,self.canvas_size*0.8,start=self.start_angle,extent=self.extent1,outline=interpolated_color,width=self.arc_width,style="arc",tags="arc"+str(self.frame_num));
        self.create_arc(self.canvas_size*0.2,self.canvas_size*0.2,self.canvas_size*0.8,self.canvas_size*0.8,start=self.start_angle2,extent=self.extent1,outline=interpolated_color,width=self.arc_width,style="arc",tags="arc"+str(self.frame_num));
        if not self.stopped:
            self.root.after(50, self.draw_arc);
        else:
            self.delete("all");
        ##endif
    ##end
    def stop(self):
        self.stopped=True;
    ##end
##end
def init():
    global main,for_install,c_auth_user;
    if (linux.is_live_boot()==True):
        for_install=True;
    ##endif
    main=ui.Window();
    main.config(bg='#333');
    main.setAttribute('fullscreen',True);
    main.attributes('-topmost',0);
##    LoadMsg=ui.Label(main,text='...',font=('Ubuntu',20),fg='#fff',bg='#333',height=1);
##    LoadMsg.place(relx=.5,rely=1,relwidth=1,anchor=ui.S);
##    #oldlen=5.2;
##    BootSpinner=BootupSpinner(main,canvas_size=96,animation_length=3.2,arc_width=6,arc_color=("#fff","#fff"),bg_color="#333");
##    BootSpinner.place(relx=.5,rely=.9,anchor=ui.S);
##    main.update(); #fixes the window size values for future use
##    main.attributes('-topmost',0);
##    main.bootIcon=icon=ui.PhotoImage(file='PyOS/assets/BootLogo.png');
##    LoadImg=ui.Label(main,text='',font=('Ubuntu',20),fg='#fff',bg='#333',height='128px',width='128px',image=icon);
##    LoadImg.place(relx=.5,rely=.5,anchor=ui.CENTER);
##    main.update();
##    # count=0;
##    # for i in range(0,30):
##    #     count+=1;
##    #     if (count>3):
##    #         count=0;
##    #     ##endif
##    #     ct='.'*count;
##    #     LoadMsg.setText(f'{ct}Loading{ct}');
##    #     main.update();
##    #     linux.time.sleep(.35);
##    # ##end
##    count=0;
##    load_time=linux.time.time();
##    start_time=linux.time.time();
##    update_time=start_time;
##    total_updates=0;  # Keep track of the number of .35-second updates
##    boot_time=0;
##    expected_boot_time=13.3; #time in seconds boot is suppose to take.
##    expected_boot_time_old=10.5;
##    while boot_time<expected_boot_time:  # Run for 30 updates
##        current_time=linux.time.time();
##        boot_time=current_time-start_time;
##        # Update the main every 50 milliseconds
##        if (current_time - update_time) >= 0.05:
##            main.update()
##            update_time=current_time;
##        ##endif
##        if (current_time - load_time) >= 0.35:
##            count+=1;
##            if count > 3:
##                count=0;
##            ##endif
##            ct='.'*count;
##            LoadMsg.setText(f'{ct}Loading{ct}');
##            load_time=current_time;
##            total_updates+=1;
##        ##endif
##        # Add a small delay to avoid busy-waiting
##        linux.time.sleep(0.01);
##    ##end
##    BootSpinner.stop();
    main.update();
##    try:
##        bootlog=open('/etc/bootlog','w+');
##        bootlog.write(f'boot_time={boot_time}');
##        bootlog.close();
##    except Exception as e:
##        print('failed to write boot log, no changes were made to "/etc/bootlog"');
##    ##endtry
##    linux.time.sleep(1);
##    LoadImg.destroy();
##    LoadMsg.destroy();
##end
def load():
    global main,for_install,c_auth_user;
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
        return;
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
                root.update();
                root.destroy();
                callback(main,cfg,user);
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
def set_current_window(win):
    global main;
    main=win;
##end
def restart(config):
    global main,msg,count;
    count=0;
    def restart_msg():
        global count,main,msg;
        if linux.os.path.exists('./splash') or linux.os.path.exists('./splash.exe'):
            if linux.os.name=="nt":
                linux.runner.run(['splash','--mode=shutdown','--reboot']);
            else:
                linux.runner.run(['./splash','--mode=shutdown','--reboot']);
            ##endif
        else:
            if linux.os.name=="nt":
                linux.runner.run(['pythonw','plymouth_boot.pyw','--mode=shutdown ','--reboot']);
            else:
                linux.runner.run(['./plymouth_boot.pyw','--mode=shutdown ','--reboot']);
            ##endif
        ##endif
    ##end
    def restart_fn():
        global main;
        linux.write_cfg('PyOS/cfg/main.pycfg',config);
        linux.restart();
    ##end
    restart_task=linux.task.Thread(target=restart_msg);
    restart_task.start();
    main.destroy();
    restart_msg();
    #__NOT YET FULLY IMPLEMENTED__
    quit();
##end
def shutdown(config):
    global main,msg,count;
    count=0;
    def shutdown_msg():
        global count,main,msg;
        if linux.os.path.exists('./splash') or linux.os.path.exists('./splash.exe'):
            if linux.os.name=="nt":
                linux.runner.run(['splash','--mode=shutdown']);
            else:
                linux.runner.run(['./splash','--mode=shutdown']);
            ##endif
        else:
            if linux.os.name=="nt":
                linux.runner.run(['pythonw','plymouth_boot.pyw','--mode=shutdown']);
            else:
                linux.runner.run(['./plymouth_boot.pyw','--mode=shutdown']);
            ##endif
        ##endif
    ##end
    def shutdown_fn():
        global main;
        linux.write_cfg('PyOS/cfg/main.pycfg',config);
        linux.shutdown();
    ##end
    shutdown_task=linux.task.Thread(target=shutdown_fn);
    shutdown_task.start();
    main.destroy();
    shutdown_msg();
    quit();
##end
