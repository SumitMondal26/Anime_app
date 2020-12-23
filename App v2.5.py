import json
import webbrowser
from tkinter import *
from tkinter import filedialog,simpledialog,messagebox
from tkinter.ttk import Combobox

root=Tk()
root.title ("App")
root.iconbitmap("C://Users//Admin//Downloads//App folder//icon.ico")

default_dir= "C:/Users/Admin/Documents/anime_app/Main_Db_data.json"

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
    except:
        print('file read error')

        messagebox.showerror(None,"file read falied")
        ans = messagebox.askyesno(None, 'enter default file loc ?')
        if ans:
            default_dir = filedialog.askopenfile(title="enter file loc").name
            data = read_data(default_dir)
        if not ans:
            messagebox.showinfo("creating","creating empty data in default loc")
            temp={}
            save_data(temp,default_dir)
            data = read_data(default_dir)
            pass
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
    except:
        messagebox.showerror(message="error")

color='steelblue'

frm1=frame(root,text="selection",bg=color)
frm2=frame(root,text="Now Playing",bg=color)
frm3=frame(root,bg=color)
frm4=frame(root,text="data",bg=color)

x,y,length=None,None,0

lbl=Label(frm4, text="file loc : "+default_dir,bg='slategray',relief='raised')
lbl.pack()

Label(frm1,text='select show',bg=color).pack()
a=Combobox(frm1,justify='center',state='readonly',width=50)
a.pack(padx=3,pady=3)

def data_refresh():
    global data
    data = read_data(default_dir)
    lbl.configure(text="file loc : "+default_dir)
    a['values'] = list(data.keys())
    root.after(100,data_refresh)
data_refresh()

Label(frm1,text='select episode',bg=color).pack()
b=Combobox(frm1,justify='center',state='readonly',width=50)
b.pack(padx=3)

lbl1=Label(frm2,text=None,relief='raised')
lbl1.pack(side='left',fill=X,expand=YES,padx=5)

def refresh():
    global x, y,length
    if data.get(a.get()) is not None:

        b['values']=list(data.get(a.get()).keys())
        lbl1.configure(text=a.get()+" "+b.get())
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
    except : messagebox.showinfo(None,'no episode selected')

prev_btn=button(frm3,'prev',side=LEFT,command=prev)

def play():
    try :
        link=data[x][y]
        webbrowser.open_new_tab(link)
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
    except:
        print("error")
btn_update()

def read_file():
    global default_dir,x,y
    try:
        default_dir=filedialog.askopenfile().name
        a.set("")
        b.set("")
        lbl1.configure(text="")
        x,y=None,None
    except : messagebox.showinfo(None,'file read failed')

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
    except : messagebox.showinfo(None," not updated ")

def episode_update():
    name=simpledialog.askstring("show name", prompt="enter show name")
    temp=update_data(name,filedialog.askopenfile(title="file to be saved").name,True)
    data[name].update(temp)
    save_data(data,default_dir)
    messagebox.showinfo(None,"episodes updated")

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
            lbl1.configure(text="")
            x, y = None, None
            messagebox.showinfo(None,"data cleared")

read_btn=button(frm4,"read db",read_file,side=LEFT)
update_shows_btn=button(frm4, "update db", update_shows, side=LEFT)
update_episodes_btn=button(frm4, "update episodes", episode_update, side=LEFT)
clear_db_btn=button(frm4, "clear db",clear_db , side=LEFT)

exit_btn=button(root,"exit",root.destroy)

root.minsize(400,400)
root.maxsize(400,400)
root.state("zoomed")

root.mainloop()
