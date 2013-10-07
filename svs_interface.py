#!/usr/bin/env python

import subprocess
import Tkinter
import tkFileDialog
import tkSimpleDialog
import os
import datetime

GPG = 'gpg2'
SERVER_KEY = ''  # replace with gpg key ID of server key
DECRYPTED_PREFIX = 'decrypted'

class GpgApp(object):
    def __init__(self, master):
        frame = Tkinter.Frame(master)
        frame.pack()
        self.text = Tkinter.Text()
        self.text.pack()
        menu = Tkinter.Menu(master)
        root.config(menu=menu)

        filemenu = Tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.filename_open)
        filemenu.add_command(label="Decrypt files", command=self.batch_decrypt)
        filemenu.add_command(label="Encrypt files", command=self.batch_encrypt)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.do_exit)
    def filename_open(self):
        fin = tkFileDialog.askopenfilenames()
        if fin:
            self.text.insert(Tkinter.END,fin)
            return fin
    def get_recipient(self):
        prompt = "Enter the email address to encrypt files to: "
        recipient = tkSimpleDialog.askstring("Encrypt files", prompt)
        return recipient
    def batch_decrypt(self):
        timestring = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        dirname = 'decrypted_'+timestring+'/'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fin = tkFileDialog.askopenfilenames()
        print fin
        for f in fin:
            try:
                self.decrypt_file(f, dirname+os.path.basename(f)+'_decrypted')
            except:
                print "Error decrypting: "+f
        self.text.insert(Tkinter.END, 'Wrote decrypted files to '+dirname+'\n')
    def batch_encrypt(self, recipient=None):
        recipient = self.get_recipient()
        if recipient is None:
            self.text.insert(Tkinter.END, "You must specify an email address for encryption\n")
            return
        timestring = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        dirname = 'encrypted_'+timestring+'/'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fin = tkFileDialog.askopenfilenames()
        for f in fin:
            try:
                self.encrypt_file(f, dirname+os.path.basename(f)+'_encrypted', recipient)
            except:
                print "Error encrypting: "+f
        self.text.insert(Tkinter.END, 'Wrote encrypted files to '+dirname+'\n')
    def encrypt_file(self, input_file, output_file, recipient):
        args = [GPG, '--output', output_file, '--recipient', recipient, '-sea', input_file]
        subprocess.call(args)
    def decrypt_file(self, input_file, output_file):
        args = [GPG, '--output', output_file, '--decrypt', input_file]
        subprocess.call(args)
    def do_exit(self):
        root.destroy()


root = Tkinter.Tk()
root.title("a simple GnuPG interface")
app = GpgApp(root)
root.mainloop()