from tkinter import *
root = Tk()
# root.title('Hello, my Name is _____')
# root. iconbitmap('c:/gui/codemy.ico')

w, l = 400, 300

def geometry(w,l):
    root.geometry(f'{w}x{l}')

count = 0
size = 24
def expand():
    global count, size
    if count<=10:
        count+=1
        size+=2
        # configure button font size
        button.config(font=('Helvetica',size))
        root.after(25,expand)

# work UI in shell
geometry(w,l)
button = Button(root,
                text='Click',
                command=expand,
                font=('Helvetica', size),
                # width=100,
                fg='blue')
button.pack(pady=100)

root.mainloop()
