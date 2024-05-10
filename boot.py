module_name="PyOS.MainExe"  # Specify the module name as a string
main=__import__(module_name,fromlist=["PyOS"]);
#EXTERN: load,init;

if __name__=='__main__':
    main.init();
    main.load();
##endif