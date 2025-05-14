import tkinter as tk;
import threading as task;
from pyTerm import TerminalFrame;
import os,sys;
thisdir=os.path.dirname(os.path.realpath(__file__));
imported=False;

def main(argc,argv):
    global imported;
    if imported:
        return;
    ##endif
    imported=True;
    if argc<2:
        print("Usage: python3 -m pyOS.programs.Terminal <exec_path>");
        return;
    ##endif
    root=tk.Tk();
    auth_user,ec=os.system('whoami'); # Get the current user (Exit code is not used)
    if ec!=0:
        print("Error: could not get the current user");
        return;
    ##endif
    exec_path=argv[1];
    if not os.path.exists(exec_path):
        print("Error: no such file or directory: "+exec_path);
        return;
    ##endif
    root.title('Terminal');
    root.geometry("640x480");
    root.focus_force();
    root.iconphoto(True,tk.PhotoImage('term_icon',master=root,file=thisdir+'/favicon.png'));
    def startApp():
        terminalFrame=TerminalFrame(root,bg='#434343',exec_path=exec_path,user=auth_user);
        terminalFrame.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=tk.CENTER);
        terminalFrame.initialize();
    ##end
    t=task.Thread(target=startApp);
    t.daemon=True;
    t.start();
    root.mainloop();
##end
main(len(sys.argv),sys.argv);
