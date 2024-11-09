from typing import Optional;
from . import LinuxUtils as linux;
psutil=linux.psutils;

class Battery_Utils:
    def __init__(self):
        pass;
    ##end
    def get_battery_level(self):
        battery=psutil.sensors_battery();
        return battery.percent;
    ##end
    def get_battery_status(self):
        battery=psutil.sensors_battery();
        return battery.power_plugged;
    ##end
    def get_battery_info(self):
        battery=psutil.sensors_battery();
        return battery.info;
    ##end
##end

class Network_Utils:
    def __init__(self):
        pass;
    ##end
    def get_connection_status(self):
        return psutil.net_if_addrs();
    ##end
    def get_ip_address(self):
        return psutil.net_if_addrs()['lo'][0].address;
    ##end
    def get_connections(self,type='inet'):
        return psutil.net_connections(kind=type);
    ##end
    def get_available_networks(self):
            addresses=psutil.net_if_addrs()
            stats=psutil.net_if_stats()
            available_networks=[]

            for interface, addr_list in addresses.items():
                # Skip interfaces with link-local addresses (usually 169.254.x.x)
                if any(getattr(addr, 'address').startswith("169.254") for addr in addr_list):
                    continue
                # Check if the interface is up
                elif interface in stats and getattr(stats[interface], "isup"):
                    available_networks.append(interface)
                ##endif
            ##endif
            return available_networks;
        ##end
    ##end
##end

class Disk_Utils:
    def __init__(self):
        pass;
    ##end
    def get_disk_usage(self,path):
        return psutil.disk_usage(path);
    ##end
    def get_disk_info(self):
        return psutil.disk_partitions();
    ##end
##end

class Memory_Utils:
    def __init__(self):
        pass;
    ##end
    def get_memory_info(self):
        return psutil.virtual_memory();
    ##end
    def get_memory_usage(self):
        return psutil.virtual_memory().percent;
    ##end
##end

class CPU_Utils:
    def __init__(self):
        pass;
    ##end
    def get_cpu_info(self):
        return psutil.cpu_stats();
    ##end
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1);
    ##end
##end

class System_Event_Utils:
    def __init__(self,canvas):
        self.canvas=canvas;
        self.click_handler=None;
        self.keypress_handler=None;
    ##end
    def register_event(self,event_name=None,event_function=None):
        if (event_name=='onclick' or event_name=='click'):
            self.click_handler=self.bindFn(event_function);
            self.canvas.bind('<Button-1>',self.onclick_event);
        elif (event_name=='onkeypress' or event_name=='keypress'):
            self.keypress_handler=self.bindFn(event_function);
        ##endif
    ##end
    def bindFn(self,func,*args,**kwargs):
        def nfn(*args2,**kwargs2):
            return func(*args,*args2,**kwargs,**kwargs2);
        ##end
        return nfn;
    ##end
    def onclick_event(self,event):
        mouseX=event.x;
        mouseY=event.y;
        item=self.canvas.find_closest(mouseX, mouseY);
        if item:
            tags=self.canvas.gettags(item);
            if (tags=='clickable' or tags=='clickable_text'):
                print('clicked item: '+str(item));
                if self.click_handler:self.click_handler(item);
                ##endif
            ##endif
        ##endif
    ##end
    def onkeypress_event(self,event):
        if self.keypress_handler:self.keypress_handler(event);
    ##end
##end

class PyOS_Utils:
    def __init__(self):
        pass;
    ##end
    class wifi_icon:
        def __init__(self,canvas,x,y,width=32,height=32):
            self.canvas=canvas;
            self.x=x;
            self.y=y;
            self.width=width;
            self.height=height;
            self.id0=None;
            self.id1=None;
            self.id2=None;
            self.id3=None;
        ##end
        def draw(self,signal_percent:Optional[int]=None):
            if signal_percent:
                if signal_percent>100:signal_percent=100;
                ##endif
                if signal_percent<0:signal_percent=0;
                ##endif
            else:
                signal_percent=100;
            ##endif
            if (self.id0):
                self.canvas.delete(self.id0);
            ##endif
            if (self.id1):
                self.canvas.delete(self.id1);
            ##endif
            if (self.id2):
                self.canvas.delete(self.id2);
            ##endif
            if (self.id3):
                self.canvas.delete(self.id3);
            ##endif
            self.id0=self.canvas.create_oval(self.x-self.width*.15,self.y-self.height*.15,self.x,self.y,fill='white',outline='white');
            self.id1=self.canvas.create_arc(self.x-self.width*.50,self.y-self.height*.50,self.x,self.y,start=90,extent=90,outline='white' if signal_percent>25 else 'gray',style='arc',width=self.width*.08);
            self.id2=self.canvas.create_arc(self.x-self.width*.75,self.y-self.height*.75,self.x,self.y,start=90,extent=90,outline='white' if signal_percent>50 else 'gray',style='arc',width=self.width*.08);
            self.id3=self.canvas.create_arc(self.x-self.width,self.y-self.height,self.x,self.y,start=90,extent=90,outline='white' if signal_percent>80 else 'gray',style='arc',width=self.width*.08);
            self.canvas.moveto(self.id1,self.x-(self.width*.37),self.y-(self.height*.37));
            self.canvas.moveto(self.id2,self.x-(self.width*.55),self.y-(self.height*.55));
            self.canvas.moveto(self.id3,self.x-(self.width*.74),self.y-(self.height*.74));
        ##end
    ##end
    class battery_icon:
        def __init__(self,canvas,x,y,width=16,height=32):
            self.canvas=canvas;
            self.x=x;
            self.y=y;
            self.width=width;
            self.height=height;
            self.id0=None;
        ##end
        def draw(self,percent:Optional[int]=None):
            if percent:
                if percent>100: percent=100;
                ##endif
                if percent<0: percent=0;
                ##endif
            ##enduf
        ##end
    ##end
##end