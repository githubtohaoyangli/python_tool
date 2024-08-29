import shutil
import os
import getpass
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import sv_ttk
import threading
import time
#"/Users/liexe/Library/CloudStorage/OneDrive-microsoft/Desktop/DEV/python3/python-tool/debug/python/Mac/VERSION/Ver. 1.x/1.1.0/time.py"正在替代 stdlib 模块"time"
#delecting
def get_time():
    t = time.localtime(time.time())
    y=time.asctime(t)
    return y
def forget1(a):
    if a==1:
        button.grid()
    else:
        button.grid_forget()
def forget2():
    u_button.grid_forget()
r=get_time()
def update():
    forget2()
    forget1(2)
    def update_thread():
        
        
        download_pb["value"] = 0
        download_pb["maximum"] = 100
        user = getpass.getuser()
        try:
            os.mkdir(f"/Users/{user}/pt_saved/logs")
        except FileExistsError:
            pass
        download_pb["value"] +=20
        time.sleep(0.11)
        try:
            shutil.rmtree("/Applications/python_tool.app")
            with open(f"/Users/{user}/pt_saved/logs/{r}.log", "a", encoding="utf-8") as a:
                a.write(f"[{get_time()}]  successfully delected old python_tool!\n")
        except FileNotFoundError:
            with open(f"/Users/{user}/pt_saved/logs/{r}.log", "a", encoding="utf-8") as c:
                c.write(f"[{get_time()}]  python_tool is not exist\n")
        download_pb["value"] += 40
        time.sleep(2)
        try:
            shutil.copytree(f"/Users/{user}/pt_saved/Update/python_tool.app","/Applications/python_tool.app")
            with open(f"/Users/{user}/pt_saved/logs/{r}.log", "a", encoding="utf-8") as b:
                b.write(f"[{get_time()}],python_tool has been updated.\n")
            download_pb["value"] += 40
            time.sleep(3)
            forget1(1)
            s_la.config(text="Update complate!Now you can open python_tool.app")
        except Exception as e:
            #cprint(f"Error to install update:{str(e)}")
            with open(f"/Users/{user}/pt_saved/logs/{r}.log", "a", encoding="utf-8") as d:
                d.write(f"[{get_time()}] copy error:{str(e)}\n")
            s_la.config(text=f"Error to install update,visit'/Users/{user}/pt_saved/logs/{r}.log'")
    u_t=threading.Thread(target=update_thread, daemon=True)
    u_t.start()
def opene():
    
    user = getpass.getuser()
    try:
        os.system("open /Applications/python_tool.app")
        with open(f"/Users/{user}/pt_saved/logs/{r}.log", "a", encoding="utf-8") as e:
            e.write(f"[{get_time()}] opened python_tool.app.\n")
    except Exception as e:
        with open(f"/Users/{user}/pt_saved/logs/{r}.log", "a", encoding="utf-8") as f:
            f.write(f"[{get_time()}] open error:{str(e)}\n")
        s_la.config(text=f"Error to open python_tool,visit'/Users/{user}/pt_saved/logs/{r}.log'")
root=tk.Tk()
root.title("Update python_tool")
img=ImageTk.PhotoImage(file="python_tool.ico")
label_img =tk.Label(root, image=img)
label_img.grid(row=0,column=0,pady=20,columnspan=3)
download_pb=ttk.Progressbar(root,length=500,mode="determinate")
download_pb.grid(row=1,column=0,pady=20,columnspan=3)
u_button=ttk.Button(root,text="update python_tool",command=update)
u_button.grid(row=2,column=0,pady=20,columnspan=3)
button=ttk.Button(root,text="open python_tool",command=opene)
button.grid(row=3,column=0,pady=20,columnspan=3)
s_la=ttk.Label(root,text="")
s_la.grid(row=4,column=0,pady=20,columnspan=3)
sv_ttk.set_theme("light")
forget1(2)
root.mainloop()
