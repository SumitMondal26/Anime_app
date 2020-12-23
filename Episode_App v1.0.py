import webbrowser
from tkinter import *
from tkinter.ttk import Combobox

ep_key=['episode ' + str(i) for i in range(40)]
link=["" for _ in range(40)]
try:
    with open("C://Users//Admin//Documents//link.txt") as f :
        ans=f.read()
    ans = ans.splitlines()
    c = -1
    for i in ans:
        link[c] = i
        c =c- 1
except:print("link file does not exist")

ep_dict=dict(zip(ep_key, link))

root=Tk()
root.title("Episode_App")
n=StringVar()
ep_disp_options=Combobox(root, textvariable=n)
ep_disp_options.pack()
ep_disp_options['values']=[i for i in ep_dict]

selected_ep_label=Label(text="None", fg="grey")
selected_ep_label.pack()
def update():
    key = n.get()
    global link
    link=ep_dict.get(key)
    selected_ep_label.configure(text=key, fg="green")

refresh=Button(root,text="refresh",command=update)
refresh.pack()

def start():
    webbrowser.open_new_tab(link)
launch=Button(text="Launch",command=start)
launch.pack()

exit_app=Button(root,text="exit",command=root.destroy)
exit_app.pack()

root.mainloop()
