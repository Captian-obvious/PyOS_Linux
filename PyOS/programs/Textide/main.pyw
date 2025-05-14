#!/usr/bin/env python
import os,sys,time;
import tkinter as tk;
import tkinter.ttk as ttk;

class textide:
    def __init__(self):
        self.tabs=[];
        self.tab_count=0;
        self.isInitialized=False;
        self.hasSaveFinished=False;
        self.hasDownloadFinished=False;
        self.state="idle";
        self.path_to_open="";
        self.window=None;
        self.notebook=None;
    ##end
    def initialize(self,file_path=""):
        if not self.isInitialized:
            print("Initializing Textide...");
            self.isInitialized=True;
            self.path_to_open=file_path;
            self.window=tk.Tk();
            self.window.title("Textide - Open Source Text Editor");
            self.window.geometry("640x480");
            self.style=ttk.Style();
        ##endif
    ##end
    def startSession(self):
        pass;
    ##end
    def coming_soon(self):
        theframe=tk.Frame(self.window);
        theframe.place(relx=.5,rely=.5,relwidth=.8,relheight=.8,anchor=tk.CENTER);
        thetitle=tk.Label(theframe,anchor=tk.CENTER,text="Application coming soon",font=("Ubuntu",20));
        thetitle.place(relx=.5,rely=.4,relwidth=1,anchor=tk.CENTER);
        thesubtitle=tk.Label(theframe,anchor=tk.CENTER,text="Are you pythoned yet?",font=("Ubuntu",14),fg="#444444");
        thesubtitle.place(relx=.5,rely=.55,relwidth=1,anchor=tk.CENTER);
    ##end
##end

app=textide();
app.initialize();
app.coming_soon();
app.window.mainloop();
