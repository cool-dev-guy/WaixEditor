from PlayerWidget import PlayerWidget
from WaixToolBar import WaixToolBar
from TimeLineWidget import TIME_LINE_WIDGET_CONTAINER as Waix_TIME_LINE
from waix_cython import Waix_PROJECT_WIDGET
import waix_cython
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import ttk,messagebox,filedialog
class Waix(tk.Tk):
    def __init__(self,**k):
        # create window
        super().__init__()
        #from modules import settings
        self.option_add('*highlightThickness', 0)
        self.option_add('*highlightBackground', '#111')
        self.geometry("950x650")
        self.title('Waix')
        self.protocol("WM_DELETE_WINDOW", self.distroyAppWindow)

        self.onWinDistroy = False
    def createAppUI(self):
        self.configureAppUILayout()
        self.createAppUIMenu()

        self.AppUITOP = ttk.PanedWindow(self, orient='horizontal')
        self.AppUITOP.grid(column=0, row=0, sticky=tk.NSEW )

        self.AppUIMID = WaixToolBar(self,borderwidth=0,height=30)
        self.AppUIMID.grid(column=0, row=1, sticky=tk.NSEW)

        self.AppUIBOT = tk.Frame(self,borderwidth=0)
        self.AppUIBOT.grid(column=0, row=2, sticky=tk.NSEW )

        self.configureAppUILayoutSUB()
        
        self.AppUIVideoProjectWidget = Waix_PROJECT_WIDGET(self.AppUITOP)
        self.AppUIVideoPropsWidget = Waix_PROJECT_WIDGET(self.AppUITOP)
        #self.AppUIVideoPlayerWidgetContainer = tk.Frame(self.AppUITOP)
        self.AppUIVideoPlayerWidget = PlayerWidget(self,bg="#111")
        self.AppUITOP.add(self.AppUIVideoProjectWidget)
        self.AppUITOP.add(self.AppUIVideoPropsWidget)
        self.AppUITOP.add(self.AppUIVideoPlayerWidget)
        
        






        self.AppUITimelineWidget = Waix_TIME_LINE(self.AppUIBOT)
        self.AppUITimelineWidget.grid(column=0, row=0, sticky=tk.NSEW )


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
        self.rowconfigure(1,weight=0)
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
            self.onWinDistroy = True
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
    def init(self):
        self.update()
        self.AppUITimelineWidget.TIME_LINE_WIDGET.EditTracksContainer.addVideoTrack()
        self.AppUITimelineWidget.TIME_LINE_WIDGET.EditTracksContainer.PlayLine.make()

if __name__=="__main__":
    app = Waix()
    style = ttk.Style(app)
    style.theme_use('default')
    style.configure("TNotebook", background='#222',highlightThickness='0',border=0);
    #style.configure("TPanedWindow", background='#222',highlightThickness='0',border=0);
    style.map("TNotebook.Tab", background=[("selected", "#222")], foreground=[("selected", "#DDD")],border='0',highlightThickness='0');
    style.configure("TNotebook.Tab", background="#444", foreground="#DDD",highlightThickness='0',border=0);
    
    app.createAppUI()
    app.init()
    # app.AppUIVideoPlayerWidget.init()
    # file_path = app.triggerOpenDialog(type="Video")
    # app.AppUIVideoPlayerWidget.player_playVID(file_path)
    # print(style.theme_names())


    app.mainloop()
    
