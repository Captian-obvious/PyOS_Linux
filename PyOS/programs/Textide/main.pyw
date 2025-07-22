import configparser,json,os,platform,re,socket,sys,threading,time;
import tkinter as tk;
from tkinter import ttk;
def read_conf(path):
    conf=configparser.ConfigParser();
    conf.read(path);
    conf_dict={};
    for section in conf.sections():
        conf_dict[section]={};
        for k,v in conf.items(section):
            conf_dict[section][k]=v;
        ##end
    ##end
    return conf_dict;
##end
def write_conf(path,newconf):
    conf=configparser.ConfigParser();
    # Update existing configuration with newconf values
    conf.read(path);
    for section,section_data in newconf.items():
        if not conf.has_section(section):
            conf.add_section(section);
        ##endif
        for key,value in section_data.items():
            conf.set(section,key,value);
        ##end
    ##end
    # Write the updated configuration back to the file
    with open(path,'w') as cfgfile:
        conf.write(cfgfile);
    ##endwith
##end
class textide:
    def __init__(self):
        self.isInitialized=False;
        self.file_open_path="";
        self.window=None;
        self.window_exists=False;
        self.cur_conf={};
        self.tab_num=0;
    ##end
    def initialize(self,path=""):
        if not self.isInitialized:
            self.isInitialized=True;
            self.cur_conf={};
            self.make_window();
        ##endif
    ##end
    def make_window(self):
        if not self.window_exists:
            self.window_exists=True;
            self.window=tk.Tk();
            self.window.geometry("640x480");
            self.window.title("Textide - Open Source Text Editor");
            self.themeCurrent="Light";
            self.styles=ttk.Style(self.window);
            self.styles.theme_create('Light',parent="clam",settings={
                'TFrame':{
                    'configure':{
                        "background":"#fff",
                    },
                },
                'TLabel':{
                    'configure':{
                        'font': ('Ubuntu', 10)
                    },
                },
                'Large.TLabel':{
                    'configure':{
                        'font': ('Ubuntu', 20)
                    },
                },
                'Main.TFrame':{
                    'configure':{
                        "background":"#aaa",
                    },
                },
                'Main.TLabel':{
                    'configure':{
                        "background":"#000",
                    },
                },
                'Txt.TFrame':{
                    'configure':{
                        'background':"#fff",
                    },
                },
                'CS.TFrame':{
                    'configure':{
                        'background':"#eee",
                    },
                },
                'CS.TLabel':{
                    'configure':{
                        'background':"#eee",
                        'foreground':"#000",
                    },
                },
                'TNotebook':{
                    'configure':{
                        'background':"#eee",
                    },
                },
                'TNotebook.Tab':{
                    'configure':{
                        'background':"#fff",
                        'foreground':"#000",
                        'lightcolor':"#fff",
                        'padding':5,
                    },
                    "map": {
                        "background": [("active", "#fff"), ("selected", "#fff"), ("!selected", "#eee")],
                    },
                },
            });
            self.styles.theme_create('Dark',parent="clam",settings={
                'TFrame':{
                    'configure':{
                        "background":"#fff",
                    },
                },
                'TLabel':{
                    'configure':{
                        'font': ('Ubuntu', 10)
                    },
                },
                'Large.TLabel':{
                    'configure':{
                        'font': ('Ubuntu', 20)
                    },
                },
                'Main.TFrame':{
                    'configure':{
                        "background":"#333",
                    },
                },
                'Txt.TFrame':{
                    'configure':{
                        'background':"#333",
                    },
                },
                'CS.TFrame':{
                    'configure':{
                        'background':"#333",
                    },
                },
                'CS.TLabel':{
                    'configure':{
                        'background':"#333",
                        'foreground':"#f00",
                    },
                },
                'TNotebook':{
                    'configure':{
                        'background':"#000",
                    },
                },
                'TNotebook.Tab':{
                    'configure':{
                        'foreground':"#fff",
                        'lightcolor':"#333",
                        'padding':5,
                    },
                    "map": {
                        "background": [("active", "#333"), ("selected", "#333"), ("!selected", "#000")],
                    },
                },
            });
        ##endif
    ##end
    def coming_soon_page(self):
        self.styles.theme_use("Light");
        frame=ttk.Frame(self.window,style="CS.TFrame");
        frame.place(relx=0,rely=0,relwidth=1,relheight=1);
        title=ttk.Label(self.window,style="CS.TLabel",text="Application Coming Soon",anchor=tk.CENTER,font=("Ubuntu",20));
        title.place(relx=0,rely=.3,relwidth=1,relheight=.2);
        tagline=ttk.Label(self.window,style="CS.TLabel",text="Are you pythoned yet?",anchor=tk.CENTER,font=("Ubuntu",10));
        tagline.place(relx=0,rely=.5,relwidth=1,relheight=.1);
    ##end
    def main_page(self):
        self.styles.theme_use("Light");
        self.notebook=ttk.Notebook(self.window);
        self.add_tab_button=ttk.Frame(self.notebook);
        self.notebook.add(self.add_tab_button,text="+");
        self.notebook.bind("<Button-1>",self.on_tab_click);
        self.notebook.bind("<Double-1>",self.on_tab_double_click);
        self.create_ribbon();
        self.notebook.place(relx=0, rely=0.08, relwidth=1, relheight=0.92);
        frame0=self.add_tab();
    ##end
    def create_ribbon(self):
        self.ribbon = ttk.Frame(self.window, style='Main.TFrame');
        self.ribbon.place(relx=0, rely=0, relwidth=1, relheight=0.08);
        self.save_btn = ttk.Button(self.ribbon, text="Save", command=self.save_current_tab)
        self.save_btn.pack(side=tk.LEFT, padx=10, pady=5);
        self.theme_toggle = ttk.Button(self.ribbon, text="Toggle Theme", command=self.toggle_theme)
        self.theme_toggle.pack(side=tk.LEFT, padx=10);
    ##end
    def save_current_tab(self):
        current_tab_id = self.notebook.select();
        current_tab_widget = self.notebook.nametowidget(current_tab_id);
        # Ensure we're working with a valid editor tab
        if hasattr(current_tab_widget, 'textarea'):
            filename = self.notebook.tab(current_tab_id, "text");
            content = current_tab_widget.textarea.get("1.0", tk.END)
            from tkinter import filedialog;
            file_path = filedialog.asksaveasfilename(
                initialfile=f"{filename}",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"),("Python Source Files", "*.py"),("Python Source Files", "*.pyw"), ("All Files", "*.*")],
                title="Save As"
            );
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content);
                        file.close();
                    ##endwith
                except Exception as e:
                    print("Error saving file:", e);
                ##endtry
            ##endif
        ##endif
    ##end
    def toggle_theme(self):
        current = self.styles.theme_use();
        new_theme = "Dark" if current == "Light" else "Light";
        self.themeCurrent=new_theme;
        self.styles.theme_use(new_theme);
        self.apply_theme_to_tabs(new_theme);
    ##end
    def add_tab(self, title="Untitled"):
        new_tab = self.editor_tab(self.notebook, title=title,themeCurrent=self.themeCurrent);
        self.tab_num += 1;

        # Insert new tab before the "+" tab
        plus_index = self.notebook.index(self.add_tab_button);
        self.notebook.insert(plus_index, new_tab, text=title);
        time.sleep(0.1);
        self.notebook.select(new_tab);
        # Reinsert "+" tab at the end to ensure it's last
        self.notebook.forget(self.add_tab_button);
        self.notebook.add(self.add_tab_button, text="+");
        return new_tab;
    ##end
    def on_tab_click(self, event):
        current_tab_id = self.notebook.select();
        current_tab_widget = self.notebook.nametowidget(current_tab_id);
        if current_tab_widget == self.add_tab_button:
            self.add_tab();
        ##endif
    ##end
    def on_tab_double_click(self, event):
        clicked_index = self.notebook.index(f"@{event.x},{event.y}");
        clicked_tab_id = self.notebook.tabs()[clicked_index];
        clicked_widget = self.notebook.nametowidget(clicked_tab_id);
        if clicked_widget == self.add_tab_button:
            return;  # Prevent rename on "+" tab
        ##endif
        self.show_rename_entry(clicked_index, clicked_tab_id);
    ##end
    def show_rename_entry(self, tab_index, tab_id):
        tab_text = self.notebook.tab(tab_id, "text");
        
        # Create floating Entry widget for renaming
        rename_entry = tk.Entry(self.window);
        rename_entry.insert(0, tab_text);
        rename_entry.select_range(0, tk.END);
        rename_entry.focus();
        # Position it near top—fine-tune if needed
        rename_entry.place(x=tab_index*20, rely=0.1, width=100);  # rough placement
        def rename_tab(event=None):
            new_title = rename_entry.get();
            if new_title.strip():
                self.notebook.tab(tab_id, text=new_title);
            ##end
            rename_entry.destroy();
        ##end
        rename_entry.bind("<Return>", rename_tab);
        rename_entry.bind("<FocusOut>", rename_tab);
        
    ##end
    def apply_theme_to_tabs(self, theme):
        # Loop through all tabs and update their background colors
        for tab_id in self.notebook.tabs():
            tab_widget = self.notebook.nametowidget(tab_id);
            if hasattr(tab_widget, 'textarea'):
                if theme == "Dark":
                    tab_widget.textarea.config(bg="#333", fg="#fff", insertbackground="#fff");
                else:
                    tab_widget.textarea.config(bg="#fff", fg="#000", insertbackground="#000");
                ##endif
            ##endif
        ##end
    ##end
    class editor_tab(ttk.Frame):
        def __init__(self,master,title="Untitled",themeCurrent="Light",**kwargs):
            ttk.Frame.__init__(self,master,**kwargs);
            self.parent_notebook=master;
            if themeCurrent == "Dark":
                bg_color = "#333";
                fg_color = "#fff";
            else:
                bg_color = "#fff";
                fg_color = "#000";
            ##endif
            self.textarea=tk.Text(self,bg=bg_color, fg=fg_color, insertbackground=fg_color,font=("Ubuntu", 10), undo=True);
            self.textarea.place(relx=0.5,rely=0.5,relwidth=.98,relheight=.98,anchor=tk.CENTER);
            self.parent_notebook.add(self,text=title);
        ##end
    ##end
##end
app=textide();
app.initialize();
app.main_page();
app.window.mainloop();
