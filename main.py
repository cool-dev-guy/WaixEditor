# import necessary dependencies
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import cv2
from PIL import Image, ImageTk

class Waix_PROJECT_WIDGET(ttk.Notebook):
    def __init__(self,inherited_parrent_self):
        super().__init__(inherited_parrent_self)
        notebook = self
        self.main = inherited_parrent_self
        # Create some tabs
        tab1 = tk.Frame(notebook, width=200, height=200, background='red')
        tab2 = tk.Frame(notebook, width=200, height=200, background='green')
        tab3 = tk.Frame(notebook, width=200, height=200, background='blue')

        # Add the tabs to the notebook
        notebook.add(tab1, text="Tab 1")
        notebook.add(tab2, text="Tab 2")
        notebook.add(tab3, text="Tab 3")

class Waix_VIDEO_PLAYER(tk.Canvas):
    def __init__(self,inherited_parrent_self,inherited_ancestor_self,pos= tk.CENTER):
        super(Waix_VIDEO_PLAYER,self).__init__(inherited_parrent_self)
        self.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        self.config(height=300,width=200)
        self.main = inherited_ancestor_self
        self.player_loadedVID = ""
        self.option_add('*highlightThickness', 0)
        self.option_add('*highlightBackground', 'white')
    def player_playVID(self,file):
        self.player_loadedVID = cv2.VideoCapture(file)
        while True:
            if self.main.onWinDistroyTrue:
                break
            ret, frame = self.player_loadedVID.read()
            if not ret:
                break
            self.width, self.height = int(self.player_loadedVID.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.player_loadedVID.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.ratio = self.height / self.width
            print(self.ratio)
            
            self.new_height = self.winfo_height()

            self.new_width = int(self.new_height /self.ratio)
            self.player_currentIMG_RAW = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.player_currentIMG = Image.fromarray(self.player_currentIMG_RAW)
            self.player_currentIMG = self.player_currentIMG.resize((self.new_width,self.winfo_height()), Image.LANCZOS)
            

    
            self.player_currentIMG_INSTANCE = ImageTk.PhotoImage(image=self.player_currentIMG)
            self.create_image(0, 0, image=self.player_currentIMG_INSTANCE, anchor=tk.NW)
            self.update()
            
        self.player_loadedVID.release()
    def player_sizer(self):
        pass
class TrackBox:
    def __init__(self,parrent,posx,posy):
        self.track = parrent.canvas.create_rectangle(parrent.timex+10,parrent.timey+10,100,60)
        
        self.track2 = parrent.canvas.create_rectangle(parrent.timex+50,60,500,100)
class Waix_TIME_LINE(tk.Frame):
    def __init__(self,inherited_parrent_self):
        super(Waix_TIME_LINE,self).__init__(inherited_parrent_self)
        self.main = inherited_parrent_self
        self.option_add('*Frame.highlightThickness', 0)
        self.option_add('*Frame.highlightBackground', 'white')
        self.timex = 0
        self.timey = 0
        self.t = 0
        print(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.update()
        self.timeline = tk.Frame(self)
        self.timeline.grid(row=0, column=0, sticky="NSEW")

        self.timeline.columnconfigure(0, weight=1)
        self.timeline.columnconfigure(1, weight=2)
        self.timeline.rowconfigure(0, weight=1)
        self.timeline.rowconfigure(1)

        self.timeline.track = tk.Frame(self.timeline)
        self.timeline.track.grid(row=0, column=0, sticky="NSEW")
        self.timeline.track.configure(bg='#666')

        self.canvas = tk.Canvas(self.timeline,borderwidth=0,highlightthickness=0)
        self.canvas.grid(column=1,row=0,sticky="NSEW")
        self.canvas.configure(bg='#333')

        self.timeline.scale = tk.Scale(self.timeline, from_=0, to=500, orient=tk.HORIZONTAL, sliderlength=100, showvalue=False)
        self.timeline.scale.bind("<Motion>", self.txr)
        #self.timeline.scale.bind("<Button>", self.play)
        self.timeline.scale.grid(row=1, column=1,columnspan=1, sticky="NSEW")

        self.line = self.canvas.create_line(0, 0, 0, self.winfo_height())
        self.t1 = TrackBox(self,self.timex+10,self.timey+10)
        #self.t2 = TrackBox(self,0,50)
    def on_resize(self,e):
        self.update()
    def txr(self,e):
        if e.state != 0:
            #print(e.x)
            print(self.timeline.scale.get())
            self.timex = -(self.timeline.scale.get())
            print(self.timex)
            self.test()
    def play(self,e):
        self.t += 1
        self.canvas.coords(self.line, self.t, 0,self.t,self.winfo_height())
        self.after(10, self.play)
    def test(self):
        self.canvas.moveto(self.t1.track, self.timex+10, self.timey+10)
        self.canvas.moveto(self.t1.track2, self.timex+50, 60)


class Waix(tk.Tk):
    def __init__(self,**k):
        # create window
        super().__init__()
        from modules import settings
        self.option_add('*highlightThickness', 0)
        self.option_add('*highlightBackground', 'white')
        self.geometry("950x650")
        self.title('Waix')
        self.protocol("WM_DELETE_WINDOW", self.distroyAppWindow)

        self.onWinDistroyTrue = False
    def createAppUI(self):
        self.configureAppUILayout()
        self.createAppUIMenu()

        self.AppUITOP = ttk.PanedWindow(self, orient='horizontal')
        self.AppUITOP.grid(column=0, row=0, sticky=tk.NSEW )

        self.AppUIMID = tk.Frame(self,borderwidth=0)
        self.AppUIMID.grid(column=0, row=1, sticky=tk.NSEW )

        self.AppUIBOT = tk.Frame(self,borderwidth=0)
        self.AppUIBOT.grid(column=0, row=2, sticky=tk.NSEW )

        self.configureAppUILayoutSUB()
        
        self.AppUIVideoProjectWidget = Waix_PROJECT_WIDGET(self.AppUITOP)
        self.AppUIVideoPropsWidget = Waix_PROJECT_WIDGET(self.AppUITOP)
        self.AppUIVideoPlayerWidgetContainer = tk.Frame(self.AppUITOP)
        self.AppUIVideoPlayerWidget = Waix_VIDEO_PLAYER(self.AppUIVideoPlayerWidgetContainer,self)
        self.AppUITOP.add(self.AppUIVideoProjectWidget)
        self.AppUITOP.add(self.AppUIVideoPlayerWidgetContainer)
        self.AppUITOP.add(self.AppUIVideoPropsWidget)






        self.AppUITimelineWidget = Waix_TIME_LINE(self.AppUIBOT)
        self.AppUITimelineWidget.grid(column=0, row=0, sticky=tk.NSEW )

        file_path = self.triggerOpenDialog(type="Video")
        self.AppUIVideoPlayerWidget.player_playVID(file_path)
    def createAppUIMenu(self):
        self.menubar = tk.Menu(self, bg="#333", fg="#fff", font=('Segoe UI', 9), borderwidth=0)
        self.file_menu = tk.Menu(self.menubar, tearoff=0, background='#444', foreground='white', font=('Segoe UI', 9), borderwidth=0)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Exit", command=self.distroyAppWindow)

        self.project_menu = tk.Menu(self.menubar, tearoff=0, background='#444', foreground='white', font=('Segoe UI', 9), borderwidth=0)
        self.project_menu.add_command(label="Add Project Files")
        self.project_menu.add_command(label="Add Custom Image")
        self.project_menu.add_command(label="Project Settings")

        self.edit_menu = tk.Menu(self.menubar, tearoff=0, background='#444', foreground='white', font=('Segoe UI', 9), borderwidth=0)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")
        self.edit_menu.add_command(label="Preferences")
        
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="File", menu=self.edit_menu)
        self.menubar.add_cascade(label="Project", menu=self.project_menu)
        self.config(menu=self.menubar)

    def configureAppUILayout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1)
        self.rowconfigure(2, weight=1)
    def configureAppUILayoutSUB(self):
        # TOP

        # MID
        self.AppUIMID.columnconfigure(0, weight=1)
        self.AppUIMID.columnconfigure(1, weight=1)
        self.AppUIMID.columnconfigure(2, weight=1)
        self.AppUIMID.rowconfigure(0, weight=1)
        # BOT
        self.AppUIBOT.rowconfigure(0,weight=1)
        self.AppUIBOT.columnconfigure(0, weight=1)
    def distroyAppWindow(self):
        print("Going to close")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.onWinDistroyTrue = True
            self.destroy()
    def triggerNewProjectDialog(self):
        pass
    def triggerOpenDialog(self,type):
        self.path = filedialog.askopenfilename(
            defaultextension=".mp4",
            filetypes=[("Videos", "*.mp4"), ("All Files", "*.*")],
            # initialdir="~/Documents",
            # initialfile="my_file.txt",
            title=f"Open {type}"
        )
        return self.path


if __name__=="__main__":
    app = Waix()
    style = ttk.Style(app)
    style.theme_use('clam')
    app.createAppUI()

    print(style.theme_names())


    app.mainloop()
    
