import tkinter as tk;
import time;
import os;

class BootupSpinner(tk.Canvas):
    def __init__(self,root,canvas_size=200,animation_length=2.0,arc_width=6,arc_color='blue',bg_color='white',arc_extent=75):
        super().__init__(root, width=canvas_size, height=canvas_size, bg=bg_color, highlightbackground=bg_color);
        self.root=root;
        self.frame_num=0;
        self.canvas_size=canvas_size;
        self.arc_color=(arc_color,) if isinstance(arc_color, str) else arc_color;
        self.bg_color=bg_color;
        self.arc_duration=animation_length / len(self.arc_color);
        self.start_angle=0;
        self.start_angle2=180;
        self.arc_width=arc_width;
        self.extent1=arc_extent;
        self.extent=0;
        self.elapsed=0;
        self.stopped=False;
        self.draw_arc();
    ##end
    def ease_quad_in_out(self,t):
        return 2*t*t if t < 0.5 else -1+(4 - 2*t)*t;
    ##end
    def interpolate_color(self,start_color,end_color,t,interpolate_start=0.95):
        if t < interpolate_start:
            return start_color;
        else:
            t=(t - interpolate_start) / (1 - interpolate_start);
            start_r,start_g,start_b=self.winfo_rgb(start_color);
            end_r, end_g, end_b=self.winfo_rgb(end_color);
            new_r=int(start_r+(end_r - start_r)*t);
            new_g=int(start_g+(end_g - start_g)*t);
            new_b=int(start_b+(end_b - start_b)*t);
            return f'#{new_r:04x}{new_g:04x}{new_b:04x}';
        ##endif
    ##end
    def draw_arc(self):
        self.frame_num+=1;
        self.elapsed+=50;
        num_colors=len(self.arc_color);
        self.delete("arc"+str(self.frame_num - 1));
        current_time=time.time();
        t=(current_time%self.arc_duration) / self.arc_duration;
        eased_t=self.ease_quad_in_out(t);
        self.extent=eased_t*360;
        self.start_angle=(current_time*(360 / self.arc_duration))*1.35%360;
        self.start_angle2=(self.start_angle+180)%360;
        span=self.arc_duration;
        index=int(current_time//span)%num_colors;
        next_index=(index+1)%num_colors;
        local_t=(current_time%span)/span;
        interpolated_color=self.interpolate_color(self.arc_color[index],self.arc_color[next_index],local_t);
        self.create_arc(self.canvas_size*0.2,self.canvas_size*0.2,self.canvas_size*0.8,self.canvas_size*0.8,start=self.start_angle,extent=self.extent1,outline=interpolated_color,width=self.arc_width,style="arc",tags="arc"+str(self.frame_num));
        self.create_arc(self.canvas_size*0.2,self.canvas_size*0.2,self.canvas_size*0.8,self.canvas_size*0.8,start=self.start_angle2,extent=self.extent1,outline=interpolated_color,width=self.arc_width,style="arc",tags="arc"+str(self.frame_num));
        if not self.stopped:
            self.root.after(50, self.draw_arc);
        else:
            self.delete("all");
        ##endif
    ##end
    def stop(self):
        self.stopped=True;
    ##end
##end
def onrun():
    main=tk.Tk();
    main.config(bg='#333');
    main.attributes('-fullscreen',True);
    main.attributes('-topmost',0);
    LoadMsg=tk.Label(main,text='...',font=('Ubuntu',20),fg='#fff',bg='#333',height=1);
    LoadMsg.place(relx=.5,rely=1,relwidth=1,anchor=tk.S);
    #oldlen=5.2;
    #oldsize=96;
    BootSpinner=BootupSpinner(main,canvas_size=96,animation_length=3.2,arc_width=6,arc_color=("#fff","#fff"),bg_color="#333");
    BootSpinner.place(relx=.5,rely=.9,anchor=tk.S);
    main.update(); #fixes the window size values for future use
    main.attributes('-topmost',0);
    main.bootIcon=icon=tk.PhotoImage(master=main,file='PyOS/assets/BootLogo.png');
    LoadImg=tk.Label(main,text='',font=('Ubuntu',20),fg='#fff',bg='#333',height='128px',width='128px',image=icon);
    LoadImg.place(relx=.5,rely=.5,anchor=tk.CENTER);
    main.update();
    # count=0;
    # for i in range(0,30):
    #     count+=1;
    #     if (count>3):
    #         count=0;
    #     ##endif
    #     ct='.'*count;
    #     LoadMsg.setText(f'{ct}Loading{ct}');
    #     main.update();
    #     linux.time.sleep(.35);
    # ##end
    count=0;
    load_time=time.time();
    start_time=time.time();
    update_time=start_time;
    total_updates=0;  # Keep track of the number of .35-second updates
    boot_time=0;
    expected_boot_time=13.3; #time in seconds boot is suppose to take.
    expected_boot_time_old=10.5;
    while boot_time<expected_boot_time:  # Run for 30 updates
        current_time=time.time();
        boot_time=current_time-start_time;
        # Update the main every 50 milliseconds
        if (current_time - update_time) >= 0.05:
            main.update()
            update_time=current_time;
        ##endif
        if (current_time - load_time) >= 0.35:
            count+=1;
            if count > 3:
                count=0;
            ##endif
            ct='.'*count;
            LoadMsg.config(text=f'{ct}Loading{ct}');
            load_time=current_time;
            total_updates+=1;
        ##endif
        # Add a small delay to avoid busy-waiting
        time.sleep(0.01);
    ##end
    BootSpinner.stop();
    main.update();
    try:
        bootlog=open('/etc/bootlog','w+');
        bootlog.write(f'boot_time={boot_time}');
        bootlog.close();
    except Exception as e:
        print('failed to write boot log, no changes were made to "/etc/bootlog"');
    ##endtry
    time.sleep(1);
    LoadImg.destroy();
    LoadMsg.destroy();
    main.destroy();
##end
onrun()
