import tkinter
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as filedialog

class Analysis(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
#--------------------------------------------------------------------------------------------------------------------------------------------------
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

            conn = sqlite3.connect('viber_messages2')

            cur = conn.cursor()
            #Adapted from Stackoverflow.com by Parfait
            cur = cur.execute("""SELECT DISTINCT messages.conversation_id
                                FROM messages
                                INNER JOIN participants_info  ON messages.participant_id = participants_info._id
                                WHERE messages.conversation_id IS NOT NULL;""")

            query = ("""SELECT messages.date, participants_info.number, participants_info.contact_name, messages.body AS Message_Sent, messages.conversation_id, messages.participant_id
                        FROM messages
                        INNER JOIN
                        participants ON messages.participant_id = participants._id
                        INNER JOIN
                        participants_info ON participants.participant_info_id = participants_info._id
                        WHERE messages.conversation_id = ?
                        ORDER BY messages.date;""")

            with open('messages.html', 'w') as h, open('test.txt', 'w') as t:
                for convo in cur.fetchall():
                    df = pd.read_sql_query(query, conn, params=convo)

                    # HTML WRITE
                    h.write(df.to_html())
                    h.write('<br/>')

                    # TXT WRITE
                    t.write(df.to_string())
                    t.write('\n\n')

            cur.close()
            conn.close()
#--------------------------------------------------------------------------------------------------------------------------------------------------
    def init_gui(self):
        #GUI Building and Grid options.
        self.root.title('Grooming Analysis')
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Makes it so the user cannot move the menu bar
        self.root.option_add('*tearOFF', 'FALSE')
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Menubar at the top of the program
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.menu_edit = tkinter.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.root.config(menu=self.menubar)
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Viber Message Extraction buttons
        self.viber_button = ttk.Button(self, width=20, text='Insert Viber Database', command=self.viber)
        self.viber_button.grid(column=3, row=1)
        self.viberanal_button = ttk.Button(self, width=25, text='Viber Database Analyse', command=self.viber_db)
        self.viberanal_button.grid(column=4, row=1)
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Word list Button
        self.words_button = ttk.Button(self, width=15, text='Words List')
        self.words_button.grid(column=3, row=2)
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Chat log button
        self.chatlog_button = ttk.Button(self, width=15, text='Chat Log')
        self.chatlog_button.grid(column=3, row=3)
#--------------------------------------------------------------------------------------------------------------------------------------------------
        #Grid Options
        self.grid(column=0, row=0, sticky='nsew')
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)




if __name__ == '__main__':
    root = tkinter.Tk()
    Analysis(root)
    root.mainloop()
