from Tkinter import *

def Call():
        button_submit['bg'] = 'blue'
        button_submit['fg'] = 'white'

        url = input_url.get()
        listbox.insert(END,url);

root = Tk()
root.geometry('800x600+350+70')
label_url = Label( root, text="Please input source url:")
input_url = Entry(root, bd =1)
button_submit = Button(root, text = 'Start', command = Call)
listbox = Listbox(root)

label_url.pack()
input_url.pack()
button_submit.pack()
listbox.pack()   

root.mainloop()