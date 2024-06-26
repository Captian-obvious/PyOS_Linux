import PyOS.MainExe as main;
import plymouth_boot as ply;
#EXTERN: load,init;
if __name__=='__main__':
    main.init();
    main.load();
##endif
