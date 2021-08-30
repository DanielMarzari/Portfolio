# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 19:55:52 2020

@author: Daniel
"""

import numpy as np
import tkinter as tk
import json
import dpath.util as dpu

#-----------------------------FILE SYSTEM GLOBALS-----------------------------
SUPER = bytearray()
INODE = bytearray()
DATA = bytearray()
INODE_START = 0
DATA_START = 0
BLOCK_SIZE = 0
FILES = []
PATH = "root"

#-----------------------------TKINTER FUNCTIONS-----------------------------
def setText(obj, text):
    #enable the box, delete old text, put new text, and disable the box again
    obj.config(state=tk.NORMAL)
    obj.delete("1.0", tk.END)
    obj.insert("1.0", text)
    obj.config(state=tk.DISABLED)

def click_event_handler(event):
    global PATH
    #Get the selected folder
    FOL_NAME = dir_files.get(tk.ACTIVE)
    #Determine if we need to exit the current folder or enter a new folder
    if(FOL_NAME == ".."):
        #prevent from going out of root
        if(PATH != "root"):
            #update the path (exit)
            PATH = '/'.join(PATH.split('/')[0:-1])
    else:
        #update the path (enter)
        PATH = PATH + '/' + FOL_NAME.split('.')[0]
    #Update the list of folders in the directory
    update_dir()

def update_dir():
    global INODE, DATA, PATH, FILES, dir_files, directory
    #Quick nav the dictionary to get the INODE Key
    VALUE = dpu.get(SUPER, "dir/" + PATH)
    #If Value is a dictionary, we have a new directory, otherwise we have a file
    if(type(VALUE) == type({})):
        #Get the list of folders in this directory
        FILES = VALUE.keys()
        
        #Update the path text box
        setText(file_path, PATH)
        
        #remove all items from the listbox
        dir_files.delete(0, tk.END)
        #Add files to the drop down
        for index, f in enumerate(FILES):
            #If the entry is a folder put extension .dir
            #If the entry is a file put extension .txt
            if(type(VALUE[f]) == type({})):
                dir_files.insert(index, f + ".dir")
            else:
                dir_files.insert(index, f + ".txt")
            
        #Add .. to exit (when not at root)
        if(PATH != "root"):
            dir_files.insert(0, "..")
    else:
        #This is a file. Undo the change in path
        PATH = '/'.join(PATH.split('/')[0:-1])
        
        #get the INODE file info
        FILE = INODE[str(VALUE)]
        
        #get the file content from the DATA section
        FILE_CONTENT = DATA[FILE['P']]
        
        #Parse the verse and file info to display
        VERSE = FILE_CONTENT[0:FILE_CONTENT.find(b'\0')].decode('utf-8')
        FILE_INFO = FILE["I"].split("|")
        DISPLAY = "Author: %s\nDate:%s\nName:%s\nVerse:%s" % tuple(FILE_INFO + [VERSE])
        
        #Update with the new verse
        setText(file_text, DISPLAY)

#-----------------------------TKINTER UI-----------------------------
        
window = tk.Tk()
window.title("File Explorer")
window.geometry("750x500") #Set fixed size
window.resizable(False, False) #Can't resize

#-----------------------------FRAMES-----------------------------

#Top Section
directory = tk.Frame(master=window, height=60, width=750, bg="#d0ffff")
directory.pack(side=tk.TOP)

#Thin Left Section
file_list = tk.Frame(master=window, width=250, bg="white")
file_list.pack(fill=tk.Y, side=tk.LEFT)

#Large Right Section
file_content = tk.Frame(master=window, width=500, bg="#eee")
file_content.pack(fill=tk.Y, side=tk.LEFT)

#-----------------------------OBJECTS-----------------------------

# Used for the current path
file_path = tk.Text(master=directory)
file_path.config(height=1, width=750, state=tk.DISABLED)
file_path.pack(padx = 10, pady = 10)

#used for folder and file listing
dir_files = tk.Listbox(master = file_list)
dir_files.bind("<Double-Button-1>", click_event_handler) #double click item in list
dir_files.pack(padx = 10, pady = 10)

#used for file contents
file_text = tk.Text(master=file_content)
setText(file_text, "Select a folder or file from the list to the left.")
file_text.pack(padx = 10, pady = 10)

#-----------------------------FILE SYSTEM IMPORT-----------------------------

def loadFile():
    global SUPER, INODE, DATA, INODE_START, DATA_START, BLOCK_SIZE
    
    #load all file contents
    file_content = open("C:/Users/Daniel/Documents/Fall 2020/OS/FileSystem.fs", "rb").read()
    
    #get the SUPER JSON
    SUPER = json.loads(file_content[0:file_content.find(b'\0')].decode('utf-8'))
    
    #Set the position of our INODE block and DATA block
    INODE_START = SUPER["super-size"] + SUPER["ibmap-size"] + SUPER["dbmap-size"]
    DATA_START = INODE_START + SUPER["inode-size"]
    BLOCK_SIZE = SUPER["block-size"]

    #Get the INODE and DATA Blocks      
    INODE = json.loads(file_content[INODE_START: file_content.find(b'\0', INODE_START)].decode('utf-8'))
    BIBLE = file_content[DATA_START:]
    DATA = [BIBLE[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(31100)]
    
    #Update the file list with root folders
    update_dir()

#Load the File System
loadFile()

#Start Tkinter Module
window.mainloop()
