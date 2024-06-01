def add_icon(self,app_name,icon_path,application=None):
    icon_image=ui.PhotoImage(file=icon_path);
    id=len(self.icons);
    self.update();
    # Calculate row and column
    row=id//self.columns;
    column=id%self.columns;
    x1=self.icon_padding+(self.columns-column)*self.icon_size;
    y1=48+self.icon_padding+row*self.icon_size;
    x2=x1+self.icon_size;
    y2=y1+self.icon_size;
    background=self.create_rectangle(x1,y1,x2,y2,fill="#333",outline="#333");
    # Create an image widget with the icon
    icon_widget=self.create_image(self.icon_padding+(self.columns-column)*self.icon_size+48,self.icon_padding+48+row*self.icon_size+48,image=icon_image,anchor=ui.CENTER);

    # Create a text label for the icon name
    name_widget=self.create_text(self.icon_padding+(self.columns-column)*self.icon_size+48,self.icon_padding+32+row*self.icon_size+self.icon_size,text=app_name,anchor=ui.N,fill="#fff",font=("Ubuntu",8));