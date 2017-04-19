import tkinter
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as filedialog
from tkinter import messagebox
from datetime import datetime
import os
import logging

if not os.path.exists("Logs"):
                 os.makedirs("Logs")

if not os.path.exists("TextLogs"):
                os.makedirs("TextLogs")

if not os.path.exists("HTMLLogs"):
                os.makedirs("HTMLLogs")

if not os.path.exists("CSVLogs"):
                os.makedirs("CSVLogs")




logname = "Logs/{}.txt".format(datetime.now().strftime("%d-%m-%Y %H.%M.%S"))
logging.basicConfig(filename=logname,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

# Function for date file name from: http://stackoverflow.com/questions/31886584/how-can-i-generate-a-file-in-python-with-todays-date

class Analysis(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
        parent.minsize(width=859, height=522)
        parent.maxsize(width=859, height=522)


#--------------------------------------------------------------VIBER DATABSASE ANALYSIS-------------------------------------------------------------
#Adapted from Stackoverflow.com by Parfait
    def viber(self):
        from tkinter.filedialog import askopenfilename
        self.vfilename = askopenfilename()
        logging.info(self.vfilename + " Viber database successfully loaded")
        messagebox.showinfo("Success", "Viber Database successfully loaded")
    def viber_db(self):
            import sqlite3
            import pandas as pd

            conn = sqlite3.connect(self.vfilename)
            cur = conn.cursor()
            cur = cur.execute("""SELECT DISTINCT messages.conversation_id
                                FROM messages
                                INNER JOIN participants_info  ON messages.participant_id = participants_info._id
                                WHERE messages.conversation_id IS NOT NULL;""")

            query = ("""SELECT strftime('%Y-%m-%d %H:%M:%S',messages.date/1000,'unixepoch') AS Time, participants_info.number AS Number, COALESCE(participants_info.contact_name, 'Phone Analysed') AS ContactName, messages.body AS Message_Sent, messages.conversation_id AS ConversationID, messages.participant_id AS ParticipantID
                        FROM messages
                        INNER JOIN
                        participants ON messages.participant_id = participants._id
                        INNER JOIN
                        participants_info ON participants.participant_info_id = participants_info._id
                        WHERE messages.conversation_id = ?
                        ORDER BY messages.date;""")

            for convo in cur.fetchall():
                with open('HTMLLogs/Conversation{}.html'.format(convo), 'w') as h, open('TextLogs/Conversation{}.txt'.format(convo), 'w') as t, open('CSVLogs/Conversation{}.csv'.format(convo), 'w') as c:
                    df = pd.read_sql_query(query, conn, params=convo)

                    # HTML WRITE
                    h.write(df.to_html())
                    h.write('<br/>')

                    # TXT WRITE
                    t.write(df.to_string())
                    t.write('\n\n')

                    # CSV WRITE
                    c.write(df.to_csv())
                    #logger.write ("test")
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Viber database successfully analysed, check relevant log folders for information")
            logging.info("The file you have analysed is located at " + self.vfilename)
            logging.info("There are {} conversations found".format(convo))


#------------------------------------------------------------------Text Editor---------------------------------------------------------------------
#Tutorial followed at http://knowpapa.com/text-editor/
#Return to main gui function
    def return_main(self):
        self.textEdit.grid_forget()
        self.menubar.delete(0, END)

#Save file function.

    def save_feature(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if file != None:
            data = self.textEdit.get('1.0', END+'-1c')
            file.write(data)
            file.close()
            logging.info ("Word list has been saved.")

#GUI Building and Grid options.

    def init_te(self):
        import tkinter.scrolledtext as st
        import tkinter.filedialog as filedialog
        from tkinter.filedialog import asksaveasfilename
        self.root.title('Word List Creator')
        top=self.top=Toplevel(root)
        self.textEdit = st.ScrolledText(top, width=118, height=30.5)
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
        messagebox.showinfo("Success", "Word list successfully loaded")
        logging.info("The word list located at: " + self.wordopen + " has been loaded")

#----------------------------------------------------------------Chat Logs-----------------------------------------------------------------------
#Insert a users chatlog
#Adapted from the following websites:
#http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
#http://stackoverflow.com/questions/19007383/compare-two-different-files-line-by-line-in-python
    def clopen(self):
        from tkinter.filedialog import askdirectory
        self.chatopen = askdirectory(title="Select chat log directory")
        logging.info("The directory " + self.chatopen + " has been loaded")
        messagebox.showinfo("Success", "Chat log directory successfully loaded")
    def chatanal(self):
        out = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=[("Text files","*.txt"), ("All Files","*.*")])
        csvname = out #check if needed.
        import fnmatch #check
        import os
        import sys
        path = self.chatopen
        files = os.listdir(path)
        paths = []
        wordlist = self.wordopen
        word = open(wordlist)
        l = set(w.strip().lower() for w in word)
        for file in files:
            paths.append(os.path.join(path, file))
            if fnmatch.fnmatch(file, '*.txt'):
                logging.info(str(file) + " successfully analysed")
                with open(paths[-1]) as f:
                    found = False
                    fline = f.readline()
                    out.write(fline)
                    for line in f:
                        line = line.lower()
                        if any(w in line for w in l):
                            found = True
                            print (line)
                            out.write(line)
                            if not found:
                                print("not here")
        messagebox.showinfo("Success", "Viber Database successfully analysed")

#----------------------------------------------------------------GUI Grid and Buttons-----------------------------------------------------------------------

    def init_gui(self):
        #GUI Building and Grid options.
        self.root.title('Grooming Analysis')

        #Instructions
        frame = Frame(self, borderwidth=1, relief="solid")
        frame.pack(side=TOP)
        labeltext = StringVar()
        labeltext.set("This is a python program to enable a user to analyse a Viber database and run language analysis on the chats within. \n\nCreated by Nathan Preen for my Final Year Project at Leeds Beckett University. \n\nWithin the directory of this program there is a log folder, this contains logs of all of the actions you have undertaken. The program will also create 3 other folders within the directory, these will contain HTML, CSV and text files of the information obtained from analysis\n\nThe buttons below are as followed.\n\n Insert Viber Database: This will open a file dialog for the user to select the viber database.\n\n Viber Database Analyse:  This will run the analysis script and output the viber chats into the root folder of the script. The chat logs will be named automatically based on the conversation id's from the database. The user will also be given a HTML and Text format. \n\n Create Word List: This will open an inbuilt text editor to allow the user to create their own words list. This will not automatically direct the program to the word list, the user must set the word list using the insert words list button. \n\n Insert Words List: This button will allow the user to insert their precreated word list (These must be in .txt format). \n\n Insert Chat Logs: This button will ask the user to point the program to the directory where all of the chat logs are stored.\n\n Analyse Chat log: This button will run the analysis based on the files passed to the program by the user. The user MUST have inserted a word list and chat log directory to work.")
        self.label = Label(frame, textvariable=labeltext, width=120, height=30, wraplength=600)
        self.label.grid(column=0, row=0, columnspan=6, rowspan=4, pady=5, padx=5)

        #Viber Message Extraction buttons
        bframe = Frame(self, borderwidth=1, relief="solid")
        bframe.pack(side=RIGHT)

        self.viber_button = ttk.Button(bframe, width=25, text='Insert Viber Database', command=self.viber)
        self.viber_button.grid(column=2, row=0,sticky='N')
        self.viberanal_button = ttk.Button(bframe, width=25, text='Viber Database Analyse', command=self.viber_db)
        self.viberanal_button.grid(column=2, row=1,sticky='N')

        #Word list Button
        self.words_button = ttk.Button(bframe, width=25, text='Insert Words List', command=self.wordop)
        self.words_button.grid(column=3, row=0,sticky='N')
        self.words_button = ttk.Button(bframe, width=25, text='Create Word List', command=self.init_te)
        self.words_button.grid(column=3, row=1,sticky='N')

        #Chat log button
        self.chatlog_button = ttk.Button(bframe, width=25, text='Insert Chat log Directory', command=self.clopen)
        self.chatlog_button.grid(column=5, row=0)
        self.chatlog_button = ttk.Button(bframe, width=25, text='Analyse Chat Logs', command=self.case_stuff)
        self.chatlog_button.grid(column=6, row=0)

        #Case Details
        self.casedetails_button = ttk.Button(bframe, width=25, text='Insert Case Details', command=self.case_stuff)
        self.casedetails_button.grid(column=1, row=0)

        #Grid Options
        self.grid()
#----------------------------------------------------------------Case Entry----------------------------------------------------------------------------


    def case_stuff(self):
        top=self.top=Toplevel(root)
        #top.attributes("-topmost", True)
        self.casetitle=Label(top,text="Please enter your case details")
        self.casetitle.grid(column=1, row=1)

        self.namelabel=Label(top,text="Please enter your Case Name")
        self.namelabel.grid(column=1, row=2)
        self.name=Entry(top)
        self.name.grid(column=2, row=2)

        self.invname=Label(top, text="Please enter your name")
        self.invname.grid(column=1, row=3)
        self.invesname=Entry(top)
        self.invesname.grid(column=2, row=3)

        self.caselabel=Label(top, text="Please enter your case number")
        self.caselabel.grid(column=1, row=4)
        self.casenumber=Entry(top)
        self.casenumber.grid(column=2, row=4)

        self.orglabel=Label(top, text="Please enter your organization")
        self.orglabel.grid(column=1, row=5)
        self.orgentry=Entry(top)
        self.orgentry.grid(column=2, row=5)

        self.contactlabel=Label(top, text="Please enter your contact information")
        self.contactlabel.grid(column=1, row=6)
        self.contactinfo=Entry(top)
        self.contactinfo.grid(column=2, row=6)

        self.b=Button(top,text='Ok', command=self.caseclose)
        self.b.grid(column=1, row=7)


    def caseclose(self):
        self.namevalue=self.name.get()
        self.invvalue=self.invesname.get()
        self.casevalue=self.casenumber.get()
        self.orgvalue=self.orgentry.get()
        self.contactvalue=self.contactinfo.get()
        self.top.destroy()
        logging.info("Case Name: " + self.namevalue)
        logging.info("Investigator Name: " + self.invvalue)
        logging.info("The organization: " + self.orgvalue)
        logging.info("Contact Details: " + self.contactvalue)



#--------------------------------------------------------------------------------------------------------------------------------------------------
#Gui loop
if __name__ == '__main__':
    root = tkinter.Tk()
    Analysis(root)
    root.mainloop()
