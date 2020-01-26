# Implementation of Global EDF Algorithm (Earliest Deadline First)
import random

def getScheduledTasks(tasks,totalPeriod):
    taskScheduled = []
    taskExe = {}
    for task in tasks:
        tasks[task]['exetime'] = random.choice(tasks[task]['wcet'])
        taskExe[task] = tasks[task]['exetime']
    for i in range(totalPeriod):
        for task in tasks:
            if (totalPeriod - i)> tasks[task]['intrvl']:
                if i % tasks[task]['intrvl'] == 0:
                    deadline = i + tasks[task]['intrvl'] - 1
                    exeTime = tasks[task]['exetime']
                    flag = 0
                    taskScheduled.append([task,i,exeTime,deadline,flag])            
    taskScheduled = sorted(taskScheduled, key = lambda x: x[3])
    for i in range(len(taskScheduled)): taskScheduled[i].append(i)
    return(taskScheduled,taskExe)
    

def dispatch_gEDF(tasks,hyperInterval,pushedQ1,pushedQ2):
    totalPeriod = hyperInterval
    taskScheduled,taskExe = getScheduledTasks(tasks,totalPeriod)   
    ##print(taskScheduled)
    for i in range(totalPeriod):
        ##print(len(taskScheduled))
        ##print(taskScheduled[len(taskScheduled)-1])
        if len(taskScheduled) > 1:
            if pushedQ1[i] == 'Halt':
                if taskScheduled[0][4] != 2:
                    if taskScheduled[1][4] != 1:
                        pushedQ1[i] = taskScheduled[0][0]
                        taskScheduled[0][2] = taskScheduled[0][2] - 1
                        if taskScheduled[0][2] == 0:
                            taskScheduled.pop(0)
                        else:
                            if i+1 != totalPeriod:
                                if pushedQ1[i+1] == 'Halt': taskScheduled[0][4] = 1
                                else: taskScheduled[0][4] = 0
                else:
                    pushedQ1[i] = taskScheduled[1][0]
                    taskScheduled[1][2] = taskScheduled[1][2] - 1
                    if taskScheduled[1][2] == 0:
                        taskScheduled.pop(1)
                    else:
                        if i+1 != totalPeriod:
                            if pushedQ1[i+1] == 'Halt': taskScheduled[1][4] = 1
                            else: taskScheduled[1][4] = 0
        if len(taskScheduled) > 1:                                          
            if pushedQ2[i] == 'Halt':
                if taskScheduled[0][4] != 1:
                    if taskScheduled[1][4] != 2:
                        pushedQ2[i] = taskScheduled[0][0]
                        taskScheduled[0][2] = taskScheduled[0][2] - 1
                        if taskScheduled[0][2] == 0:
                            taskScheduled.pop(0)
                        else:
                            if i+1 != totalPeriod:
                                if pushedQ2[i+1] == 'Halt': taskScheduled[0][4] = 1
                                else: taskScheduled[0][4] = 0
                else:
                    pushedQ2[i] = taskScheduled[1][0]
                    taskScheduled[1][2] = taskScheduled[1][2] - 1
                    if taskScheduled[1][2] == 0:
                        taskScheduled.pop(1)
                    else:
                        if i+1 != totalPeriod:
                            if pushedQ2[i+1] == 'Halt': taskScheduled[1][4] = 1
                            else: taskScheduled[1][4] = 0
        if len(taskScheduled) == 1:
            if pushedQ1[i] == 'Halt':
                if taskScheduled[0][4] != 2:
                    pushedQ1[i] = taskScheduled[0][0]
                    taskScheduled[0][2] = taskScheduled[0][2] - 1
                    if taskScheduled[0][2] == 0:
                        taskScheduled.pop(0)
                    else:
                        if i+1 != totalPeriod:
                            if pushedQ1[i+1] == 'Halt': taskScheduled[0][4] = 1
                            else: taskScheduled[0][4] = 0
        if len(taskScheduled) == 1:
            if pushedQ2[i] == 'Halt':
                if taskScheduled[0][4] != 1:
                    pushedQ2[i] = taskScheduled[0][0]
                    taskScheduled[0][2] = taskScheduled[0][2] - 1
                    if taskScheduled[0][2] == 0:
                        taskScheduled.pop(0)
                    else:
                        if i+1 != totalPeriod:
                            if pushedQ2[i+1] == 'Halt': taskScheduled[0][4] = 1
                            else: taskScheduled[0][4] = 0
        if len(taskScheduled) == 0: break
    return(pushedQ1,pushedQ2,taskExe)