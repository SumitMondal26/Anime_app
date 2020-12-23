import json
import webbrowser
from tkinter import *
from tkinter import filedialog,simpledialog,messagebox
from tkinter.ttk import Combobox,Style

root=Tk()

def frame(master,side=TOP,fill=BOTH):
    frm=Frame(master,bg='slate gray')
    frm.pack(side=side,fill=fill,expand=YES)
    return frm
def button(master,text,command=None,side=None,icon=False,fill=BOTH,state=NORMAL):
    btn = Button(master, text=text, relief='solid', command=command, bd=2,state=state)
    btn.pack(side=side,fill=fill,expand=YES,padx=3,pady=3)
    return btn

def read_data(directory):
    try:
        with open(directory) as f :
            f=json.load(f)
            data=dict()
            data.update(f)
            return data
    except:
        print('file read error')
        messagebox.showerror(None,"file read falied")
def update_data(show_name, directory):
    with open(directory) as f:
        links = f.read().splitlines()[::-1]
    ep_keys = ['ep ' + str(i) for i in range(len(links))]
    ep_keys[0] = "trailer"
    ep_dict = dict(zip(ep_keys, links))
    temp = dict()
    temp[show_name] = ep_dict
    data.update(temp)

    return data
def save_data(data,directory):
    with open(directory,"w")as f :
        json.dump(data,f,indent=2)

default_dir= "C:/Users/Admin/Documents/anime_app/newdata.json"

ans=messagebox.askyesno(None,'enter default file loc ?')
if ans :
    default_dir=filedialog.askopenfile(title="enter file loc").name
    data=read_data(default_dir)

frm1=frame(root)
frm2=frame(root)
frm3=frame(root)
frm4=frame(root)

x,y=None,None

lbl=Label(frm4, text="file loc : "+default_dir)
lbl.pack()

a=Combobox(frm1,justify='center',state='readonly')
a.pack(padx=3,pady=3)

def data_refresh():
    global data
    data = read_data(default_dir)
    lbl.configure(text="file loc : "+default_dir)
    a['values'] = list(data.keys())
    root.after(100,data_refresh)
data_refresh()

b=Combobox(frm1,justify='center',state='readonly')
b.pack(padx=3)

lbl1=Label(frm2,text=None)
lbl1.pack(side='left',fill=X,expand=YES,padx=5)

def refresh():
    global x, y
    if data.get(a.get()) is not None:
        b['values']=list(data.get(a.get()).keys())
        lbl1.configure(text=a.get()+" "+b.get())
        x = a.get()
        y = b.get()
    root.after(500,func=refresh)
refresh()

def prev():
    try:
        ep_no=int(y.split(" ")[1])
        if ep_no > 1 :
            ep_no=ep_no-1
            b.set("ep "+str(ep_no))
    except : messagebox.showinfo(None,'no episode selected')

prev_btn=button(frm3,'prev',side=LEFT,command=prev)

def play():
    try :
        link=data[x][y]
        webbrowser.open_new_tab(link)
    except :
        if x == 0:
            messagebox.showinfo(None,'no show selected')
        else :
            messagebox.showinfo(None,'no episode selected')

play_btn=button(frm3,'play',side=LEFT,command=play)

def next_b():
    try :
        global y
        ep_no = int(y.split(" ")[1])
        if ep_no < len(data[x].keys())-1:
            ep_no = ep_no + 1
            b.set("ep " + str(ep_no))
    except: messagebox.showinfo(None,'no episode selected')

next_btn=button(frm3,'next',side=LEFT,command=next_b)

def btn_update():
    if y is None or y == "":
        prev_btn.configure(state=DISABLED)
        next_btn.configure(state=DISABLED)
    else :
        prev_btn.configure(state=NORMAL)
        next_btn.configure(state=NORMAL)

    root.after(ms=500,func=btn_update)

btn_update()

def read_file():
    global default_dir,x,y
    try:
        default_dir=filedialog.askopenfile().name
        a.set("")
        b.set("")
        lbl1.configure(text="")
        x,y=None,None
    except:messagebox.showinfo(None,'file read failed')

def update_shows():
    try:
        f= filedialog.askopenfile(title="file to be saved").name   #file to be saved ddirectory dest .A
        name=simpledialog.askstring("show name",prompt="enter show name")
        ans=messagebox.askyesno(None,"enter file directory to be saved ?")
        if ans :
            fname=filedialog.askopenfile(title='where to save ?').name  # where file is to be saved dest .B
            save_data(update_data(name, f), fname)
        else :
            save_data(update_data(name, f), default_dir)
        messagebox.showinfo(None,"successfully updated")
    except:messagebox.showinfo(None,"update failed")

read_btn=button(frm4,"read",read_file,side=LEFT)
update_show_btn=button(frm4, "update_show", update_shows, side=LEFT)

exit_btn=button(root,"exit",root.destroy)

root.minsize(350,300)
root.maxsize(350,300)
root.state("zoomed")
root.mainloop()
