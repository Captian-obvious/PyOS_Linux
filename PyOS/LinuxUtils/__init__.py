from .. import Filesystem as fs;
from .. import UI as uiw;
import json,math,os,time;
import threading as task;
import subprocess as runner;
from . import psutils as psutils;
import sys;
import ctypes as c;
from ctypes import CDLL as LoadLibrary;
import base64;
#create the library loader
sys.modules['psutil']=psutils;
thisdir=os.path.dirname(os.path.realpath(__file__));
#Load Linux Library
#lin=lib.LoadLibrary('./liblinux.so.2');
#Linux Kernel Utils.
def isExecutable(path):
    # Check if the file is executable (an ELF or PyExe)
    return os.access(path, os.X_OK);
##end
def get_pwd():
    return os.getcwd();
##end
def pwencode(s):
    obfesbytes=[];
    for i in range(len(s)):
        hashed=s[i]+i;
        rshifted=hashed>>4;
        obfesbytes.append(rshifted)
    ##end
    return base64.b64encode(bytes(obfesbytes));
##end
def usrnencode(s):
    obfesbytes=bytearray();
    key=4;
    for i in range(len(s)):
        hashed=s[i]+(i+key);
        obfesbytes.append(hashed);
    ##end
    return base64.b64encode(obfesbytes);
##end
def usrndecode(b64):
    obfesbytes=base64.b64decode(b64.encode('ascii'));
    origbytes=bytearray();
    key=4;
    for i in range(len(obfesbytes)):
        orig=obfesbytes[i]-(i+key);
        origbytes.append(orig);
    ##end
    return bytes(origbytes);
##end
def sys_run(cmd):
    return runner.run(cmd,shell=True,capture_output=True);
##end
def sys_read(path):
    exists=os.access(path,os.R_OK);
    if (exists==True):
        f=open(path,'rb');
        bytes=f.read();
        f.close();
        return bytes;
    ##endif
##end
def sys_write(path,data:bytearray|bytes):
    exists=os.access(path,os.W_OK);
    if (exists==True):
        f=open(path,'wb');
        f.write(data);
        f.close();
        return True;
    else:
        return False;
    ##endif
##end
def hostname():
    with open('/etc/hostname','r') as f:
        hn=f.read();
        f.close();
        return hn.strip();
    ##endwith
##end
def parse_desktop_file(file_path):
    data={};
    with open(file_path,"r") as f:
        for line in f:
            line=line.strip();
            if "=" in line:
                key,value=line.split("=", 1);
                data[key.strip()]=value.strip();
            ##endif
        ##end
    ##endwith
    return data;
##end
def create_desktop_file(data,file_path):
    with open(file_path, "w") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n");
        ##end
    ##endwith
##end
def populate_dash(add_icon=None):
    sys_dash_path='/usr/share/applications';
    usr_dash_path='~/.local/share/applications';
    found={};
    if (os.path.exists(sys_dash_path)==False):
        return;
    else:
        for i in os.listdir(sys_dash_path):
            if (i.endswith('.desktop')):
                iconData={};
                desktop_file_path=os.path.join(sys_dash_path,i);
                data=parse_desktop_file(desktop_file_path);
                if ('Exec' in data):
                    iconData['command']=data['Exec'];
                else:
                    iconData['command']='';
                ##endif
                if ('Icon' in data):
                    iconData['icon']=data['Icon'];
                else:
                    iconData['icon']=None;
                ##endif
                if ('Name' in data):
                    iconData['name']=data['Name'];
                else:
                    iconData['name']=i.split('.')[0];
                ##endif
                if (add_icon):
                    add_icon(iconData['name'],iconData['icon'],iconData['command']);
                ##endif
                found[iconData['name']]=iconData;
            ##endif
        ##end
    ##endif
    if (os.path.exists(usr_dash_path)==False):
        return;
    else:
        for i in os.listdir(sys_dash_path):
            if (i.endswith('.desktop')):
                iconData={};
                desktop_file_path=os.path.join(sys_dash_path,i);
                data=parse_desktop_file(desktop_file_path);
                if ('Exec' in data):
                    iconData['command']=data['Exec'];
                else:
                    iconData['command']='';
                ##endif
                if ('Icon' in data):
                    iconData['icon']=data['Icon'];
                else:
                    iconData['icon']=None;
                ##endif
                if ('Name' in data):
                    iconData['name']=data['Name'];
                else:
                    iconData['name']=i.split('.')[0];
                ##endif
                if (add_icon):
                    add_icon(iconData['name'],iconData['icon'],iconData['command']);
                ##endif
                found[iconData['name']]=iconData;
            ##endif
        ##end
    ##endif
##end
def get_window_title_by_pid(pid):
    try:
        process=psutils.Process(pid);
        window_title=process.name();  # Get the process name (executable)
        return window_title;
    except psutils.NoSuchProcess:
        return None;
    ##endtry
##end
def get_pid_by_name(process_name):
    pid=None;
    for proc in psutils.process_iter(attrs=['pid','name']):
        if proc.exe==process_name:
            pid=proc.pid;
            break;
        ##endif
    ##end
    return pid;
##end
def focus_process(pid):
    import pywinctl;
    if (not pid):
        return;
    ##endif
    try:
        title=None;
        if (pid==-1):
            title=pywinctl.getActiveWindowTitle();
        else:
            title=get_window_title_by_pid(pid);
        ##endif
        if (title):
            pywinctl.getWindowsWithTitle(title)[0].activate();
        ##endif
    except Exception as e:
        print(e);
    ##endtry
##end
def is_live_boot():
    #Check if the system is booted live (aka configs are missing)
    if (os.path.exists('PyOS/cfg/main.pycfg')):
        return False;
    else:
        return True;
    ##end
##end
def restart():
    #Restart the system (is only used when actually installed on a home system, otherwise serversafe mode is used.
    #This is a bit of a hack, but it works.)
    global main,msg,count;
    #if not serversaafe run reboot.
    powercfg=read_cfg('PyOS/cfg/power.pycfg');
    if (powercfg['safemode']!=True):
        runner.run('reboot',shell=True);
    else:
        #__NOT YET FULLY IMPLEMENTED__
        time.sleep(13);
        os.system('python boot.pyw');
        quit();
    ##endif
##end
def mkhome(username):
    #creates home directory of username (ofc onlt when in non-serversafe mode)
    powercfg=read_cfg('PyOS/cfg/power.pycfg');
    try:
        if jsonDecode(powercfg):
            powercfg=jsonDecode(powercfg);
            if (powercfg['safemode']!=True):
                runner.run(f'mkhomedir_helper {username}');
            else:
                return;
            ##endif
        ##endif
    except Exception as e:
        print(powercfg);
        #if (powercfg['safemode']!=True):
        #    runner.run(f'mkhomedir_helper {username}');
        #else:
        #    return;
        ###endif
    ##endtry
##end
def shutdown():
    #Shutdown the system (is only used when actually installed on a home system, otherwise serversafe mode is used.
    #This is a bit of a hack, but it works.)
    global main,msg,count;
    #if not serversaafe run reboot.
    powercfg=read_cfg('PyOS/cfg/power.pycfg');
    if (powercfg['safemode']!=True):
        runner.run('shutdown -h now',shell=True);
    else:
        #__NOT YET FULLY IMPLEMENTED__
        pass;
    ##endif
##end
def get_root_dir():
    return os.path.split(os.path.realpath(__file__))[0];
##end
def jsonEncode(data):
    return json.dumps(data);
##end
def jsonDecode(data):
    return json.loads(data);
##end
def run_command(cmd):
    return runner.run(cmd,shell=True);
##end
def sys_listdir(path):
    return os.listdir(path);
##end
def sys_listdir_items(path):
    items={};
    for k in os.listdir(path):
        item=os.path.join(path,k);
        if (os.path.isdir(item)):
            items[k]=("Folder",k);
        elif (os.path.isfile(item)):
            items[k]=("File",k);
        ##endif
    ##end
    return items;
##end
def execute_prog(path,args):
    runner.call([path]);
##end
def root_exec_path():
    config=read_cfg('PyOS/cfg/main.pycfg');
    return config['system_path'];
##end
def get_file_size(path):
    return os.path.getsize(path);
##end
def write_cfg(path,dictionary):
    MAGIC_HEADER=b'<PyCfg!\x00\x00\x00\x00';
    SIGNATURE=b'PyOS\x00\x00\x01';
    MAGIC_FOOTER=b'\x00\x00\x00\x00/PyCfg!>';
    data=jsonEncode(dictionary).encode('utf-8');
    fSize=int(len(data));
    f=open(path,'wb');
    f.write(MAGIC_HEADER);
    f.write(fSize.to_bytes(4,byteorder='little'));
    f.write(SIGNATURE);
    f.write(data);
    f.write(MAGIC_FOOTER);
##end
def read_cfg(path):
    MAGIC_HEADER=b'<PyCfg!\x00\x00\x00\x00';
    SIGNATURE=b'PyOS\x00\x00\x01';
    MAGIC_FOOTER=b'\x00\x00\x00\x00/PyCfg!>';
    f=open(path,'rb');
    header=f.read(len(MAGIC_HEADER));
    if (header!=MAGIC_HEADER):
        print("File is not a PyCFG File! Header does not match!");
        return None;
    ##endif
    fSize=int.from_bytes(f.read(4),byteorder='little');
    signature=f.read(len(SIGNATURE));
    if (signature!=SIGNATURE):
        print("File is not a PyCFG File! Signature does not match!");
        return None;
    ##endif
    data=f.read(fSize);
    footer=f.read(len(MAGIC_FOOTER));
    if (footer!=MAGIC_FOOTER):
        print("File is not a PyCFG File! Footer does not match!");
        return None;
    ##endif
    return jsonDecode(data.decode('utf-8'));
##end
