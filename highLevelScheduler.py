from fileRateMonotonic import dispatchRateMonotonic, executeRateMonotonic
from fileGlobalEDF import dispatch_gEDF
from fileBestEffort import dispatchBestEffort
import numpy
import collections
from itertools import groupby
import matplotlib
from matplotlib.collections import LineCollection
#import pylab as pl
import matplotlib.pyplot as plt
#from random import sample
import pandas as pd

def readData(filename):
    lc = 1
    diction = {}
    with open (filename, 'r') as fin:
        for line in fin:
            if lc == 1:
                lc += 1
                continue
            else:
                crit, tsk, intrvl, E3, E2, E1 = line.strip().split()
                # assuming each task is unique
                wcet = [int(x) for x in (E3, E2, E1) if int(x) > 0]

                if crit not in diction:
                    diction[crit] = {}
                diction[crit][tsk] = {'intrvl': int(intrvl), 'wcet': wcet}
    return diction

def getHyperInterval(rm_tasks):
    wcet_perprocess = []
    for key in rm_tasks:
        wcet_perprocess.append(rm_tasks[key]['intrvl'])
    return(numpy.lcm.reduce(numpy.asarray(wcet_perprocess)))
    
def getProcessorWiseRMTasks(rm_tasks):
    rm_tasks_processor1 = {}
    rm_tasks_processor2 = {}
    for i,key in enumerate(rm_tasks):
        if i % 2 == 0: rm_tasks_processor1[key] = rm_tasks[key]
        else: rm_tasks_processor2[key] = rm_tasks[key]
    return rm_tasks_processor1, rm_tasks_processor2

def scheduleCriticalitiy1Scheduler(rm_tasks,hyperInterval):
    rm_tasks_processor1, rm_tasks_processor2 = getProcessorWiseRMTasks(rm_tasks)
    rmQueue1 = dispatchRateMonotonic(rm_tasks_processor1,hyperInterval)
    rmQueue2 = dispatchRateMonotonic(rm_tasks_processor2,hyperInterval)
    executeQueueRM1, crit1TaskTimeP1 = executeRateMonotonic(rm_tasks_processor1,rmQueue1,hyperInterval)
    executeQueueRM2, crit1TaskTimeP2 = executeRateMonotonic(rm_tasks_processor2,rmQueue2,hyperInterval)
    return executeQueueRM1, executeQueueRM2, crit1TaskTimeP1, crit1TaskTimeP2

def getTaskIntervals(taskExecutionQueue):
    taskClusters = groupby(taskExecutionQueue)
    distribution = [(value, sum(1 for _ in cluster)) for value, cluster in taskClusters]
    ##print(distribution)
    taskIntervals = []
    intervalSeperator = 0
    for item in distribution:
        taskIntervals.append([item[0],intervalSeperator,item[1]+intervalSeperator])
        intervalSeperator += item[1]
    return(taskIntervals)
    
def plotGanttChart(intervals,colorList,x_row,y_column,pNo,max_time):
    lineSegments = []
    max_time = int(max_time + 0.05*max_time)
    min_time = int(0 - 0.05*max_time)
    for item in intervals:
        y_val = y_column.index(item[0]) + 1
        x_val_low = item[1]
        x_val_high = item[2]
        segment = [(x_val_low,y_val),(x_val_high,y_val)]
        lineSegments.append(segment)
    label_index = list(range(len(y_column)))
    for i in range(len(label_index)): label_index[i] += 1
    segmentColor = []
    for item in lineSegments:
        segmentColor.append(colorList[item[0][1]-1])
    fig, ax = plt.subplots()
    plt.yticks(label_index, y_column)
    plotLineSegment = LineCollection(lineSegments, colors=segmentColor, linewidths=10)
    plt.ylim(0,len(label_index))
    plt.xlim(min_time,max_time)
    plt.xlabel('Duration')
    plt.ylabel('Tasks')
    ax.add_collection(plotLineSegment)
    ax.grid(color='g',linestyle=':')
    ax.margins(0.1)
    ax.set_title('Task Scheduling Chart for Processor ' + str(pNo))
    plt.savefig('tsp'+str(pNo)+'.png')
    
if __name__ == '__main__':
    dataSchedule = readData('schedulingData.txt')
    ##print(dataSchedule)
    numberOfProcessor = 2
    rm_tasks = dataSchedule['1']
    hyperInterval = getHyperInterval(rm_tasks)
    #print('Scheduling Length is ' + str(hyperInterval))
    proc1qCrit1, proc2qCrit1, crit1TaskTimeP1, crit1TaskTimeP2 = scheduleCriticalitiy1Scheduler(rm_tasks,hyperInterval)
    #print('Post Critical Level 1')
    #print(collections.Counter(proc1qCrit1))
    #print(collections.Counter(proc2qCrit1))
    gEDF_tasks = dataSchedule['2']
    proc1qCrit2, proc2qCrit2, crit2TaskTime = dispatch_gEDF(gEDF_tasks,hyperInterval,proc1qCrit1, proc2qCrit1)
    #print('Post Critical Level 2')
    ##print(collections.Counter(proc1qCrit2))
    ##print(collections.Counter(proc2qCrit2))
    fifo_tasks = dataSchedule['3']
    proc1qCrit3, proc2qCrit3 = dispatchBestEffort(proc1qCrit2,proc2qCrit2,fifo_tasks, hyperInterval)
    ##print('Post Critical Level 3')
    ##print(collections.Counter(proc1qCrit3))
    ##print(collections.Counter(proc2qCrit3)) 
    p1_taskIntervals = getTaskIntervals(proc1qCrit3)
    p2_taskIntervals = getTaskIntervals(proc2qCrit3)
    
    x_row = list(range(hyperInterval))
    y_column = []
    for key in dataSchedule:
        for secKey in dataSchedule[key]: y_column.append(secKey)
    y_column.append('Halt')
    colorList = []
    for name, hexVal in matplotlib.colors.cnames.items(): colorList.append(name)
    #colorList = sample(colorList,len(y_column))
    base = 15
    colorList = colorList[base:base+len(y_column)]
    plotGanttChart(p1_taskIntervals,colorList,x_row,y_column,pNo=1,max_time=hyperInterval)
    plotGanttChart(p2_taskIntervals,colorList,x_row,y_column,pNo=2,max_time=hyperInterval)
    
    #print('Task-Wise total Execution Cycle')
    totalTasksCyclesConsumed = proc1qCrit3 + proc2qCrit3
    taskCycleCounter = collections.Counter(totalTasksCyclesConsumed)
    if "Halt" in taskCycleCounter: del taskCycleCounter["Halt"]
    taskWorstDuration = {}
    for key in dataSchedule:
        for secKey in dataSchedule[key]:
            taskWorstDuration[secKey] = int(hyperInterval/dataSchedule[key][secKey]['intrvl']*dataSchedule[key][secKey]['wcet'][0])
    crit3TaskTime = {}
    ##print(fifo_tasks)
    for key in fifo_tasks:
        crit3TaskTime[key] = fifo_tasks[key]['wcet'][0]
    neededDuration = {}
    critTaskTime = {**crit1TaskTimeP1, **crit1TaskTimeP2, **crit2TaskTime, **crit3TaskTime}
    for key in dataSchedule:
        for secKey in dataSchedule[key]:
            neededDuration[secKey] = int(hyperInterval/dataSchedule[key][secKey]['intrvl']*critTaskTime[secKey])
    #compareCycles = []
    keys = []
    compareCycles = {'Task Name': [], 'WCET': [], 'ET': [], 'Allotted': []}
    for key in taskCycleCounter:
        #To removed the redundant cycles
        #if neededDuration[key] < taskCycleCounter[key]: taskCycleCounter[key] = neededDuration[key]
        compareCycles['Task Name'].append(key)
        compareCycles['WCET'].append(taskWorstDuration[key])
        compareCycles['ET'].append(neededDuration[key])
        compareCycles['Allotted'].append(taskCycleCounter[key])
    df = pd.DataFrame(compareCycles)
    df = df.sort_values(by='Task Name')
    print(df.to_string(index=False))
    