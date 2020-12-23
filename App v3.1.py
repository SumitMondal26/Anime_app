import json
import os
import webbrowser
from custom_package.link_exctract import run
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox ,scrolledtext
from tkinter.ttk import Combobox

root=Tk()
root.title ("App")
root.iconbitmap("C://Users//Admin//Downloads//App folder//icon.ico")

def check_dir():
    if not os.path.exists("C:/Users/Admin/Documents/Episode_database"):
        os.mkdir("C:/Users/Admin/Documents/Episode_database")
    if not os.path.exists("C:/ProgramData/Episode_backup/backup.json") :
        os.mkdir("C:/ProgramData/Episode_backup")
        temp={"Last watched":None}
        with open("C:/ProgramData/Episode_backup/backup.json","w")as f:
            json.dump(temp,f)

check_dir()

default_dir= "C:/Users/Admin/Documents/Episode_database/Main_Db_data.json"
backup="C:/ProgramData/Episode_backup/backup.json"

def frame(master,side=TOP,text=None,fill=BOTH,bg=None):
    frm=LabelFrame(master,text=text,bg=bg)
    frm.pack(side=side,fill=fill,expand=YES)
    return frm

def button(master,text,command=None,side=None,fill=BOTH,state=NORMAL):
    btn = Button(master, text=text, relief='ridge',font=10,background='slategrey',command=command, bd=5,state=state,activebackground="white")
    btn.pack(side=side,fill=fill,expand=YES,padx=3,pady=3)
    return btn

def read_data(directory):
    global default_dir
    try:
        with open(directory) as f :
            f=json.load(f)
            data=dict()
            data.update(f)
            return data
    except Exception as e:
        messagebox.showerror(None,e)
        messagebox.showinfo("loading","loading from backup")
        temp=read_data(backup)
        save_data(temp,default_dir)
        data = read_data(default_dir)
        return data

def update_data(show_name, directory,newep=False):
    with open(directory) as f:
        links = f.read().splitlines()[::-1]
    ep_keys = []
    for i in range(len(links)):
        start=links[i].find("Episode")
        end = links[i].find("?")
        temp=links[i][start:end]
        ep_keys.append(temp)
        pass
    if not newep:
        ep_keys[0] = "trailer"
        ep_dict = dict(zip(ep_keys, links))
        temp = dict()
        temp[show_name] = ep_dict
        data.update(temp)
    if newep:
        return dict(zip(ep_keys,links))
    return data

def save_data(data,directory):
    try:
        with open(directory,"w")as f :
            json.dump(data,f,indent=2)
    except Exception as e:
        messagebox.showerror(message=e)

data=read_data(default_dir)

color='steelblue'

frm1=frame(root,text="Selection",bg=color)
frm2=frame(root,text="Now Playing",bg=color)
frm3=frame(root,bg=color)
frm4=frame(root,text="Data",bg=color)

x,y,length=None,None,0

file_loc_label=Label(frm4, text="file loc : " + default_dir, bg='slategray', relief='groove')
file_loc_label.pack(side='bottom', fill=X, expand=YES, padx=5)

Label(frm1,text='Select Show',bg=color).pack()
a=Combobox(frm1,justify='center',state='readonly',width=50)
a.pack(padx=3,pady=3)

Label(frm1,text='Select Episode',bg=color).pack()
b=Combobox(frm1,justify='center',state='readonly',width=50)
b.pack(padx=3)

def data_refresh():
    global data
    file_loc_label.configure(text="file loc : " + default_dir)
    l=list(data.keys())
    try:
        l.remove("Last watched")
    except:pass
    a['values'] = l
    root.after(100,data_refresh)
data_refresh()

now_playing_label=Label(frm2, text=None, relief='ridge')
now_playing_label.pack(side='top', fill=X, expand=YES, padx=5)

try:
    last_played_label=Label(frm2, text='Last watched :   ' + data["Last watched"], bg='slategray', relief='groove')
    last_played_label.pack(side='bottom', fill=X, expand=YES, padx=5)
except :pass

def refresh():
    global x, y,length
    if data.get(a.get()) is not None:

        b['values']=list(data.get(a.get()).keys())
        now_playing_label.configure(text=a.get() + " " + b.get())

        x = a.get()
        y = b.get()
        length=len(b['values'])

    root.after(100,func=refresh)
refresh()

def prev():
    try:
        global y
        ep_list=list(data.get(a.get()).keys())
        ep_index=ep_list.index(y)
        if ep_index > 1:
            ep_index -=1
            y=ep_list[ep_index]
            b.set(y)
            print(y, " ", ep_index)
    except Exception as e: messagebox.showinfo(None,str(e)+'\nno episode selected')
prev_btn=button(frm3,'prev',side=LEFT,command=prev)

def play():
    try :
        link=data[x][y]
        last_played_label.configure(text="Last watched :   " + str(x) + " " + str(y))
        data["Last watched"]=x+y
        save_data(data,default_dir)
        webbrowser.open_new_tab(link)
        save_data(data, backup)  # backup update

    except :
        if x == 0: messagebox.showinfo(None,'no show selected')
        else : messagebox.showinfo(None,'no episode selected')
play_btn=button(frm3,'play',side=LEFT,command=play)

def next_b():
    try:
        global y
        ep_list = list(data.get(a.get()).keys())
        ep_index = ep_list.index(y)
        if ep_index < length:
            ep_index += 1
            y = ep_list[ep_index]
            b.set(y)
            print(y, " ", ep_index)
    except: messagebox.showinfo(None,'no episode selected')
next_btn=button(frm3,'next',side=LEFT,command=next_b)

def btn_update():
    try :
        if y is None or y == "" :
            prev_btn.configure(state=DISABLED)
            next_btn.configure(state=DISABLED)
        elif y == list(data.get(a.get()).keys())[1] :
            prev_btn.configure(state=DISABLED)
        elif  y== list(data.get(a.get()).keys())[-1]:
            next_btn.configure(state=DISABLED)
        else :
            prev_btn.configure(state=NORMAL)
            next_btn.configure(state=NORMAL)

        root.after(ms=100,func=btn_update)
    except Exception as e:
        print(e)
btn_update()

def read_file():
    global default_dir,x,y
    try:
        default_dir=filedialog.askopenfile().name
        a.set("")
        b.set("")
        now_playing_label.configure(text="")
        x,y=None,None
    except Exception as e: messagebox.showinfo(None,e)

def update_shows():
    try:
        f= filedialog.askopenfile(title="file to be saved").name   #file to be saved directory dest .A
        name=simpledialog.askstring("show name",prompt="enter show name")
        ans=messagebox.askyesno(None,"enter file directory to be saved ?")
        if ans :
            fname=filedialog.askopenfile(title='where to save ?').name  # where file is to be saved dest .B
            save_data(update_data(name, f), fname)
        else :
            save_data(update_data(name, f), default_dir)
            messagebox.showinfo(None,"successfully updated")
    except Exception as e: messagebox.showinfo(None,e)

def episode_update():
    l = list(data.keys())
    l.remove("Last watched")

    window=Tk()
    sc=scrolledtext.ScrolledText(window)
    sc.pack()
    for i in l :
        sc.insert(1.0,i+"\n")
    try:
        name=simpledialog.askstring("show name", prompt="enter show name")
        temp=update_data(name,filedialog.askopenfile(title="file to be saved").name,True)
        data[name].update(temp)
        save_data(data,default_dir)
        messagebox.showinfo(None,"episodes updated")
        window.destroy()
    except :window.destroy()   
    
def clear_db():
    ans=messagebox.askyesno("clear main db","Are you sure ?")
    if ans :
        ans = messagebox.askyesno("clear main db", "Are you really sure ?")
        if ans:
            temp = {}
            save_data(temp,default_dir)
            a.set("")
            b.set("")
            b['values']=[]
            now_playing_label.configure(text="")
            x, y = None, None
            messagebox.showinfo(None,"data cleared")

read_btn=button(frm4,"read\ndb",read_file,side=LEFT)
update_shows_btn=button(frm4, "add\nshows", update_shows, side=LEFT)
update_episodes_btn=button(frm4, "update\nepisodes", episode_update, side=LEFT)
clear_db_btn=button(frm4, "clear\ndb",clear_db , side=LEFT)
link_extract_btn=button(frm4, "link\nextractor",lambda :run(), side=LEFT)

exit_btn=button(root,"exit",root.destroy)

root.minsize(480,420)
root.maxsize(480,420)
root.state("zoomed")

root.mainloop()
