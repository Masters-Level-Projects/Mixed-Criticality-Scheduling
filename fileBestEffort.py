# Implementation of FIFO Algorithm (Best Effort)
from copy import deepcopy
import numpy as np


#def printdebuginfo(cpu1, cpu2, msg):
    #print(msg)
    #print('The queue for CPU 1:')
    #print(cpu1)
    #print('The queue for CPU 2:')
    #print(cpu2)


def dispatchBestEffort(cpu1, cpu2, fifo_d, hyperinterval):
    #printdebuginfo(cpu1, cpu2, 'Before FIFO')
    # the following data structure will merely see if there are more tasks generated than allowed
    gen_tasks = {}
    gen_possible = {}
    for task in fifo_d:
        gen_tasks[task] = 1
        gen_possible[task] = int(np.floor(hyperinterval/fifo_d[task]['intrvl']))

    # make fifo level task queue
    fifo_que = []
    for p in fifo_d:
        # each entry of process queue: [process name, interval, wcet, wcet copy]
        fifo_que.append([p, fifo_d[p]['intrvl'], fifo_d[p]['wcet'][0], fifo_d[p]['wcet'][0]])

    # sort and copy to a new queue, we will change this
    fifo_que_new = deepcopy(fifo_que)
    fifo_que_new = sorted(fifo_que_new, key=lambda x: x[1])

    time_counter = 0

    proc1 = fifo_que_new.pop(0)     # get two processes from fifo queue
    proc2 = fifo_que_new.pop(0)

    while time_counter < len(cpu1) or time_counter < len(cpu2):
        # update fifo queue, add as many instances of each process in que as their intervals have elapsed upto this time since last interval passing time

        # check if at current time CPU1 is idle, here cpu1 is one which has earlier idle/halt time
        if time_counter < len(cpu1) and cpu1[time_counter] == 'Halt':      # halt is idle
            if proc1[3] > 0:        # proceed only if remaining execution time is not zero
                proc1[3] -= 1       # update execution time of process
                cpu1[time_counter] = proc1[0]
            if proc1[3] == 0 and len(fifo_que_new) != 0: # if current process exhausted and more processes available
                proc1 = fifo_que_new.pop(0)
        elif time_counter < len(cpu1) and cpu1[time_counter] != 'Halt' and proc1[3] != proc1[2] and proc1[3] > 0:
            fifo_que_new.append(deepcopy(proc1))
            proc1 = fifo_que_new.pop(0)

        # check if at current time CPU2 is idle
        if time_counter < len(cpu2) and cpu2[time_counter] == 'Halt':
            if proc2[3] > 0:
                proc2[3] -= 1
                cpu2[time_counter] = proc2[0]
            if proc2[3] == 0 and len(fifo_que_new) != 0:
                proc2 = fifo_que_new.pop(0)
        elif time_counter < len(cpu2) and cpu2[time_counter] != 'Halt' and proc2[3] != proc2[2] and proc2[3] > 0:
            fifo_que_new.append(deepcopy(proc2))
            proc2 = fifo_que_new.pop(0)

        time_counter += 1
        for proc in deepcopy(fifo_que):
            if time_counter % proc[1] == 0 and gen_tasks[proc[0]] < gen_possible[proc[0]]:
                fifo_que_new.append(proc)       # just enque one instance of each process whose interval has passed.
                gen_tasks[proc[0]] += 1
                if proc1[3] == 0 and len(fifo_que_new) != 0:
                    proc1 = fifo_que_new.pop(0)
                if proc2[3] == 0 and len(fifo_que_new) != 0:
                    proc2 = fifo_que_new.pop()
    #printdebuginfo(cpu1, cpu2, 'Before cleanup')
    # In the following logic, we will check if any outstanding process is remaining that could not
    # be completed within allowed time, if yes, remove all occurrences of that process from the
    # schedule
    if proc1 is not None and proc1[3] != 0:
        loc = len(cpu1) - 1
        while proc1[2] - proc1[3] != 0:
            if loc < len(cpu1) and cpu1[loc] == proc1[0]:
                cpu1[loc] = 'Halt'
                proc1[3] += 1
            loc -= 1
    if proc2 is not None and proc2[3] != 0:
        loc = len(cpu2) - 1
        while proc2[2] - proc2[3] != 0:
            if loc < len(cpu2) and cpu2[loc] == proc2[0]:
                cpu2[loc] = 'Halt'
                proc2[3] += 1
            loc -= 1
    #printdebuginfo(cpu1, cpu2, 'After Cleanup')
    ##print(gen_tasks)
    return cpu1, cpu2
