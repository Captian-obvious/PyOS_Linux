import tkinter as tk;
import threading as task;
TerminalFrame=None;
try:
    from .pyTerm import TerminalFrame as t;
    TerminalFrame=t;
except ImportError as e:
    import pyTerm
    TerminalFrame=pyTerm.TerminalFrame;
##endtry
import os,sys;
thisdir=os.path.dirname(os.path.realpath(__file__));
imported=False;

def main(exec_path=None,auth_user=None):
    root=tk.Tk();
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
