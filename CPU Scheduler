from operator import attrgetter
from this import d
import copy
import queue

ZERO_INDEX = 0

class PROCESS: 
  def __init__(self, id=None, burst=None, arrival=None, priority=None, turnaround=None, waiting=None, rem_burst=None, ratio=None):
    self.id = id
    self.burst = burst
    self.arrival = arrival
    self.priority = priority
    self.turnaround = turnaround
    self.waiting = waiting

    self.rem_burst = rem_burst
    self.ratio = ratio


def Make_Gantt(gantt, process, time): # list of gantt char is call by reference?   
    for i in range(time):
        gantt.append(str(process))

def Output_Gantt(outfile, gantt):
    for i in gantt:
        if int(i) == -1:
            str = "-"
        elif int(i) > 9:
            str = chr(int(i)+55)
        else:
            str = i

        outfile.write(str)

    outfile.write('\n')  

def Store_Process_Info(process_list, id, turnaround, waiting):
    isFound = False
    i = 0
    while not isFound:
        if process_list[i].id == id:
            process_list[i].turnaround = turnaround
            process_list[i].waiting = waiting
            isFound = True
        i+=1

def FCFS(process_list, outfile):
    
    gantt = []
    curTime = 0
   
    for j in range(len(process_list)):
        while process_list[j].arrival > curTime:
            gantt.append(-1)
            curTime+=1
        
        Make_Gantt(gantt, process_list[j].id, process_list[j].burst)
        curTime = curTime + process_list[j].burst

        process_list[j].turnaround = curTime - process_list[j].arrival 
        process_list[j].waiting = process_list[j].turnaround - process_list[j].burst

    outfile.write("==        FCFS==\n")    
    Output_Gantt(outfile, gantt)
           
def RR(process_list, timeslice, outfile):
    gantt = []
    curTime = 0
    process = queue.Queue()
    ready_queue = queue.Queue()

    for i in process_list:
        process.put(i)

    buffer = process.get() # first process
    while buffer.arrival > curTime:
        gantt.append(-1)
        curTime+=1

    lastProcess = False

    while process.qsize() + ready_queue.qsize() > 0:
        
        while lastProcess == False and buffer.arrival <= curTime:
            ready_queue.put(buffer)                # process arrived, put into ready_queue
            if process.qsize() == 0 :
                lastProcess = True
            if process.qsize() != 0:
                buffer = process.get()
   
        if ready_queue.qsize() != 0:                # is any process in the ready queue
            run_process = ready_queue.get()         # run_process use cpu
            if run_process.rem_burst > timeslice:
                run_process.rem_burst = run_process.rem_burst - timeslice
                curTime = curTime + timeslice
                Make_Gantt(gantt, run_process.id, timeslice)
            else: # remaining burst time <= timeslice    DONE!
                curTime = curTime + run_process.rem_burst
                Make_Gantt(gantt, run_process.id, run_process.rem_burst)
                run_process.rem_burst = 0
                turnaround = curTime - run_process.arrival
                waiting = turnaround - run_process.burst
                Store_Process_Info(process_list, run_process.id, turnaround, waiting)           
        
            while lastProcess == False and buffer.arrival <= curTime: # check is any process arrived, during run_process running
                ready_queue.put(buffer)
                if process.qsize() == 0:
                    lastProcess = True
                if process.qsize() != 0:
                    buffer = process.get()
        
            if run_process.rem_burst != 0:           # run_process has't done, put into ready_queue
                ready_queue.put(run_process)

        if ready_queue.qsize() == 0 and process.qsize() != 0:
            gantt.append(-1)
            curTime+=1
  
    outfile.write("==          RR==\n")
    Output_Gantt(outfile, gantt)

        
def SRTF(process_list, outfile):    
    gantt = []
    process = []
    ready_queue = []
    curTime = 0  
    next_arrival = 0
    has_next_process = True

    for j in process_list:
        process.append(j)

    while process[ZERO_INDEX].arrival > curTime:
        gantt.append(-1)
        curTime+=1

    while len(process) + len(ready_queue) > 0:

        while len(process) != 0 and process[ZERO_INDEX].arrival <= curTime: # process arrived, put into ready_queue
            ready_queue.append(process[ZERO_INDEX])
            process.pop(ZERO_INDEX)                                         # remove first process in process[]

        if len(process) != 0:                                               # store next process arrival time
            next_arrival = process[ZERO_INDEX].arrival
        else: # All process arrived
            has_next_process = False
        ready_queue.sort(key = attrgetter('rem_burst', 'arrival', 'id'))

        if len(ready_queue) != 0:
            run_process = ready_queue[ZERO_INDEX]

            while (has_next_process == False or next_arrival > curTime) and len(ready_queue) != 0 and run_process.rem_burst != 0:
                # No process arrive && ready_queue has process && the run_process still has burst time
                Make_Gantt(gantt, run_process.id, 1)
                run_process.rem_burst = run_process.rem_burst - 1
                curTime = curTime + 1

            ready_queue.pop(ZERO_INDEX) 

            if run_process.rem_burst != 0: # preemptive -> put into ready_queue again
                ready_queue.append(run_process)
            else:
                turnaround = curTime - run_process.arrival
                waiting = turnaround - run_process.burst                
                Store_Process_Info(process_list, run_process.id, turnaround, waiting) 
            

        if len(ready_queue) == 0 and len(process) != 0:
            gantt.append(-1)
            curTime+=1
    
    outfile.write("==        SRTF==\n")
    Output_Gantt(outfile, gantt)

# ----------------------------------------------- PPRR -----------------------------------------------

def Priority_Preemptive(process_list, ready_queue, run_process, curTime):
    '''check if there is any arrived process's priorty is smaller than run_process
       If arrived process's priority is smaller
       then move process in run_process to ready_queue and put arrived process into run_process'''

    if len(ready_queue) != 0:
        if run_process[ZERO_INDEX].priority > ready_queue[ZERO_INDEX].priority:
            i = 0
            while len(ready_queue) > i and run_process[ZERO_INDEX].priority >= ready_queue[i].priority:
                i+=1
            
            if run_process[ZERO_INDEX].rem_burst == 0:
                # don't need to put run_process into ready_queue
                turnaround = curTime - run_process[ZERO_INDEX].arrival
                waiting = turnaround - run_process[ZERO_INDEX].burst                
                Store_Process_Info(process_list, run_process[ZERO_INDEX].id, turnaround, waiting) 
                run_process.pop(ZERO_INDEX)
                run_process.append(ready_queue[ZERO_INDEX])
                ready_queue.pop(ZERO_INDEX)
            
            else:           
                ready_queue.insert(i, run_process[ZERO_INDEX])
                run_process.pop(ZERO_INDEX)
                run_process.append(ready_queue[ZERO_INDEX])
                ready_queue.pop(ZERO_INDEX)

            return True
        else:
            return False
    else:
        return False

def Check_Arrived(process, ready_queue, run_process, curTime):
    ''' Check if any process arrived, put it into ready_queue,
        If run_process is empty, put ready_queue[ZERO] in it'''
    while len(process) > 0 and process[ZERO_INDEX].arrival <= curTime:
        i = 0
        while len(ready_queue) > i and ready_queue[i].priority <= process[ZERO_INDEX].priority: # find place to insert arrived process
            i+=1
        
        ready_queue.insert(i, process[ZERO_INDEX])
        process.pop(ZERO_INDEX)

    if len(run_process) == 0 and len(ready_queue) != 0:
        run_process.append(ready_queue[ZERO_INDEX])
        ready_queue.pop(ZERO_INDEX)

def PPRR(process_list, timeslice, outfile):
    gantt = []
    process = []
    ready_queue = []
    curTime = 0
    isPreemptive = False
    run_process = []


    for i in process_list:
        process.append(i)
    
    while process[ZERO_INDEX].arrival > curTime: # if first process hasn't arrived
        gantt.append(-1)
        curTime+=1
    
    while len(process) + len(ready_queue) + len(run_process) > 0 :

        Check_Arrived(process, ready_queue, run_process, curTime)

        if len(ready_queue) + len(run_process) > 0:

            if run_process[ZERO_INDEX].rem_burst < timeslice:
                while run_process[ZERO_INDEX].rem_burst > 0:
                    run_process[ZERO_INDEX].rem_burst = run_process[ZERO_INDEX].rem_burst - 1
                    curTime = curTime + 1
                    Make_Gantt(gantt, run_process[ZERO_INDEX].id, 1)
                    Check_Arrived(process, ready_queue, run_process, curTime)
                    isPreemptive = Priority_Preemptive(process_list, ready_queue, run_process, curTime)
                    if isPreemptive:
                        break                  

            else:
                i = 0
                while i < timeslice:
                    run_process[ZERO_INDEX].rem_burst = run_process[ZERO_INDEX].rem_burst - 1
                    curTime = curTime + 1
                    Make_Gantt(gantt, run_process[ZERO_INDEX].id, 1)

                    Check_Arrived(process, ready_queue, run_process, curTime)
                    isPreemptive= Priority_Preemptive(process_list, ready_queue, run_process, curTime)
                    if isPreemptive:
                        break
                    i+=1
            
            if isPreemptive == False:
                if run_process[ZERO_INDEX].rem_burst != 0:
                    i = 0
                    while len(ready_queue) > i and ready_queue[i].priority <= run_process[ZERO_INDEX].priority:      
                        i+=1
                    ready_queue.insert(i, run_process[ZERO_INDEX])        
                else:
                    turnaround = curTime - run_process[ZERO_INDEX].arrival
                    waiting = turnaround - run_process[ZERO_INDEX].burst                
                    Store_Process_Info(process_list, run_process[ZERO_INDEX].id, turnaround, waiting) 
                
                if len(ready_queue) != 0:
                    run_process.append(ready_queue[ZERO_INDEX])
                    ready_queue.pop(ZERO_INDEX)
                
                run_process.pop(ZERO_INDEX)
    
        
        if len(process) != 0 and len(ready_queue) == 0 and len(run_process) == 0:
            gantt.append(-1)
            curTime+=1
    
    outfile.write("==        PPRR==\n")
    Output_Gantt(outfile, gantt)

# ----------------------------------------------- HRRN -----------------------------------------------

def Ratio_Sort(ready_queue):

    n = len(ready_queue)
    for i in range(n-1):                   
        for j in range(n-i-1):             
            if ready_queue[j].ratio < ready_queue[j+1].ratio:       
                ready_queue[j], ready_queue[j+1] = ready_queue[j+1], ready_queue[j]

            elif ready_queue[j].ratio == ready_queue[j+1].ratio: 
                if ready_queue[j].arrival > ready_queue[j+1].arrival:
                    ready_queue[j], ready_queue[j+1] = ready_queue[j+1], ready_queue[j]

                elif ready_queue[j].arrival == ready_queue[j+1].arrival:
                    if ready_queue[j].id > ready_queue[j+1].id:
                        ready_queue[j], ready_queue[j+1] = ready_queue[j+1], ready_queue[j]
            
def HRRN(process_list, outfile):
    process = []
    ready_queue = []
    gantt = []
    
    curTime = 0
    for i in process_list:
        process.append(i)
    
    while len(process) + len(ready_queue) != 0:
        while len(process) != 0 and process[ZERO_INDEX].arrival <= curTime: # process arrived, put into ready_queue
            process[ZERO_INDEX].ratio = float( curTime - process[ZERO_INDEX].arrival + process[ZERO_INDEX].burst ) / float(process[ZERO_INDEX].burst)
            ready_queue.append(process[ZERO_INDEX])
            Ratio_Sort(ready_queue)
            process.pop(ZERO_INDEX)       

        if len(ready_queue) != 0:
            run_process = ready_queue[ZERO_INDEX]                                      
            ready_queue.pop(ZERO_INDEX)

            Make_Gantt(gantt, run_process.id, run_process.burst)
            curTime = curTime + run_process.burst

            turnaround = curTime - run_process.arrival 
            waiting = turnaround - run_process.burst
            Store_Process_Info(process_list, run_process.id, turnaround, waiting)

            if len(ready_queue) != 0: # update response ratio
                for i in ready_queue:
                    i.ratio = float( curTime - i.arrival + i.burst ) / float(i.burst)

            while len(process) != 0 and process[ZERO_INDEX].arrival <= curTime: # process arrived, put into ready_queue
                process[ZERO_INDEX].ratio = float( curTime - process[ZERO_INDEX].arrival + process[ZERO_INDEX].burst ) / float(process[ZERO_INDEX].burst)
                ready_queue.append(process[ZERO_INDEX])
                process.pop(ZERO_INDEX)  

            Ratio_Sort(ready_queue)

        if len(process) != 0 and len(ready_queue) == 0:
            gantt.append(-1)
            curTime+=1

    outfile.write("==        HRRN==\n")
    Output_Gantt(outfile, gantt)

def WriteFile_Single(outfile, method, process_list):
    outfile.write("===========================================================\n\n")
    outfile.write("Waiting Time\n")
    outfile.write("ID" + "\t" + method + "\n")
    outfile.write("===========================================================\n")

    # write waiting time into file
    for i in range(len(process_list)):
        outfile.write(str(process_list[i].id) + "\t")
        outfile.write(str(process_list[i].waiting) + "\n")

    
    outfile.write("===========================================================\n\n")
    outfile.write("Turnaround Time\n")
    outfile.write("ID" + "\t" + method + "\n")
    outfile.write("===========================================================\n")

    # write turnaround time into file
    for i in range(len(process_list)):
        outfile.write(str(process_list[i].id) + "\t")
        outfile.write(str(process_list[i].turnaround) + "\n")
 

    outfile.write("===========================================================\n\n") 

def WriteFile_ALL(outfile, process_list1, process_list2, process_list3, process_list4, process_list5):
    outfile.write("===========================================================\n\n")
    outfile.write("Waiting Time\n")
    outfile.write("ID	FCFS	RR	SRTF	PPRR	HRRN\n")
    outfile.write("===========================================================\n")

    # write waiting time into file
    for i in range(len(process_list1)):
        outfile.write(str(process_list1[i].id) + "\t")
        outfile.write(str(process_list1[i].waiting) + "\t" + str(process_list2[i].waiting) + "\t")
        outfile.write(str(process_list3[i].waiting) + "\t" + str(process_list4[i].waiting) + "\t")
        outfile.write(str(process_list5[i].waiting) + "\n")
    
    outfile.write("===========================================================\n\n")
    outfile.write("Turnaround Time\n")
    outfile.write("ID	FCFS	RR	SRTF	PPRR	HRRN\n")
    outfile.write("===========================================================\n")

    # write turnaround time into file
    for i in range(len(process_list1)):
        outfile.write(str(process_list1[i].id) + "\t")
        outfile.write(str(process_list1[i].turnaround) + "\t" + str(process_list2[i].turnaround) + "\t")
        outfile.write(str(process_list3[i].turnaround) + "\t" + str(process_list4[i].turnaround) + "\t")
        outfile.write(str(process_list5[i].turnaround) + "\n")  

    outfile.write("===========================================================\n\n") 



# -----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    keep = True
    while keep:
        file_exist = False
        print("### Enter \"EXIT\" can exit ###")
        filename = input("Please input a filename(.txt): ")
        if filename == "EXIT":
            keep = False

        try:
            file = open(filename, "r")
            file_exist = True
        except FileNotFoundError:
            if filename != "EXIT":
                print("Sorry! The file "+filename+" can't find.")
    
        if file_exist:   
            i = 0 
            source_input = file.read().split()
            method = source_input[i]           # store method number
            i+=1
            timeslice = int(source_input[i])   # store time slice (Need to convert to int?)
            i+=1

            # read the title (ID, CPU Burst, Arrival Time, Priority)
            while not( source_input[i] >= '0' and source_input[i] <= '9' ):
                i+=1
      
            process_list = []
            for j in range(i, len(source_input), 4):
                if j+3 < len(source_input):
                    process_list.append(PROCESS(int(source_input[j]), int(source_input[j+1]), int(source_input[j+2]), int(source_input[j+3]), 0, 0, int(source_input[j+1]), 0))
                
            # attrgetter for many keys to sort (e.g. arrival time -> id)
            process_list.sort(key = attrgetter('arrival', 'id'))

            outfile = open("out_"+filename, "w")

            if method == "1":
                outfile.write("FCFS\n")
                process_list1 = copy.deepcopy(process_list)
                FCFS(process_list1, outfile) 
                process_list1.sort(key = attrgetter('id'))
                WriteFile_Single(outfile, "FCFS", process_list1)
                outfile.close()
                print("Method 1 Finish!")
        
            elif method == "2":
                outfile.write("RR\n")
                process_list2 = copy.deepcopy(process_list)
                RR(process_list2, timeslice, outfile)
                process_list2.sort(key = attrgetter('id'))
                WriteFile_Single(outfile, "RR", process_list2)
                outfile.close()
                print("Method 2 Finish!")

            elif method == "3":
                outfile.write("SRTF\n")
                process_list3 = copy.deepcopy(process_list)
                SRTF(process_list3, outfile)
                process_list3.sort(key = attrgetter('id'))
                WriteFile_Single(outfile, "SRTF", process_list3)
                outfile.close()
                print("Method 3 Finish!")
        
            elif method == "4":
                outfile.write("Priority RR\n")
                process_list4 = copy.deepcopy(process_list)
                PPRR(process_list4, timeslice, outfile)
                process_list4.sort(key = attrgetter('id'))
                WriteFile_Single(outfile, "PPRR", process_list4)
                outfile.close()
                print("Method 4 Finish!")

            elif method == "5":
                outfile.write("HRRN\n")
                process_list5 = copy.deepcopy(process_list)
                HRRN(process_list5, outfile)
                process_list5.sort(key = attrgetter('id'))
                WriteFile_Single(outfile, "HRRN", process_list5)
                outfile.close()
                print("Method 5 Finish!")
         
            elif method == "6":
                outfile.write("All\n")
                process_list1 = copy.deepcopy(process_list)
                FCFS(process_list1, outfile) 
                process_list1.sort(key = attrgetter('id'))

                process_list2 = copy.deepcopy(process_list)
                RR(process_list2, timeslice, outfile)
                process_list2.sort(key = attrgetter('id'))

                process_list3 = copy.deepcopy(process_list)
                SRTF(process_list3, outfile)
                process_list3.sort(key = attrgetter('id'))

                process_list4 = copy.deepcopy(process_list)
                PPRR(process_list4, timeslice, outfile)
                process_list4.sort(key = attrgetter('id'))

                process_list5 = copy.deepcopy(process_list)
                HRRN(process_list5, outfile)
                process_list5.sort(key = attrgetter('id'))

                WriteFile_ALL(outfile, process_list1, process_list2, process_list3, process_list4, process_list5)

                outfile.close()
                print("Method 6 Finish!")
            
            else:
                print("Sorry! No this option. ")

            
 

