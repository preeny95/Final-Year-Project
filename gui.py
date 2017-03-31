import tkinter
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as filedialog

class Analysis(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
        parent.minsize(width=965, height=500)
        parent.maxsize(width=965, height=500)
#-----------------------------------------------------------------------Exit Button----------------------------------------------------------------
#Function for the exit button
    def on_quit(self):
        quit()

#--------------------------------------------------------------VIBER DATABSASE ANALYSIS-------------------------------------------------------------
#Adapted from Stackoverflow.com by Parfait
    def viber(self):
        from tkinter.filedialog import askopenfilename
        self.vfilename = askopenfilename()

    def viber_db(self):
        if self.vfilename:
            import sqlite3
            import pandas as pd

            conn = sqlite3.connect(self.vfilename)
            cur = conn.cursor()
            cur = cur.execute("""SELECT DISTINCT messages.conversation_id
                                FROM messages
                                INNER JOIN participants_info  ON messages.participant_id = participants_info._id
                                WHERE messages.conversation_id IS NOT NULL;""")

            query = ("""SELECT strftime('%Y-%m-%d %H:%M:%S',messages.date/1000,'unixepoch') AS Time, participants_info.number AS Number, COALESCE(participants_info.contact_name, 'Phone Analysed') AS Contact, messages.body AS Message_Sent, messages.conversation_id AS ConversationID, messages.participant_id AS ParticipantID
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
#Tutorial followed at http://knowpapa.com/text-editor/
#Return to main gui function
    def return_main(self):
        self.textEdit.grid_forget()



#Save file function.

    def save_feature(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
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
        self.textEdit = st.ScrolledText(root, width=118, height=31)
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
        self.grid()


#----------------------------------------------------------------Word list-----------------------------------------------------------------------

    def wordop(self):
        from tkinter.filedialog import askopenfilename
        self.wordopen = askopenfilename(title="Please selet your chat log", filetypes=[("Text files","*.txt"), ("All Files","*.*")])


#----------------------------------------------------------------Chat Logs-----------------------------------------------------------------------
#Insert a users chatlog
#Adapted from the following websites:
#http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
#http://stackoverflow.com/questions/19007383/compare-two-different-files-line-by-line-in-python
    def clopen(self):
        from tkinter.filedialog import askdirectory
        self.chatopen = askdirectory(title="Select chat log directory")

    def chatanal(self):
        out = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=[("Text files","*.txt"), ("All Files","*.*")])
        import fnmatch
        import os
        import sys
        path = self.chatopen
        files = os.listdir(path)
        paths = []
        wordlist = self.wordopen
        word = open(wordlist)
        l = set(w.strip().lower() for w in word)
        inchat = []
        for file in files:
            paths.append(os.path.join(path, file))
            if fnmatch.fnmatch(file, '*.txt'):
                with open(paths[-1]) as f:
                    found = False
                    for line in f:
                        line = line.lower()
                        if any(w in line for w in l):
                            found = True
                            print (line)
                            out.write(line)
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

        #Instructions
        frame = Frame(self, borderwidth=1, relief="solid")
        frame.pack(side=TOP)
        labeltext = StringVar()
        #labeltext.set("")
        labeltext.set("This is a python program to enable a user to analyse a Viber database and run language analysis on the chats within. \n\nCreated by Nathan Preen for my Final Year Project at Leeds Beckett University. \n\nThe buttons below are as followed.\n\n Insert Viber Database: This will open a file dialog for the user to select the viber database.\n\n Viber Database Analyse:  This will run the analysis script and output the viber chats into the root folder of the script. The chat logs will be named automatically based on the conversation id's from the database. The user will also be given a HTML and Text format. \n\n Create Word List: This will open an inbuilt text editor to allow the user to create their own words list. This will not automatically direct the program to the word list, the user must set the word list using the insert words list button. Please note to be able to understand the analysis results your first word must be 'Time'  \n\n Insert Words List: This button will allow the user to insert their precreated word list (These must be in .txt format) Please note to be able to understand the analysis results your first word must be 'Time'. \n\n Insert Chat Logs: This button will ask the user to point the program to the directory where all of the chat logs are stored.\n\n Analyse Chat log: This button will run the analysis based on the files passed to the program by the user. The user MUST have inserted a word list and chat log directory to work.")
        self.label = Label(frame, textvariable=labeltext, width=120, height=30, wraplength=600)
        self.label.grid(column=0, row=1, columnspan=6, rowspan=4, pady=5, padx=5)

        #Viber Message Extraction buttons
        bframe = Frame(self, borderwidth=1, relief="solid", bg="red")
        bframe.pack(side=RIGHT)

        self.viber_button = ttk.Button(bframe, width=25, text='Insert Viber Database', command=self.viber)
        self.viber_button.grid(column=1, row=0,sticky='N')
        self.viberanal_button = ttk.Button(bframe, width=25, text='Viber Database Analyse', command=self.viber_db)
        self.viberanal_button.grid(column=2, row=0,sticky='N')

        #Word list Button
        self.words_button = ttk.Button(bframe, width=25, text='Insert Words List', command=self.wordop)
        self.words_button.grid(column=4, row=0,sticky='N')
        self.words_button = ttk.Button(bframe, width=25, text='Create Word List', command=self.init_te)
        self.words_button.grid(column=3, row=0,sticky='N')

        #Chat log button
        self.chatlog_button = ttk.Button(bframe, width=25, text='Insert Chat log Directory', command=self.clopen)
        self.chatlog_button.grid(column=5, row=0)
        self.chatlog_button = ttk.Button(bframe, width=25, text='Analyse Chat Log', command=self.chatanal)
        self.chatlog_button.grid(column=6, row=0)

        #Grid Options
        self.grid()


#--------------------------------------------------------------------------------------------------------------------------------------------------
#Gui loop
if __name__ == '__main__':
    root = tkinter.Tk()
    Analysis(root)
    root.mainloop()
