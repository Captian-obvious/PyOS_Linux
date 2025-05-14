#!/usr/bin/env python
import tkinter as tk;
import tkinter.ttk as ttk;
import tkinter.messagebox as dialogs;
import json,os,re,sys,time;
import threading as task;
import subprocess as runner;
from PIL import Image,ImageTk;
imported=False;
thisdir=os.path.dirname(os.path.realpath(__file__));
def err_popup(title,msg):
    dialogs.showerror(title,msg);
##end
def isExecutable(path):
    # Check if the file is executable (an ELF or PyExe)
    return os.access(path,os.X_OK);
##end
def endswithregex(string,regex):
    # Check if the string ends with the regex
    return re.search(regex,string) is not None;
##end
def execute_prog(path,args):
    runner.call([path]);
##end
def jsonEncode(obj):
    return json.dumps(obj);
##end
def jsonDecode(obj):
    return json.loads(obj);
##end
def jsonDecodeF(obj):
    return json.load(obj);
##end
def test_function():
    print('test');
##end
def check_for_default_folders(sidebar:ttk.Treeview,pathChange,current_path): #Automatically constructs the sidebar if the default folders exist in a User's home directory.
    #check for defaults
    sidebar.home_icon=home_icon=tk.PhotoImage(master=sidebar,file=thisdir+'/assets/home_icon.png');
    sidebar.document_icon=document_icon=tk.PhotoImage(master=sidebar,file=thisdir+'/assets/document_icon.png');
    sidebar.downloads_icon=downloads_icon=tk.PhotoImage(master=sidebar,file=thisdir+'/assets/downloads_icon.png');
    sidebar.music_icon=music_icon=tk.PhotoImage(master=sidebar,file=thisdir+'/assets/music_icon.png');
    sidebar.desktop_icon=desktop_icon=tk.PhotoImage(master=sidebar,file=thisdir+'/assets/desktop_icon.png');
    sidebar.python_icon=python_icon=tk.PhotoImage(master=sidebar,file=thisdir+'/assets/python_folder_icon.png');
    if (os.path.exists(os.path.join(os.path.expanduser('~')))):
        #add home shortcut
        sidebar.insert('','end',text='Home',image=home_icon);
    ##endif
    if (os.path.exists(os.path.join(os.path.expanduser('~'),'Documents'))):
        #add documents shortcut
        sidebar.insert('','end',text='Documents',image=document_icon);
    ##endif
    if (os.path.exists(os.path.join(os.path.expanduser('~'),'Downloads'))):
        #add downloads shortcut
        sidebar.insert('','end',text='Downloads',image=downloads_icon);
    ##endif
    if (os.path.exists(os.path.join(os.path.expanduser('~'),'Music'))):
        #add music shortcut
        sidebar.insert('','end',text='Music',image=music_icon);
    ##endif
    if (os.path.exists(os.path.join(os.path.expanduser('~'),'Desktop'))):
        #add desktop shortcut
        sidebar.insert('','end',text='Desktop',image=desktop_icon);
    ##endif
    if (os.path.exists(os.path.join(os.path.expanduser('~'),'Python'))):
        #add python documents shortcut (if PyOS, which has this as a default folder)
        sidebar.insert('','end',text='Python',image=python_icon);
    ##endif
    #finished adding the shortcut folders..
    def doubleClick(event=None):
        # Get the selected item
        selected_item=sidebar.selection()[0];
        # Get the full path of the selected item
        if (selected_item==''):
            # If the selected item is empty, return
            return;
        elif (sidebar.item(selected_item)["text"]=="Home"):
            # If the selected item is the home shortcut, change the path to the home directory
            full_path=os.path.join(os.path.expanduser('~'));
        else:
            # Otherwise, get the full path of the selected item
            full_path=os.path.join(os.path.expanduser("~"),sidebar.item(selected_item)["text"]);
        ##endif

        if os.path.isdir(full_path):
            # If it's a folder, change the current path to the selected folder
            parent_path=os.path.split(current_path.get())[0];
            if full_path.endswith(".."):
                current_path.set(parent_path);
            else:
                current_path.set(full_path);
            ##endif
            pathChange();  # Update the treeview
        ##endif
    ##end
    sidebar.bind("<Double-1>",doubleClick);
##end
def main(argc,args):
    thepath=os.getcwd();
    if (len(args)>1):
        thepath=args[1];
    ##endif
    #If there isnt already a known file format config file, add one.
    if (not os.path.exists(thisdir+"/cfg/Files/fileformats.cfg")):
        if (not os.path.exists(thisdir+"/cfg/Files")):
            os.makedirs(os.path.join(thisdir+"/cfg/Files"));
        ##ed
        with open(thisdir+"/cfg/Files/fileformats.cfg", "wb") as f:
            KnownFormats={
                "Image":["PNG","JPG","JPEG","GIF","BMP","ICO","TIFF","WEBP","SVG","SVGZ"],
                "Audio":["MP3","WAV","OGG","AAC","WMA","FLAC","M4A","MP4"],
                "Video":["MOV","MP4","M4V","AVI","WMV","FLV","MKV","MK3D"],

                "Document":["PDF","TXT"],
                "Compressed":["ZIP","RAR","7Z","GZ","BZ2","XZ","TAR","GZIP"],
            };
            f.write(jsonEncode(KnownFormats).encode('utf-8'));
        ##endwith
    ##endif
    main=tk.Tk();
    main.title('Files');
    main.geometry('640x480');
    main.icon=icon=tk.PhotoImage('files_icon',master=main,file=thisdir+'/favicon.png');
    main.iconphoto(True,icon);
    s=ttk.Style(master=main);
    s.configure('Files.Treeview',rowheight=32);
    sidebar_relwidth=.2;
    sidebar_relheight=.9;
    file_relwidth=.8;
    file_relheight=.9;
    main.focus_force();
    current_path=tk.StringVar();
    current_path.set(thepath);  # Set initial path
    sidebar=ttk.Treeview(main,columns=("Name"),style='Files.Treeview');
    sidebar.heading("#0",text="Name",anchor="center");
    sidebar.column('Name',anchor=tk.W);
    sidebar.place(relx=0,rely=.1,relwidth=sidebar_relwidth,relheight=sidebar_relheight);
    file_tree=ttk.Treeview(main,columns=("Name","Type",),style='Files.Treeview');
    file_tree.heading("#0",text="Name");
    file_tree.heading("#1",text="Type");
    file_tree.column('Name',anchor=tk.W);
    file_tree.column('Type',anchor=tk.W);
    file_tree.place(relx=sidebar_relwidth,rely=.1,relwidth=file_relwidth,relheight=file_relheight);
    scroll=tk.Scrollbar(main,width=5,command=file_tree.yview);
    scroll.place(relx=1,rely=1,relheight=.8,anchor=tk.SE);
    scroll.update();
    file_tree.update();
    sidebar.update();
    file_tree.file_icon=file_icon=tk.PhotoImage(file=thisdir+"/assets/file_icon.png",master=main);
    file_tree.exe_icon=exe_icon=tk.PhotoImage(file=thisdir+"/assets/exe_icon.png",master=main);
    file_tree.exe_ext_icon=exe_ext_icon=tk.PhotoImage(file=thisdir+"/assets/exe_ext_icon.png",master=main);
    file_tree.folder_icon=folder_icon=tk.PhotoImage(file=thisdir+"/assets/folder_icon.png",master=main);
    file_tree.unknown_icon=unknown_icon=tk.PhotoImage(file=thisdir+"/assets/unknown_icon.png",master=main);
    file_tree.new_icon=new_icon=tk.PhotoImage(file=thisdir+"/assets/add_item_icon.png",master=main);
    file_tree.settings_icon=settings_icon=tk.PhotoImage(file=thisdir+"/assets/settings_icon.png",master=main);
    def format_check(path):
        KnownFormats=jsonDecodeF(open(thisdir+"/cfg/Files/fileformats.cfg","r"));
        # Search through the known file formats and update them accordingly.
        file_extension_regex=r"(?:\.)([A-Za-z0-9]+)$";
        format=None;
        for k in KnownFormats:
            matches=re.findall(file_extension_regex,path);
            filtered_matches=[match.replace(".", "") for match in matches]
            if (k=="Image"):
                if (filtered_matches and filtered_matches[0].upper() in KnownFormats["Image"]):
                    format=f"{filtered_matches[0].upper()} Image";
                    break;
                ##endif
            ##endif
            if (k=="Audio"):
                if (filtered_matches and filtered_matches[0].upper() in KnownFormats["Audio"]):
                    format=f"{filtered_matches[0].upper()} Audio";
                    break;
                ##endif
            ##endif
            if (k=="Video"):
                if (filtered_matches and filtered_matches[0].upper() in KnownFormats["Video"]):
                    format=f"{filtered_matches[0].upper()} Video";
                    break;
                ##endif
            ##endif
            if (k=="Document"):
                if (filtered_matches and filtered_matches[0].upper() in KnownFormats["Document"]):
                    format=f"{filtered_matches[0].upper()} Document";
                    break;
                ##endif
            ##endif
            if (k=="Compressed"):
                if (filtered_matches and filtered_matches[0].upper() in KnownFormats["Compressed"]):
                    format=f"{filtered_matches[0].upper()} Archive";
                    break;
                ##endif
            ##endif
        ##end
        if (format==None):
            matches=re.findall(file_extension_regex,path);
            filtered_matches=[match.replace(".", "") for match in matches]
            if (filtered_matches):
                format=f"{filtered_matches[0].upper()} File";
            else:
                format="File";
            ##endif
        ##endif
        return format;
    ##end
    def pathChange(event=None):
        # Get a list of files and folders in the current path
        try:
            directory=os.listdir(current_path.get());
            # Clear the treeview
            file_tree.delete(*file_tree.get_children());
            #create parent directory shortcut
            if (current_path.get()!="/"):
                file_tree.insert("", tk.END,text="..",image=folder_icon);
            ##endif
            # Insert each item into the treeview
            for item in directory:
                full_path=os.path.join(current_path.get(),item);
                if os.path.isfile(full_path):
                    if (not isExecutable(full_path)):
                        file_tree.insert("",tk.END,text=item,values=[format_check(full_path)],image=file_icon);
                    else:
                        if (full_path.endswith('.so') or endswithregex(full_path,'.so.[0-9]+$')):
                            file_tree.insert("",tk.END,text=item,values=['Shared Library (.so)'],image=exe_ext_icon);
                        else:
                            file_tree.insert("",tk.END,text=item,values=["Application"],image=exe_icon);
                        ##endif
                    ##endif
                elif os.path.isdir(full_path):
                    file_tree.insert("",tk.END,text=item,values=['-'],image=folder_icon);
                else:
                    file_tree.insert("",tk.END,text=item,values=['?'],image=unknown_icon);
                ##endif
            ##end
            scroll.update();
            file_tree.update();
            sidebar.update();
            main.update();
        except PermissionError as e:
            print("Error opening path: "+str(e));
            parent_path=os.path.split(current_path.get())[0];
            current_path.set(parent_path);
            err_popup("Error opening path","Permission Denied.");
            pathChange();
        ##endtry
    ##end
    check_for_default_folders(sidebar,pathChange,current_path);
    def linux_create_folder(path):
        file_creator=tk.Toplevel(main);
        file_creator.title('Create Folder');
        file_creator.geometry("100x100");
        # Calculate center coordinates
        x=main.winfo_x()+main.winfo_width()//2-file_creator.winfo_width()//2;
        y=main.winfo_y()+main.winfo_height()//2-file_creator.winfo_height()//2;
        # Set the Toplevel window's position
        file_creator.geometry(f"+{x}+{y}");
        name_ent=ttk.Entry(file_creator);
        name_ent.place(relx=.5,rely=.25,relwidth=1,relheight=.5,anchor="n");
        name_ent.focus_force();
        name_ent.insert(0,"New Folder");
        create_btn=tk.Button(file_creator,text='Create');
        create_btn.place(relx=.5,rely=.75,relwidth=.5,relheight=.25);
        cancel_btn=tk.Button(file_creator,text='Cancel');
        cancel_btn.place(relx=0,rely=.75,relwidth=.5,relheight=.25);
        def on_cancel():
            file_creator.destroy();
        ##end
        def on_create():
            new_path=path+"/"+name_ent.get();
            try:
                os.mkdir(new_path);
                pathChange(None);
            except Exception as err:
                return False;
            ##endtry
            file_creator.destroy();
        ##end
        file_creator.bind('<Return>',lambda event:on_create());
        file_creator.positionfrom('program');
        file_creator.bind('<Escape>',lambda event:on_cancel());
        create_btn.config(command=on_create);
        cancel_btn.config(command=on_cancel);
    ##end
    button_relwidth=sidebar_relwidth/3;
    new_item_btn=ttk.Button(main,text='New',image=new_icon);
    new_item_btn.place(relx=0,rely=0,relwidth=button_relwidth,relheight=1-sidebar_relheight);
    settings_icon=ttk.Button(main,text='',image=settings_icon);
    settings_icon.place(relx=button_relwidth,rely=0,relwidth=button_relwidth,relheight=1-sidebar_relheight);
    new_item_menubar=tk.Menu(main,cursor="");
    new_item_menubar.add_command(label='File');
    new_item_menubar.add_command(label='Folder',command=lambda:linux_create_folder(current_path.get()));
    def show_menu(event):
        new_item_menubar.tk_popup(event.x_root,event.y_root)
    ##end
    new_item_btn.bind('<Button-1>',show_menu);
    path_entry=tk.Entry(main,textvariable=current_path);
    path_entry.place(relx=sidebar_relwidth,rely=0,relwidth=file_relwidth,relheight=.1);
    path_entry.bind("<Return>",pathChange);  # Bind Enter key to pathChange()
    def doubleClick(event=None):
        # Get the selected item
        selected_item=file_tree.selection()[0];
        # Get the full path of the selected item
        full_path=os.path.join(current_path.get(),file_tree.item(selected_item)["text"]);

        # Check if the selected item is a file or folder
        if os.path.isfile(full_path):
            if (isExecutable(full_path)):
                execute_prog(full_path,[]);
            ##endif
            # If it's a file, and not a standard executable, open it in the default application (if there is one)
            print('Opening file:',full_path);
        elif os.path.isdir(full_path):
            # If it's a folder, change the current path to the selected folder
            parent_path=os.path.split(current_path.get())[0];
            if full_path.endswith(".."):
                current_path.set(parent_path);
            else:
                current_path.set(full_path);
            ##endif
            pathChange();  # Update the treeview
        ##endif
    ##end
    def on_configure(event):
        main.update();
        main.update_idletasks();
        if (main.winfo_width()>640):
            sidebar_relwidth=.15;
            file_relwidth=.85;
        else:
            sidebar_relwidth=.2;
            file_relwidth=.8;
        ##endif
        if (main.winfo_height()<480):
            sidebar_relheight=.9;
            file_relheight=.9;
        else:
            sidebar_relheight=.95;
            file_relheight=.95;
        ##endif
        button_relwidth=sidebar_relwidth/3;
        sidebar.place(relx=0,rely=1-sidebar_relheight,relwidth=sidebar_relwidth,relheight=sidebar_relheight);
        file_tree.place(relx=sidebar_relwidth,rely=1-file_relheight,relwidth=file_relwidth,relheight=file_relheight);
        scroll.place(relx=1,rely=1,relheight=file_relheight,anchor=tk.SE);
        path_entry.place(relx=sidebar_relwidth,rely=0,relwidth=file_relwidth,relheight=1-file_relheight);
        new_item_btn.place(relx=0,rely=0,relwidth=sidebar_relwidth,relheight=1-sidebar_relheight);
        new_item_btn.place(relx=0,rely=0,relwidth=button_relwidth,relheight=1-sidebar_relheight);
        settings_icon.place(relx=button_relwidth,rely=0,relwidth=button_relwidth,relheight=1-sidebar_relheight);
        settings_icon.update();
        new_item_btn.update();
        path_entry.update();
        file_tree.update();
        sidebar.update();
        if (new_item_btn.winfo_height()<32):
            pass;
        else:
            pass;
        ##endif
    ##end
    file_tree.bind("<Double-1>",doubleClick);
    main.bind('<Configure>',on_configure);
    # Update the list when the path changes
    pathChange();
    main.mainloop();
##end
time.sleep(.5);
if (imported==False):
    main(len(sys.argv),sys.argv);
##endif