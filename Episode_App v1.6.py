import webbrowser
import tkinter
from tkinter import messagebox
from tkinter.ttk import Combobox

try:
    with open("C://Users//Admin//Documents//link.txt") as f :
        ans=f.read()
    ans = ans.splitlines()
    ep_key = ['episode ' + str(i) for i in range(len(ans))]
    link = ["" for _ in range(len(ans))]
    ep_key[0]="trailer"
    c = -1
    for i in ans:
        link[c] = i
        c =c- 1
except:print("link file does not exist")

ep_dict=dict(zip(ep_key, link))

root=tkinter.Tk()
root.title("Episode_App")
root.iconbitmap("C://Users//Admin//Downloads//New folder//iconapp.ico")

tkinter.Label(text="JoJo no Kimyō na Bōken Daiyamondo wa Kudakenai").pack()

n=tkinter.StringVar()
ep_disp_options=Combobox(root, textvariable=n)
ep_disp_options.pack()
ep_disp_options['values']=[i for i in ep_dict]
ep_disp_options.current(1)

selected_ep_label=tkinter.Label(text="None", fg="grey")
selected_ep_label.pack()

frm=tkinter.Frame(root)
frm.pack()

def next_ep():
    key ="episode "+str((int((n.get()).split(" ")[1]))+1)
    if int(key.split(" ")[1]) <= 39 :
        ep_disp_options.set(key)
        global link
        link = ep_dict.get(key)
        selected_ep_label.configure(text=key, fg="green")

next_b=tkinter.Button(frm, text="next", command=next_ep)
next_b.pack(side='left')

tkinter.Label(frm,text=" ").pack(side="left")

def prev_ep():
    key ="episode "+str((int((n.get()).split(" ")[1]))-1)
    if int(key.split(" ")[1]) >= 0 :
        ep_disp_options.set(key)
        global link
        link = ep_dict.get(key)
        selected_ep_label.configure(text=key, fg="green")

prev_b=tkinter.Button(frm, text="prev", command=prev_ep)
prev_b.pack(side='right')

def start():
    try:
        key =n.get()
        ep_disp_options.set(key)
        global link
        link = ep_dict.get(key)
        selected_ep_label.configure(text=key, fg="green")
        webbrowser.open_new_tab(link)
    except: messagebox.showerror(None,"No link selected")

launch=tkinter.Button(text="Launch", command=start)
launch.pack()

exit_app=tkinter.Button(root, text="exit", command=root.destroy).pack()

root.maxsize(300,150)
root.minsize(300,150)

root.mainloop()
