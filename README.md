# Mixed-Criticality-Scheduling
Implemened a simulated version of Mixed Criticality Real-Time Scheduling based on the paper 'Mixed-Criticality Real-Time Scheduling
for Multicore Systems' (see below).

To Run the code run the file 'highLevelScheduler.py'
The total number of processors considered for this project is two.

The file 'schedulingData.txt' contains the processes that needs to be executed.
The first column represents priority, where lower value means higher priority.
The second column represents the task name.
The third column represents the interval.
The last three columns reprsents the per criticality execution times (00 execution time is a flag representing
that the task don't consider that execution time).

The final outputs are one table and two plots.
The table represents the number of execution steps executed for a task.
The two plots represents the gantt charts of the two processors.
The plots are saved in the path as 'tsp1.png' and 'tsp2.png', and can be view from there.

    @inproceedings{mollison2010mixed,
        title={Mixed-criticality real-time scheduling for multicore systems},
        author={Mollison, Malcolm S and Erickson, Jeremy P and Anderson, James H and Baruah, Sanjoy K and Scoredos, John A},
        booktitle={2010 10th IEEE international conference on computer and information technology},
        pages={1864--1871},
        year={2010},
        organization={IEEE}
    }
