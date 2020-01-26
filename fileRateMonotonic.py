# Implementation of Rate Monotonic Algorithm (Cyclic Executive)

import numpy
import random
    
def getIntervals(tasks):
    intervals = numpy.zeros(len(tasks),dtype=int)
    for i,key in enumerate(tasks): intervals[i] = tasks[key]['intrvl']
    return(intervals)

def eachTask_cyclicExecutionCost(period,interval,executionCost):
    return(int((period/interval)*executionCost))
    
def check_conditions(tasks):
    ##print(tasks)
    intervals = getIntervals(tasks).astype(int)
    totalPeriod = numpy.lcm.reduce(intervals)
    totalExecutionCost = 0
    for i,key in enumerate(tasks):
        totalExecutionCost += eachTask_cyclicExecutionCost(totalPeriod,tasks[key]['intrvl'],tasks[key]['wcet'][0])
    ##print(totalPeriod,totalExecutionCost)
    if totalExecutionCost <= totalPeriod: return(True)
    else: return(False)
    
def get_priorities(tasks):
    priority_dict = {}
    for i,key in enumerate(tasks): priority_dict[key] = tasks[key]['intrvl']
    priority_dict = sorted(priority_dict, key=priority_dict.get)
    return(priority_dict)

def dispatch_rm_scheduler(tasks,hyperInterval):
    priorities = get_priorities(tasks)
    totalPeriod = hyperInterval
    taskScheduled = []
    ##print(priorities)
    for item in priorities: tasks[item]['priority'] = priorities.index(item)
    for i in range(totalPeriod):
        for task in tasks:
            if i % tasks[task]['intrvl'] == 0: taskScheduled.append([task,i,tasks[task]['wcet'][0],tasks[task]['priority']])            
    #print(taskScheduled)
    executionQueue = []
    tempQueue = []
    for i in range(totalPeriod):
        for item in taskScheduled:
            if item[1] == i: tempQueue.append(item)
        ##print((tempQueue))
        if len(tempQueue) == 0: executionQueue.append('Halt')
        else:
            tempQueue = sorted(tempQueue, key=lambda x: x[3])
            executionQueue.append(tempQueue[0][0])
            tempQueue[0][2] = tempQueue[0][2] - 1
            if tempQueue[0][2] == 0: tempQueue.pop(0)
    return(executionQueue)
    
def dispatchRateMonotonic(tasks,hyperInterval):
    ##print(tasks)
    conditions_satisfiability = check_conditions(tasks)
    if conditions_satisfiability == True:
        taskExecutionQueue = dispatch_rm_scheduler(tasks,hyperInterval)
        ##print(taskExecutionQueue)
        return(taskExecutionQueue)
    else:
        #print('Conditions Not Satified')
        return(None)
        
def executeRateMonotonic(tasks,exeQueue,hyperInterval):
    taskExe = {}
    for key in tasks:
        tasks[key]['exetime'] = random.choice(tasks[key]['wcet'])
        tasks[key]['counter'] = tasks[key]['exetime']
        taskExe[key] = tasks[key]['exetime']
        #print(tasks[key]['exetime'])
    ##print(exeQueue)
    for i in range(hyperInterval):
        key = exeQueue[i]
        if key != 'Halt':
            for task in tasks:
                if i % tasks[task]['intrvl'] == 0: tasks[task]['counter'] = tasks[task]['exetime']
            #if i % tasks[key]['intrvl'] == 0 or :
                ##print(key)
                #tasks[key]['counter'] = tasks[key]['exetime']
            if tasks[key]['counter'] == 0:
                exeQueue[i] = 'Halt'
            else:
                tasks[key]['counter'] = tasks[key]['counter'] - 1
    ##print(exeQueue)
    return(exeQueue,taskExe)