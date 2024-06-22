import tkinter as tk;
import os,pty,queue,re,sys,time;
import threading as task;
import subprocess as sub;

def bindFn(fn,*args,**kwargs):
    def nfn(*args2,**kwargs2):
        return fn(*args,*args2,*kwargs,*kwargs2);
    ##end
    return nfn;
##end

def hostname():
    with open('/etc/hostname','r') as f:
        hn=f.read();
        f.close();
        return hn.strip();
    ##endwith
##end

class sh_cmds:
    def __init__(self):
        self.cmd_literals=[
            {'cmd':'clear','desc':'clears the terminal','valid':['clear','clr','cls'],'arguments':'None'},
            {'cmd':'help','desc':'shows all commands','valid':['help'],'arguments':'(opt)<command>'},
            {'cmd':'exit','desc':'exits the terminal','valid':['exit','quit','q'],'arguments':'None'},
            {'cmd':'mkdir','desc':'creates a directory in the working path.','valid':['makedir','mkdir','md'],'arguments':'<dir_name>'},
            {'cmd':'cdir','desc':'changes the working directory.','valid':['chdir','cdir','cd'],'arguments':'<path>'},
            {'cmd':'remove','desc':'removes a file or directory.','valid':['remove','rm','rmdir'],'arguments':'[-rf|-r|-f] <path or file>'},
            {'cmd':'move','desc':'moves a file or directory.','valid':['move','mv'],'arguments':'<source> <destination>'},
            {'cmd':'copy', 'desc':'copies a file or directory.','valid':['copy','cp'],'arguments':'[-rf|-r|-f] <source> <destination>'},
            {'cmd':'python','desc':'Python Interpreter (if installed)','valid':['py','>>>'],'arguments':'<code or path>'},
            {'cmd':'battery_firmware','desc':'Access various parts of battery firmware','valid':['battery_firmware','battery_fw','batt_fw'],'arguments':'[-get|-set] <name> (opt)<value>'},
            {'cmd':'battery_status','desc':'Shows the status of the battery','valid':['battery_status','battery_stat','batt_stat'],'arguments':'(opt)<stat>'},
            {'cmd':'wifi_scan','desc':'Scans for available wifi networks','valid':['wifiscan','wifi_scan'],'arguments':'None'},
            {'cmd':'wifi_connect','desc':'Connects to a wifi network','valid':['wifi_connect','wifi_conn','wifi_c'],'arguments':'<ssid> (opt)<password>',},
        ]
    ##end
    def get_cmd(self,cmdstr):
        cmd_ran=None;
        cmdstr=cmdstr.lower();
        cmd_args=cmdstr.split(' ');
        cmd=cmd_args[0];
        cmd_args.pop(0);
        for cmd_literal in self.cmd_literals:
            if cmd in cmd_literal['valid']:
                cmd_ran={'name':cmd_literal['cmd'],'args':cmd_args};
                break;
            ##endif
        ##end
        if (cmd_ran==None):
            cmd_ran={'name':cmd,'args':cmd_args};
        ##endif
        return cmd_ran;
    ##end
    def run_builtin(self,cmd_ran,*args):
        if cmd_ran['name']=='clear':
            args[0].clear_text();
        elif cmd_ran['name']=='help':
            args[0].type_str('Available Commands:');
            for cmd_literal in self.cmd_literals:
                args[0].type_str(cmd_literal['cmd']+' - '+cmd_literal['desc']);
                args[0].type_str('  Arguments: '+str(cmd_literal['arguments']));
                args[0].type_str(''); # Buffer
            ##end
            return {"ran":True,"cmd":cmd_ran};
        elif cmd_ran['name']=='exit':
            pass;
        else:
            return {"ran":False,"cmd":cmd_ran};
        ##endif
    ##end
##end

class TerminalFrame(tk.Frame):
    def __init__(self,master,cnf={},**kwargs):
        if ('exec_path' in kwargs):
            self.exec_path=kwargs['exec_path'];
            self.path=self.parse_path(self.exec_path);
            kwargs.pop('exec_path');
        else:
            self.exec_path=os.getcwd();
            self.path=self.parse_path(self.exec_path);
        ##endif
        if ('privs' in kwargs and 'root' in kwargs['privs'] and kwargs['privs']['root']==True):
            self.exec_path='/PyOS'
            self.path=self.parse_path(self.exec_path);
            kwargs.pop('privs');
        ##endif
        if ('user' in kwargs):
            self.prefix=kwargs['user']+"@"+hostname()+": ";
            kwargs.pop('user');
        else:
            self.prefix=hostname()+": ";
        ##endif
        tk.Frame.__init__(self,master,cnf,**kwargs);
        self.isInitialized=False;
        self.typing=False;
        self.cmdToRun=None;
        self.curr_text='';
        #self.mainTextArea=tk.Listbox(self,bg='#434343',fg='#f90',font=('Courier New',10),highlightcolor='#434343', highlightthickness=0,selectbackground='#434343',selectforeground="#f90",activestyle=tk.NONE,selectmode='single');
        self.mainTextArea=tk.Text(self,bg='#434343',fg='#f90',font=('Courier New',10),highlightcolor='#434343', highlightthickness=0,selectbackground='#434343',selectforeground="#f90",insertbackground="#f00");
        self.scrollbar=tk.Scrollbar(self);
        self.copyrightStr='Copyright (c) 2024, PyOS Developers\n';
        self.versionStr='Version: 1.11.0\n';
        self.Keybinds={'<Return>':lambda x :self.enter_key_callback(),'<BackSpace>':lambda x :self.backspace_callback(),'<KeyPress>':lambda x :self.keypress_callback(x.char),'<KeyRelease>':lambda x :self.keyrelease_callback(x.char)};
        self.cursor_index=0;
        self.cursor_visible=tk.BooleanVar(self.master,value=True);
        self.mainTextArea.pack(expand=1,fill=tk.BOTH);
        self.scrollbar.place(relx=1,rely=.5,width=10,relheight=1,anchor=tk.E);
        self.log='';
    ##end
    def endsWith(self,s1,s2):
        return s1.endswith(s2);
    ##end
    def startsWith(self,s1, s2):
        return s1.startswith(s2);
    ##end
    def stringContains(self,s, s2):
        return s2 in s;
    ##end
    def execLater(self,func,func2,ti):
        def run():
            t=__import__('time');
            t.sleep(ti);
            if func:func();
            ##endif
            if func2:func2();
            ##endif
        ##end
        runner=task.Thread(target=run);
        runner.start();
    ##end
    def parse_path(self,path):
        home_path_regex=r'^(\/home\/[A-Za-z0-9_]+)(?:.*)';
        home_path_regex_match=re.match(home_path_regex,path);
        if (home_path_regex_match):
            mstr=home_path_regex_match.group(1);
            print(mstr);
            newpath=path.replace(mstr,'~');
            return newpath;
        else:
            return path;
        ##endif
    ##end
    # def run_cmd(self,cmd="",lastLI=0):
    #     os.environ['PYTHONUNBUFFERED']='1';
    #     process=sub.Popen(cmd,stdin=sub.PIPE,stdout=sub.PIPE,stderr=sub.STDOUT,shell=True,universal_newlines=True,cwd=self.exec_path);
    #     global inputting;
    #     inputting=False;
    #     #before we run any executables, check for if the user ran "cd" to avoid broken directories.
    #     if (self.startsWith(cmd,'cd')):
    #         path=cmd.split(' ')[1];  # Get the directory from the command
    #         try:
    #             if path.startswith('~'):
    #                 path=path.replace('~','');
    #                 path=os.path.expanduser('~')+path;
    #             ##endif
    #             os.chdir(path);  # Change the directory
    #             self.exec_path=os.getcwd();  # Update the exec_path variable to the new directory
    #             self.path=self.parse_path(self.exec_path);
    #             self.refresh();
    #             self.master.update();
    #             print(f"Directory changed to {self.path}");
    #         except FileNotFoundError:
    #             self.mainTextArea.insert(tk.END,f"Directory not found: {path}\n");
    #             self.master.update();
    #         except PermissionError:
    #             self.mainTextArea.insert(tk.END,"Permission Denied\n");
    #             self.master.update();
    #         ##endtry
    #     ##endif
    #     #PROCESS I/O LOOP
    #     self.mainTextArea.unbind("<Return>");
    #     self.curr_text='';
    #     global outlen,enter_bound;
    #     enter_bound=False;
    #     def send_input(input,event):
    #         try:
    #             tosend=input+"\n";
    #             process.stdin.write(tosend);
    #             process.stdin.flush();
    #             inputting=False;
    #         except Exception as e:
    #             print(e);
    #         ##endtry
    #     ##end
    #     while process.poll() is None:
    #         def new_backspace(event):
    #             global outlen;
    #             return self.backspace_callback(def_len=outlen);
    #         ##end
    #         def new_enter(event):
    #             tosend=self.curr_text+"\n";
    #             process.stdin.write(tosend);
    #             process.stdin.flush();
    #             self.curr_text="";
    #         ##end
    #         self.mainTextArea.bind('<Return>',new_enter);
    #         self.mainTextArea.bind('<BackSpace>',new_backspace);
    #         output=process.stdout;
    #         output.flush();
    #         outlen=0;
    #         if (output):
    #             for line in output:
    #                 self.mainTextArea.insert(tk.END,line);
    #                 self.mainTextArea.see(tk.END);
    #                 self.mainTextArea.yview_moveto(1);
    #                 self.mainTextArea.mark_set(tk.INSERT,tk.END);
    #                 self.master.update();
    #             ##end
    #         else:
    #             break;
    #         ##endif
    #         outlen=0;
    #         self.master.update();
    #     ##end
    #     if cmd!="":
    #         self.mainTextArea.insert(tk.END,'\n');
    #     ##endif
    #     return process.returncode;
    # ##end
    def run_cmd(self,cmd="",lastLI=0):
        os.environ['PYTHONUNBUFFERED']='1';
        master_fd,slave_fd=pty.openpty();
        process=sub.Popen(cmd,stdin=slave_fd,stdout=slave_fd,stderr=slave_fd,close_fds=True,shell=True,universal_newlines=True,cwd=self.exec_path);
        global inputting;
        inputting=False;
        #before we run any executables, check for if the user ran "cd" to avoid broken directories.
        if (self.startsWith(cmd,'cd')):
            path=cmd.split(' ')[1];  # Get the directory from the command
            try:
                if path.startswith('~'):
                    path=path.replace('~','');
                    path=os.path.expanduser('~')+path;
                ##endif
                os.chdir(path);  # Change the directory
                self.exec_path=os.getcwd();  # Update the exec_path variable to the new directory
                self.path=self.parse_path(self.exec_path);
                self.refresh();
                self.master.update();
                print(f"Directory changed to {self.path}");
            except FileNotFoundError:
                self.mainTextArea.insert(tk.END,f"Directory not found: {path}\n");
                self.master.update();
            except PermissionError:
                self.mainTextArea.insert(tk.END,"Permission Denied\n");
                self.master.update();
            ##endtry
        ##endif
        #PROCESS I/O LOOP
        self.mainTextArea.unbind("<Return>");
        self.curr_text='';
        global outlen,enter_bound;
        outlen=0;
        enter_bound=False;
        def new_backspace(event):
            global outlen;
            # Your backspace callback logic here
            return self.backspace_callback(def_len=outlen);
        ##end
        def new_enter(event):
            tosend=self.curr_text+"\n";
            os.write(master_fd,tosend.encode());  # Write to the pty
            self.curr_text="";
        ##end
        self.mainTextArea.bind('<Return>', new_enter);
        self.mainTextArea.bind('<BackSpace>', new_backspace);
        while process.poll() is None:
            try:
                output=os.read(master_fd,1024);  # Read from the pty
                if output:
                    line=output.decode();
                    self.mainTextArea.insert(tk.END,line);
                    self.mainTextArea.see(tk.END);
                    self.mainTextArea.yview_moveto(1);
                    self.mainTextArea.mark_set(tk.INSERT,tk.END);
                    outlen=len(line);
                    self.master.update();
                ##end
            except OSError:
                break;  # End of file or error
            ##endtry
            time.sleep(0.01); #add a small delay to avoid busy looping.
        ##end
        # Close the master file descriptor
        os.close(master_fd);
        if cmd!="":
            self.mainTextArea.insert(tk.END,'\n');
        ##endif
        return process.returncode;
    ##end
    def send_to_process(self,process,command):
        process.stdin.write(command);
        #process.stdin.flush();
    ##end
    # def blink_cursor(self):
    #     if self.cursor_visible.get():
    #         self.mainTextArea.itemconfig(self.cursor_index,selectbackground="red");  # Show cursor
    #     else:
    #         self.mainTextArea.itemconfig(self.cursor_index,selectbackground="#434343");  # Hide cursor
    #     ##endif
    #     self.cursor_visible.set(not self.cursor_visible.get());  # Toggle visibility
    #     self.after(500,self.blink_cursor);  # Change cursor every 500 milliseconds
    #     self.master.update();
    # ##end
    def add_prefix(self,prefix,path):
        self.mainTextArea.tag_config('red', foreground='#e99');
        self.mainTextArea.tag_config('yellow', foreground='yellow');
        self.mainTextArea.insert(tk.END,prefix,'red');
        self.mainTextArea.insert(tk.END,path,'yellow');
        self.mainTextArea.insert(tk.END,'$ ');
        return f'{prefix+path}$ ';
    ##end
    def refresh(self,backspace=False):
        cursor_index=self.mainTextArea.index(tk.INSERT);
        if (self.curr_text!=f'{self.prefix+self.path}$ ' or backspace):
            self.mainTextArea.delete(f"{cursor_index} - 1 chars");
        ##endif
        self.master.update();
        return;
    ##end
    # def on_listbox_click(self,event):
    #     self.cursor_index=self.mainTextArea.nearest(event.y);  # Get the index of the clicked item
    # ##end
    # def on_item_appended(self,event):
    #     self.cursor_index=self.mainTextArea.size()-1;  # Set cursor to the last item
    # ##end
    def append_to_text(self,text,ymoveoverride=True):
        #self.mainTextArea.delete(tk.END);
        self.curr_text=self.curr_text+text;
        #self.mainTextArea.insert(tk.END,self.curr_text);
        if (ymoveoverride!=True):
            self.mainTextArea.yview_moveto(1);
        ##endif
    ##end
    def type_str(self,string):
        # types a given string automatically to the terminal.
        for k in string:
            self.append_to_text(k);
        ##end
        self.mainTextArea.yview_moveto(1);
        self.mainTextArea.see(tk.END);
        self.master.update();
        return;
    ##end
    def enter_key_callback(self):
        self.mainTextArea.insert(tk.END,'\n');
        compiler_thread=task.Thread(target=self.run_cmd,args=(self.curr_text[len(self.prefix+self.path)+2 : ],self.mainTextArea.size()));
        compiler_thread.daemon=True;
        compiler_thread.start();
        while (compiler_thread.is_alive()):
            self.master.update();
            time.sleep(0.1);
        ##end
        #self.run_cmd(self.curr_text[len(self.path)+2 : ],self.mainTextArea.size());        
        self.curr_text=self.add_prefix(self.prefix,self.path);
        # Insert new text at the end
        self.mainTextArea.see(tk.END);
        self.mainTextArea.yview_moveto(1);
        self.mainTextArea.mark_set(tk.INSERT,tk.END);
        self.mainTextArea.bind('<Return>',lambda event: self.enter_key_callback());
        self.mainTextArea.bind('<BackSpace>',lambda event: self.backspace_callback());
        self.master.update();
        return 'break';
    ##end
    def keypress_callback(self,key=''):
        if (key!=''):
            self.log+=f' (keydown - {key})';
            self.append_to_text(key);
            self.typing=True;
            self.master.update();
        ##endif
    ##end
    def keyrelease_callback(self,key=''):
        if (key!=' '):
            self.log+=f' (keyup - {key})';
            self.typing=False;
        ##endif
    ##end
    def backspace_callback(self,def_len=None):
        # callback for backspace key erases the last character.
        if (len(self.curr_text)>(len(self.prefix+self.path)+2 if def_len==None else def_len)):
            self.curr_text=self.curr_text[:-1];
            self.refresh(True);
            self.master.update();
        ##endif
        return 'break';
    ##end
    def initialize(self,startCmd=''):
        if (not self.isInitialized):
            print('I am initial');
            self.mainTextArea.insert(tk.END,"Welcome to the PyOS Terminal!\n");
            self.mainTextArea.insert(tk.END,"Type 'help' for a list of commands.\n");
            self.mainTextArea.insert(tk.END,self.copyrightStr);
            self.mainTextArea.insert(tk.END,self.versionStr);
            self.mainTextArea.insert(tk.END, '\n');
            self.mainTextArea.insert(tk.END, '\n');
            self.append_to_text(''); # Buffer.
            self.isInitialized=True;
            self.refresh();
            self.startSession(startCmd);
            self.addEventListeners();
            self.master.update();
        ##endif
    ##end
    def startSession(self,startCmd=''):
        print('I am session');
        if (startCmd!='' and startCmd!=' '):
            self.type_str(startCmd);
            self.run_cmd(startCmd,self.mainTextArea.size());
        ##endif
        self.curr_text=self.add_prefix(self.prefix,self.path); #Initialize the terminal with the correct string.
        self.master.update();
    ##end
    def addEventListeners(self):
        self.scrollbar.config(command=self.mainTextArea.yview);
        self.mainTextArea.config(yscrollcommand=self.scrollbar.set);
        self.addKeypressListeners();
        self.master.update();
    ##end
    def addKeypressListeners(self):
        global terminal_listbox;
        terminal_listbox=self.mainTextArea;
        for key,func in self.Keybinds.items():
            if (key!=None and func!=None):
                terminal_listbox.bind(key, func);
            ##endif
        ##end
        self.master.update();
    ##end
    def clear_text(self):
        self.mainTextArea.delete(0,tk.END);
    ##end
##end