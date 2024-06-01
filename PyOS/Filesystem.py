from . import libCommon as common;
from . import LinuxUtils as linux;

def init():
    pass;
##end

def get_file(path:str):
    return linux.get_pwd()+"/"+path;
##end

def path_exists(path:str):
    return linux.os.path.exists(path);
##end

def write_file(path:str,data:bytearray):
    try:
        f=open(path,'wb');
        f.write(data);
        return f;
    except Exception as e:
        print(e);
        return None;
    ##endtry
##end

def disk_scan(onprogress=None,oncount=None):
    rootdir='/';
    if (rootdir==None):
        return False;
    else:
        #This will begin a full disk scan once ran, if any part of it fails, it calls panic.
        #*this could take a while*
        results={
            "ScannedFiles":[],
            "ScannedDirs":[],
            "FileCount":0,
            "ErrorCount":0,
        };
        curCount=0;
        finalCount=0;
        for root,dirs,files in linux.os.walk(rootdir):
            for name in files:
                path=root+'/'+name;
                if (path_exists(path)):
                    curCount+=1;
                else:
                    results["ErrorCount"]+=1;
                ##endif
                if oncount: oncount(curCount);
                ##endif
                if (curCount<1000):
                    linux.time.sleep(.0005);
                ##endif
            ##end
        ##end
        for root,dirs,files in linux.os.walk(rootdir):
            ##endif
            for name in files:
                if (onprogress):onprogress(linux.math.floor((finalCount/curCount)*100));
                ##endif
                finalCount+=1;
                if (name!='smartscan.log' and name!='PyOS.py'):
                    path=root+'/'+name;
                    if (path_exists(path)):
                        results['ScannedFiles'].append({
                            "Path":path,
                            "FileName":name,
                            "Size":linux.os.path.getsize(path),
                            "IsDir":False,
                        });
                    else:
                        return False;
                    ##endif
                ##endif
            ##end
            for name in dirs:
                path=root+'/'+name;
                if (path_exists(path)):
                    results['ScannedDirs'].append({
                        "Path":path,
                        "Name":name,
                        "IsDir":True,
                    });
                else:
                    return False;
                ##endif
            ##end
            #gets around more race conditions.
            if (curCount>500):
                linux.time.sleep(.005);
            else:
                linux.time.sleep(.05);
            ##endif
        ##end
        results['FileCount']=finalCount;
        #logfile=open(linux.get_pwd()+'/PyOS/smartscan.log','w');
        #logfile.write(linux.jsonEncode(results));
        #logfile.close();
        return True;
    ##endif
##end