import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
import tkinter.filedialog as filedialog
from tkinter.filedialog import asksaveasfilename


class TextEditor(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_te()
#--------------------------------------------------------------------------------------------------------------------------------------------------
#Function for the exit button
    def on_quit(self):
        quit()

#--------------------------------------------------------------------------------------------------------------------------------------------------
#Save file function.

    def save_feature(self):
        file = filedialog.asksaveasfile(mode='w')
        if file != None:
            data = self.textEdit.get('1.0', END+'-1c')
            file.write(data)
            file.close()
#--------------------------------------------------------------------------------------------------------------------------------------------------
#GUI Building and Grid options.

    def init_te(self):
        self.root.title('Word List Creator')
        self.textEdit = st.ScrolledText(root, width=80, height=20)
        self.textEdit.grid(column=0, row=0)
        self.grid(column=0, row=0, sticky='nsew')
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Makes it so the user cannot move the menu bar
        self.root.option_add('*tearOFF', 'FALSE')
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Menubar at the top of the program
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Save', command=self.save_feature)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.root.config(menu=self.menubar)
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

if __name__ == '__main__':
    root = tkinter.Tk()
    TextEditor(root)
    root.mainloop()
