from os.path import exists
from . import UI as uiw;
from . import Filesystem as fs;
from . import LinuxUtils as linux;
from . import Pointer as pt;
from . import libCommon as com;
from . import MainExe as lib_main;
from . import Desktop as desk;
ui=uiw.UI();

def main(argc:int,argv:list[str]):
    window=ui.Window();
    window.wm_attributes('-type','splash');
    window.geometry('128x32');
##end