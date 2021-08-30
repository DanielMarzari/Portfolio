# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 02:33:42 2020

@author: Daniel Marzari
"""

#ACM ICPC 2016 Problem M: What Really Happened on Mars?

#-------------------------------RESOURCES--------------------------------------
class resource:
    def __init__(self, id):
        #resouce id
        self.id = id
        #not locked yet
        self.islocked = False
        
    def setpc(self):
        global input_processes
        #base priority set (pc = highest base priority that locks this resource)
        bps = [p.get_resource_priority(self.id) for p in input_processes]
        #set priority ceiling
        self.priority_ceil = max(bps)
      
    def lock(self, process):
        #lock the resource and identify the process locking it
        self.locking_process = process
        self.islocked = True

    def unlock(self):
        #unlock this resource
        self.locking_process = None
        self.islocked = False
        
        
#-------------------------------PROCESSES--------------------------------------
class process:
    def __init__(self, args):
        #set process data
        self.stime = int(args[0])
        self.base_priority = int(args[1])
        self.cnt = int(args[2])
        self.cmds = args[3:]
        #current priority set to bp until changed later
        self.current_priority = self.base_priority
        #init
        self.incomplete = True
        self.ftime = 0
    
    def get_resource_priority(self, id):
        #find what resources are used
        if (''.join(self.cmds).find("L%s"%id) > -1):
            return self.base_priority
        else:
            return 0
    
    def resetstats(self):
        #reset cp and blocked for the next cycle
        self.current_priority = self.base_priority
        self.blocked = False
    
    def setblocked(self):
        #set the processes as blocked
        self.blocked = True
    
    def updatecp(self, inc):
        #increase the current priority of this process
        self.current_priority += inc
    
    def nextisRes(self):
        #find out if the next cmd is a lock command
        self.nextcmd = self.cmds[0]
        if(self.nextcmd[0] == "L"):
            #set nextcmd to the number of the resource being locked
            self.nextcmd = int(self.nextcmd[1:])
            return True
        else:
            return False
    
    def execute(self):
        #get next command
        crnt_cmd = self.cmds.pop(0)
        
        #break down command into components
        letter = crnt_cmd[0]
        number = int(crnt_cmd[1:])
        
        if(letter == 'L'):
            #lock a given resource
            resources[number].lock(self)
            #always succeeds and takes no time
            status = 0
        
        if(letter == 'U'):
            #unlock a given resource
            resources[number].unlock()
            #always succeeds and takes no time
            status = 0
        
        if(letter == 'C'):  
            if(number > 1):
                #put the remaining compute comands back
                self.cmds.insert(0, "C%s" % (number-1))
            #always succeeds and takes 1us
            status = 1
        
        #check if wthis process has completed
        if(len(self.cmds) == 0):
            #save details
            self.incomplete = False
            self.ftime = clock + status
        
        #return the run time of this process
        return status

#---------------------------------CYCLE----------------------------------------
def cycle():        
    global clock, resources
    #get running tasks by priority
    running = [p for p in input_processes if (p.stime <= clock) and p.incomplete]
    
    if running:        
        #reset stats
        for r in running:
            r.resetstats()
            
        #update current priority and blocking
        for r in running:
            isblocked(r)
        
        #get all unblocked running processes
        unblocked = [r for r in running if not r.blocked]
        #first base then current to resolve order
        unblocked.sort(key = lambda e: e.base_priority, reverse=True)
        unblocked.sort(key = lambda e: e.current_priority, reverse=True)
        
        #run highest priority process
        if(unblocked):
            #run the process (returns time in us)
            clock += unblocked[0].execute()
        cycle()
        
#-------------------------------BLOCKING---------------------------------------

def isblocked(process):
    #check only if the next command is L
    if(process.nextisRes()):
        global resources
        #rule 1: locking
        if(resources[process.nextcmd].islocked):
            #blocked by another task using the resource
            process.setblocked()
            #increase the current priority of the blocking process
            resources[process.nextcmd].locking_process.updatecp(process.current_priority)
            #return true because we blocked a process
            return True
        else:
            #rule 2: blocking
            locked = []
            for l in resources.values():
                #get the resource if it is locked, isn't the resource we are looking for, and isn't owned by us
                if (l.islocked) and (l.id != process.nextcmd) and (l.locking_process != process):
                    locked.append(l)
            #if any resources fall into that group continue
            if(locked):
                #sort by the priority of the resource
                locked.sort(key=lambda e: e.priority_ceil)
                #see if that priority is >= the process priority
                if(locked[0].priority_ceil >= process.current_priority):
                    #block the process
                    process.setblocked()
                    #increase the current priority of the blocking process
                    locked[0].locking_process.updatecp(process.current_priority) ##
                    #return true because we blocked a process
                    return True
            else:
                #not blocked resource
                return False


#---------------------------------INIT-----------------------------------------
#number of inputs
pro_cnt, res_cnt = [int(v) for v in input("Processes and Resources: ").split(" ")]

#initialize resources
resources = {}
for r in range(1, res_cnt+1):
    resources[r] = resource(r)

#get process data
input_processes = []
for i in range(1, pro_cnt+1):
    data = input("Input %s: " % i).split(" ")
    input_processes.append(process(data))

#calculate new pc
for r in resources.values():
    r.setpc()

#start at the first process that runs (no need to wait)
clock = min([p.stime for p in input_processes])

#begin the cycle (will continue until all processes complete)
cycle()

#output runtimes
for p in input_processes:
    print("%s" % p.ftime)