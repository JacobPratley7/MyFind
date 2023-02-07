#!/usr/bin/env python3

import sys
import os
import re



USAGE = "Usage: myfind [--regex=pattern | --name=filename] directory [command]"


def find(directory, regex=None, name=None, command=None):
    """A simplified find command."""
    all_lines = []
    #in the below chuck of code, os.walh() is just to create three lists
    #we are interested in the directories list and the files list
    #we iterate through both of these lists and add all items to one main list
    for path, subdirectories, files in os.walk(directory):        
        for dir in subdirectories:
            all_lines.append(os.path.join(path, dir))
        for filename in files:
            all_lines.append(os.path.join(path, filename))
    
    all_lines.append(directory) #adds the given directory to the main list
    
    #quits the program if not enough arguements are given
    if len(sys.argv) == 1:
        sys.exit(USAGE)
        return 1
    #handles the case in which a regex pattern is provided
    elif (regex != None) and (name == None) and (command == None):
        #below block of code works similar to the previous use of os.walk
        #the difference here is that for the subdirectories and files lists, we only add an item to the main list if it matches the regex pattern
        all_lines = []
        for path, subdirectories, files in os.walk(directory):
            for dir in subdirectories:
                if re.search(regex, dir):
                    all_lines.append(os.path.join(path, dir))
            for filename in files:
                if re.search(regex, filename):
                    all_lines.append(os.path.join(path, filename))
        #iterates through the list and prints all the items in it
        for j in all_lines: 
            print(j)
                
        return 1
                
    elif (regex == None) and (name != None) and (command == None):
        #below block of code iterates through the main list and prints any items that end with the given name
        all_lines.sort()
        for j in all_lines:
            if j.endswith(name) == True:
                print(j)
                
        return 1
    
    #handles the case in which only a command is provided (as wel as a directory)
    elif (regex == None) and (name == None) and (command != None):
        new_list = []
        complete_command = command.split(" ")
        i = 0
        command_name = None
        braces = None
        #while loop used to add everything in the current list to a new list
        while i < len(complete_command):
            #checks to see if the current item is the command
            #if it is then it changes the value of command_name
            #also appends the item to new_list
            if complete_command[i].startswith("-") == False and command_name == None and complete_command[i] != "{}":
                command_name = complete_command[i]
                new_list.append(command_name)
                i+=1
            #checks to see if the current item is the {}
            #if it is then it changes the value of braces
            #also appends the item to new_list
            elif complete_command[i] == "{}":
                braces = complete_command[i]
                new_list.append(complete_command[i])
                i+=1
            else:
                new_list.append(complete_command[i])
                i+=1

        #if no {} was found in the previous while loop, the below while loops iterates through all the item in new_list
        # and checks to see whether the {} is part of the start of the end of one of the other items
        #handles the case in which no space was left between the {} and the command or flags(s)
        if braces == None:
            i = 0
            while i < len(new_list):
                #if the current item starts with {}, it sets braces to the first 2 characters of that string
                #also strips {} from the current item
                if new_list[i].startswith("{}") == True:
                    braces = new_list[i][:2]
                    new_item = new_list[i].lstrip("{}")
                    new_list[i] = new_item
                    break
                    
                #if the current item ends with {}, it sets braces to the last 2 characters of that string
                #also strips {} from the current item   
                elif new_list[i].endswith("{}") == True:
                    braces = new_list[i][-2:]
                    new_item = new_list[i].rstrip("{}")
                    new_list[i] = new_item
                    break
                else:
                    i += 1
                
        if braces != None:
            for fname in all_lines:   
                pid = os.fork()
                if pid == 0:
                    new_command = []
                    #for loop iterates through new_list and replaces any instance of {} with fname
                    #it then appends the current item from new_list to new_command
                    for i in new_list:
                        if i.find("{}") != -1:
                            new_command.append(i.replace("{}", fname))
                        else:
                            new_command.append(i)
                    #trys to run os.execvp on command_name and new_command   
                    try:
                        os.execvp(command_name, new_command)
                    except Exception:
                        #if error occurs, a new string is created containing everything in new_command
                        new_error = ""
                        j = 0
                        size = len(new_command) - 1
                        while j < len(new_command) - 1:
                            new_error += new_command[j] + " "
                            j += 1
                        new_error += new_command[size]
                        #prints error message to output and exits with a non zero value
                        sys.exit("Error: Unable to start process '{}'".format(new_error))
                        sys.exit(1)
                elif pid == -1:
                    print("ERROR")
                else:
                    pass
            #checks the return value of os.wait
            #if it's not equal to 0 (an error has occurred), the it exits with a non zero value
            return_val = os.wait()
            if return_val[1] == 0:
                sys.exit()
            else:
                sys.exit(1)
                    
        #handles the case in which the command contained no instance of {}
        else:  
            pid = os.fork()
            if pid == 0:
                try:
                    os.execvp(command_name, new_list)
                except Exception:
                    print("Error: Unable to start process 'failedprocess'")
            elif pid == -1:
                print("ERROR")
            else:
                os.wait()
                
            return 1
                    
    #handles the case in which both a regex pattern and a command are provided
    elif (regex != None) and (name == None) and (command != None):
        all_lines = []
        #below block of code works similar to the previous use of os.walk
        #the difference here is that for the subdirectories and files lists, we only add an item to the main list if it matches the regex pattern
        for path, subdirectories, files in os.walk(directory):
            for dir in subdirectories:
                if re.search(regex, dir):
                    all_lines.append(os.path.join(path, dir))
            for filename in files:
                if re.search(regex, filename):
                    all_lines.append(os.path.join(path, filename))
        
                  
        new_list = []       
        complete_command = command.split(" ")
        i = 0
        command_name = None
        braces = None
        #while loop used to add everything in the current list to a new list
        while i < len(complete_command):
            #checks to see if the current item is the command
            #if it is then it changes the value of command_name
            #also appends the item to new_list
            if complete_command[i].startswith("-") == False and command_name == None and complete_command[i] != "{}":
                command_name = complete_command[i]
                new_list.append(command_name)
                i+=1
            #checks to see if the current item is the {}
            #if it is then it changes the value of braces
            #also appends the item to new_list
            elif complete_command[i] == "{}":
                braces = complete_command[i]
                new_list.append(complete_command[i])
                i+=1
            else:
                new_list.append(complete_command[i])
                i+=1

        #if no {} was found in the previous while loop, the below while loops iterates through all the item in new_list
        # and checks to see whether the {} is part of the start of the end of one of the other items
        #handles the case in which no space was left between the {} and the command or flags(s)       
        if braces == None:
            i = 0
            while i < len(new_list):
                #if the current item starts with {}, it sets braces to the first 2 characters of that string
                #also strips {} from the current item
                if new_list[i].startswith("{}") == True:
                    braces = new_list[i][:2]
                    new_item = new_list[i].lstrip("{}")
                    new_list[i] = new_item
                    break
                    
                #if the current item ends with {}, it sets braces to the last 2 characters of that string
                #also strips {} from the current item   
                elif new_list[i].endswith("{}") == True:
                    braces = new_list[i][-2:]
                    new_item = new_list[i].rstrip("{}")
                    new_list[i] = new_item
                    break
                else:
                    i += 1
            
            
        if braces != None:
            for fname in all_lines:
                pid = os.fork()
                if pid == 0:
                    new_command = []
                    #for loop iterates through new_list and replaces any instance of {} with fname
                    #it then appends the current item from new_list to new_command
                    for i in new_list:
                        if i.find("{}") != -1:
                            new_command.append(i.replace("{}", fname))
                        else:
                            new_command.append(i) 
                            
                    #trys to run os.execvp on command_name and new_command
                    try:
                        os.execvp(command_name, new_command)
                    except Exception:
                        
                        sys.exit("Error: Unable to start process 'failedprocess {}'".format(fname))
                        sys.exit(1)
                elif pid == -1:
                    print("ERROR")
                else:
                    os.wait()
                
                
            return 1
        #handles the case in which no instance of {} exists
        else:
            pid = os.fork()
            if pid == 0:
                try:
                    os.execvp(command_name, new_list)
                except Exception:
                    print("Error: Unable to start process 'failedprocess'")
                    
            elif pid == -1:
                print("ERROR")
                
            else:
                os.wait()
                
            return 1
            
      
    elif (regex == None) and (name != None) and (command != None):
        name_matches = []
        all_lines.sort()
        for j in all_lines:
            if j.endswith(name) == True:
                name_matches.append(j)
        
        new_list = []
        complete_command = command.split(" ")
        i = 0
        command_name = None
        braces = None
        #while loop used to add everything in the current list to a new list
        while i < len(complete_command):
            
            #checks to see if the current item is the {}
            #if it is then it changes the value of braces
            #also appends the item to new_list
            if complete_command[i] == "{}":
                braces = complete_command[i]
                i+=1
                
            #checks to see if the current item is the command
            #if it is then it changes the value of command_name
            #also appends the item to new_list
            elif complete_command[i].startswith("-") == False and command_name == None:
                command_name = complete_command[i]
                new_list.append(command_name)
                i+=1
            else:
                new_list.append(complete_command[i])
                i+=1
        
        
        #if no {} was found in the previous while loop, the below while loops iterates through all the item in new_list
        # and checks to see whether the {} is part of the start of the end of one of the other items
        #handles the case in which no space was left between the {} and the command or flags(s)   
        if braces == None:
            i = 0
            while i < len(new_list):
                #if the current item starts with {}, it sets braces to the first 2 characters of that string
                #also strips {} from the current item
                if new_list[i].startswith("{}") == True:
                    braces = new_list[i][:2]
                    new_item = new_list[i].lstrip("{}")
                    new_list[i] = new_item
                    break
                    
                #if the current item ends with {}, it sets braces to the last 2 characters of that string
                #also strips {} from the current item   
                elif new_list[i].endswith("{}") == True:
                    braces = new_list[i][-2:]
                    new_item = new_list[i].rstrip("{}")
                    new_list[i] = new_item
                    break
                else:
                    i += 1
            
            
        if braces != None:
            braces = name_matches
            #iterates through name_matches
            #for each item in name_matches, it adds the item to new_list and runs execvp on command_name and new_list
            for fname in braces:
                pid = os.fork()
                if pid == 0:
                    try:
                        new_list.append(fname)
                        os.execvp(command_name, new_list)
                    except Exception:
                        print("Error: Unable to start process 'failedprocess {}'".format(fname))
                    
                elif pid == -1:
                    print("ERROR")
            
                else:
                    os.wait()
                
            return 1
        
        #handles the case in which no instance of {} was found
        else:
            pid = os.fork()
            if pid == 0:
                try:
                    os.execvp(command_name, new_list)
                except Exception:
                    print("Error: Unable to start process 'failedprocess'")
            elif pid == -1:
                print("ERROR")
            else:
                os.wait()
            
            return 1
        
    #handles the case in which only the directory is provided
    elif directory != None and regex == None and name == None and command == None:
        printDirectory(directory)
        
    #nandles any other case by exiting with the USAGE message   
    else:
        sys.exit(USAGE)
        return 1
        

#uses os.walk to print all files and subdirectories within the given directory   
def printDirectory(directory):
    print(directory)
    everything = []
        
    for path, subdirectories, files in os.walk(directory):
        for dir in subdirectories:
            everything.append(os.path.join(path, dir))
        for name in files:
            everything.append(os.path.join(path, name))


    everything.sort()
    for i in everything:
        print(i)

    
  
    
if __name__ == "__main__":
    directory = None
    regex = None
    name = None
    command = None
    

    
    i = 1
    while i < len(sys.argv):
        #extracts the regex pattern from the regex arg
        if sys.argv[i].startswith("--regex"):
            regex = sys.argv[i][8:]
            i+=1
        #extracts the name from the name arg
        elif sys.argv[i].startswith("--name"):
            name = sys.argv[i][7:]
            i+=1
        #sets arg to command so long as the directroy already exists   
        elif sys.argv[i].startswith("--") == False and directory != None:
            command = sys.argv[i]
            i+=1
        #sets arg to the directory if it doesn't meet any of the following criteria    
        else:
            directory = sys.argv[i]
            i+=1
            
            
            
    if len(sys.argv) == 1:
        sys.exit(USAGE)        
            
    #handles the case in which both a name and regex pattern are provided    
    elif regex != None and name != None:
        sys.exit(USAGE)
    
    else:
        find(directory, regex, name, command)
        


