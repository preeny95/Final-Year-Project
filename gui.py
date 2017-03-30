import tkinter
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as filedialog

class Analysis(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
#-----------------------------------------------------------------------Exit Button-----------------------------------------------------------------
#Function for the exit button
    def on_quit(self):
        quit()

#--------------------------------------------------------------VIBER DATABSASE ANALYSIS-------------------------------------------------------------
    def viber(self):
        from tkinter.filedialog import askopenfilename
        self.vfilename = askopenfilename()

    def viber_db(self):
        if self.vfilename:
            import sqlite3
            import pandas as pd

            conn = sqlite3.connect(self.vfilename)

            cur = conn.cursor()
            #Adapted from Stackoverflow.com by Parfait
            cur = cur.execute("""SELECT DISTINCT messages.conversation_id
                                FROM messages
                                INNER JOIN participants_info  ON messages.participant_id = participants_info._id
                                WHERE messages.conversation_id IS NOT NULL;""")

            query = ("""SELECT strftime('%Y-%m-%d %H:%M:%S',messages.date/1000,'unixepoch'), participants_info.number, participants_info.contact_name, messages.body AS Message_Sent, messages.conversation_id, messages.participant_id
                        FROM messages
                        INNER JOIN
                        participants ON messages.participant_id = participants._id
                        INNER JOIN
                        participants_info ON participants.participant_info_id = participants_info._id
                        WHERE messages.conversation_id = ?
                        ORDER BY messages.date;""")

            for convo in cur.fetchall():
                with open('{}.html'.format(convo), 'w') as h, open('{}.txt'.format(convo), 'w') as t:
                    df = pd.read_sql_query(query, conn, params=convo)

                    # HTML WRITE
                    h.write(df.to_html())
                    h.write('<br/>')

                    # TXT WRITE
                    t.write(df.to_string())
                    t.write('\n\n')

            cur.close()
            conn.close()

#------------------------------------------------------------------Text Editor---------------------------------------------------------------------
#Return to main gui function
    def return_main(self):
        self.textEdit.destroy()
        #self.init_gui.destroy()
        #root = tkinter.Tk()
        #Analysis(root)
        #root.mainloop()

#Save file function.

    def save_feature(self):
        file = filedialog.asksaveasfile(mode='w')
        if file != None:
            data = self.textEdit.get('1.0', END+'-1c')
            file.write(data)
            file.close()

#GUI Building and Grid options.

    def init_te(self):
        import tkinter.scrolledtext as st
        import tkinter.filedialog as filedialog
        from tkinter.filedialog import asksaveasfilename
        self.root.title('Word List Creator')
        self.textEdit = st.ScrolledText(root, width=80, height=20)
        self.textEdit.grid(column=0, row=0)
        self.grid(column=0, row=0, sticky='nsew')

        #Makes it so the user cannot move the menu bar
        self.root.option_add('*tearOFF', 'FALSE')

        #Menubar at the top of the program
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Save', command=self.save_feature)
        self.menu_file.add_command(label='Exit', command=self.return_main)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.root.config(menu=self.menubar)
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

#----------------------------------------------------------------Word list-----------------------------------------------------------------------

    def wordop(self):
        from tkinter.filedialog import askopenfilename
        self.wordopp = askopenfilename()



#----------------------------------------------------------------Chat Logs-----------------------------------------------------------------------
#Insert a users chatlog

    def clopen(self):
        from tkinter.filedialog import askopenfilename
        self.chatlog = askopenfilename()

    def chatanal(self):
        import os
        import io
        import re
        import sys
        wordlist = self.wordopp
        f = open(wordlist)
        l = set(w.strip().lower() for w in f)
        chatlog = self.chatlog
        with open(chatlog) as f:
            found = False
            file = open("out.txt", "w")
            for line in f:
                line = line.lower()
                if any(w in line for w in l):
                    found = True
                    file.write(line)
            if not found:
                print("not here")



#----------------------------------------------------------------GUI Grid and Buttons-----------------------------------------------------------------------

    def init_gui(self):
        #GUI Building and Grid options.
        self.root.title('Grooming Analysis')

        #Makes it so the user cannot move the menu bar
        self.root.option_add('*tearOFF', 'FALSE')

        #Menubar at the top of the program
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.root.config(menu=self.menubar)

        #Viber Message Extraction buttons
        self.viber_button = ttk.Button(self, width=25, text='Insert Viber Database', command=self.viber)
        self.viber_button.grid(column=2, row=1)
        self.viberanal_button = ttk.Button(self, width=25, text='Viber Database Analyse', command=self.viber_db)
        self.viberanal_button.grid(column=3, row=1)

        #Word list Button
        self.words_button = ttk.Button(self, width=25, text='Insert Words List', command=self.wordop)
        self.words_button.grid(column=3, row=2)
        self.words_button = ttk.Button(self, width=25, text='Create Word List', command=self.init_te)
        self.words_button.grid(column=2, row=2)

        #Chat log button
        self.chatlog_button = ttk.Button(self, width=25, text='Insert Chat log', command=self.clopen)
        self.chatlog_button.grid(column=2, row=3)
        self.chatlog_button = ttk.Button(self, width=25, text='Analyse Chat Log', command=self.chatanal)
        self.chatlog_button.grid(column=3, row=3)

        #Grid Options
        self.grid(column=0, row=0, sticky='nsew')
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


#--------------------------------------------------------------------------------------------------------------------------------------------------
#Gui loop
if __name__ == '__main__':
    root = tkinter.Tk()
    Analysis(root)
    root.mainloop()
