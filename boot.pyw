import os,subprocess,time;
module_name="PyOS.MainExe"  # Specify the module name as a string
main=__import__(module_name,fromlist=["PyOS"]);
if os.path.exists('./splash'):
    if os.name=="nt":
        subprocess.run(['splash','--mode=boot']);
    else:
        subprocess.run(['./splash','--mode=boot']);
    ##endif
else:
    if os.name=="nt":
        subprocess.run(['pythonw','plymouth_boot.pyw','--mode=boot']);
    else:
        subprocess.run(['./plymouth_boot.pyw','--mode=boot']);
    ##endif
##endif
#EXTERN: load,init;
if __name__=='__main__':
    main.init();
    main.load();
##endif