import tkinter as tk;
import tkinter.ttk as ttk;
from PyOS.Modules.tksvg import SvgImage;
class UI:
    N=tk.N;
    NE=tk.NE;
    E=tk.E;
    SE=tk.SE;
    S=tk.S;
    SW=tk.SW;
    W=tk.W;
    NW=tk.NW;
    C=tk.CENTER;
    CENTER=tk.CENTER;
    NSEW=tk.NSEW;
    YES=tk.YES;
    NO=tk.NO;
    BOTH=tk.BOTH;
    X=tk.X;
    Y=tk.Y;
    LEFT=tk.LEFT;
    RIGHT=tk.RIGHT;
    TOP=tk.TOP;
    BOTTOM=tk.BOTTOM;
    END=tk.END;
    UNITS=tk.UNITS;
    NONE=tk.NONE;
    HORIZONTAL=tk.HORIZONTAL;
    VERTICAL=tk.VERTICAL;
    NORMAL=tk.NORMAL;
    DISABLED=tk.DISABLED;
    HIDDEN=tk.HIDDEN;
    ACTIVE=tk.ACTIVE;
    ANCHOR=tk.ANCHOR;
    ARC=tk.ARC;
    CHORD=tk.CHORD;
    ALL=tk.ALL;
    BASELINE=tk.BASELINE;
    BEVEL=tk.BEVEL;
    BROWSE=tk.BROWSE;
    BUTT=tk.BUTT;
    CASCADE=tk.CASCADE;
    CHAR=tk.CHAR;
    CHECKBUTTON=tk.CHECKBUTTON;
    COMMAND=tk.COMMAND;
    CURRENT=tk.CURRENT;
    DOTBOX=tk.DOTBOX;
    EXCEPTION=tk.EXCEPTION;
    EXTENDED=tk.EXTENDED;
    FALSE=tk.FALSE;
    FLAT=tk.FLAT;
    FIRST=tk.FIRST;
    GROOVE=tk.GROOVE;
    INSERT=tk.INSERT;
    INSIDE=tk.INSIDE;
    LAST=tk.LAST;
    MITER=tk.MITER;
    MOVETO=tk.MOVETO;
    MULTIPLE=tk.MULTIPLE;
    NUMERIC=tk.NUMERIC;
    OFF=tk.OFF;
    ON=tk.ON;
    OUTSIDE=tk.OUTSIDE;
    PAGES=tk.PAGES;
    PIESLICE=tk.PIESLICE;
    PROJECTING=tk.PROJECTING;
    ROUND=tk.ROUND;
    RADIOBUTTON=tk.RADIOBUTTON;
    RAISED=tk.RAISED;
    READABLE=tk.READABLE;
    RIDGE=tk.RIDGE;
    SCROLL=tk.SCROLL;
    SEL=tk.SEL;
    SEL_FIRST=tk.SEL_FIRST;
    SEL_LAST=tk.SEL_LAST;
    SEPARATOR=tk.SEPARATOR;
    SINGLE=tk.SINGLE;
    SOLID=tk.SOLID;
    SUNKEN=tk.SUNKEN;
    TRUE=tk.TRUE;
    UNDERLINE=tk.UNDERLINE;
    UNITS=tk.UNITS;
    WORD=tk.WORD;
    WRITABLE=tk.WRITABLE;
    class Event(tk.Event):
        def __init__(self):
            super().__init__();
        ##end
    ##end
    def __init__(self):
        pass;
    ##end
    class Wm(tk.Wm):
        def __init__(self):
            tk.Wm.__init__(self);
        ##end
    ##end
    class PhotoImage(tk.PhotoImage):
        def __init__(self,name:str|None=None,cnf={},*args,**kwargs):
            tk.PhotoImage.__init__(self,name,cnf,*args,**kwargs)
        ##end
    ##end
    class StringVar(tk.StringVar):
        def __init__(self,master,value='',name=None):
            tk.StringVar.__init__(self,master,value,name);
        ##end
    ##end
    class IntVar(tk.IntVar):
        def __init__(self,master,value=0,name=None):
            tk.IntVar.__init__(self,master,value,name);
        ##end
    ##end
    class BooleanVar(tk.BooleanVar):
        def __init__(self,master,value=False,name=None):
            tk.BooleanVar.__init__(self,master,value,name);
        ##end
    ##end
    class Window(tk.Tk):
        def __init__(self,screenName=None,width=400,height=300,title="Window",icon=None,**kwargs):
            tk.Tk.__init__(self,screenName,**kwargs);
            self.geometry(f"{width}x{height}");
            self.title(title);
            if (icon!=None):
                self.iconphoto(True,tk.PhotoImage(file=icon));
            ##endif
        ##end
        def setIcon(self,path):
            self.iconphoto(True,tk.PhotoImage(file=path));
        ##end
        def setTitle(self,title):
            self.title(title);
        ##end
        def setSize(self,width=400,height=300):
            self.geometry(f"{width}x{height}");
        ##end
        def setAttribute(self,attribute,value):
            if (attribute=='fullscreen' or attribute=='isfullscreen'):
                self.attributes('-fullscreen',value);
            elif (attribute=='resizeable' or attribute=='isresizeable'):
                self.resizable(value[0],value[1]);
            else:
                self.attributes(attribute,value);
            ##endif
        ##end
    ##end
    class Label(tk.Label):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Label.__init__(self,master,cnf,*a,**kwargs);
        ##end
        def setText(self,text):
            self.config(text=text);
        ##end
        def setFont(self,font):
            self.config(font=font);
        ##end
        def setImage(self,path,isSVG=False):
            if isSVG:
                self.config(image=SvgImage(file=path));
            else:
                self.config(image=tk.PhotoImage(file=path));
            ##endif
        ##end
    ##end
    class Button(tk.Button):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Button.__init__(self,master,cnf,*a,**kwargs);
        ##end
        def setText(self,text):
            self.config(text=text);
        ##end
        def setFont(self,font):
            self.config(font=font);
        ##end
        def setCommand(self,command):
            self.config(command=command);
        ##end
        def setImage(self,path,isSVG=False):
            if isSVG:
                self.config(image=SvgImage(file=path));
            else:
                self.config(image=tk.PhotoImage(file=path));
            ##endif
        ##end
    ##end
    class Entry(tk.Entry):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Entry.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Frame(tk.Frame):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Frame.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Canvas(tk.Canvas):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Canvas.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Scrollbar(tk.Scrollbar):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Scrollbar.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Listbox(tk.Listbox):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Listbox.__init__(self,master,cnf,*a,**kwargs);
        ##end
        def appendText(self,text):
            self.insert(tk.END,text);
        ##end
    ##end
    class Combobox(ttk.Combobox):
        def __init__(self,master,cnf={},*a,**kwargs):
            ttk.Combobox.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Text(tk.Text):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Text.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Menu(tk.Menu):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Menu.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Checkbutton(tk.Checkbutton):
        def __init__(self,master,cnf={},*a,**kwargs):
            tk.Checkbutton.__init__(self,master,cnf,*a,**kwargs);
        ##end
    ##end
    class Treeview(ttk.Treeview):
        def __init__(self,master,*a,**kwargs):
            ttk.Treeview.__init__(self,master,*a,**kwargs);
        ##end
    ##end
    class Progressbar(ttk.Progressbar):
        def __init__(self,master,*a,**kwargs):
            ttk.Progressbar.__init__(self,master,*a,**kwargs);
        ##end
    ##end
    class CLabel(ttk.Label):
        def __init__(self,master,*a,**kwargs):
            ttk.Label.__init__(self,master,*a,**kwargs);
        ##end
        def setText(self,text):
            self.config(text=text);
        ##end
        def setFont(self,font):
            self.config(font=font);
        ##end
        def setImage(self,path,isSVG=False):
            if isSVG:
                self.config(image=SvgImage(file=path));
            else:
                self.config(image=tk.PhotoImage(file=path));
            ##endif
        ##end
    ##end
    class CButton(ttk.Button):
        def __init__(self,master,*a,**kwargs):
            ttk.Button.__init__(self,master,*a,**kwargs);
        ##end
        def setText(self,text):
            self.config(text=text);
        ##end
        def setCommand(self,command):
            self.config(command=command);
        ##end
        def setImage(self,path,isSVG=False):
            if isSVG:
                self.config(image=SvgImage(file=path));
            else:
                self.config(image=tk.PhotoImage(file=path));
            ##endif
        ##end
    ##end
    class CEntry(ttk.Entry):
        def __init__(self,master=None,*a,**kwargs):
            ttk.Entry.__init__(self,master,*a,**kwargs);
        ##end
    ##end
    class CFrame(ttk.Frame):
        def __init__(self,master,*a,**kwargs):
            ttk.Frame.__init__(self,master,*a,**kwargs);
        ##end
    ##end
    class Style(ttk.Style):
        def __init__(self,master):
            ttk.Style.__init__(self,master);
        ##end
    ##end
##end
class Custom_UI:
    def __init__(self):
        pass;
    ##end
##end