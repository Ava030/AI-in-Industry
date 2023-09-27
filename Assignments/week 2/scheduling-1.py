class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = 0


def compute_metrics(processes):
    waiting_times = {p.name: p.start_time - p.arrival_time for p in processes}
    turnaround_times = {p.name: p.finish_time -
                        p.arrival_time for p in processes}
    return waiting_times, turnaround_times


processes = [
    Process('P1', 0, 24, 3),
    Process('P2', 4, 3, 1),
    Process('P3', 5, 3, 4),
    Process('P4', 6, 12, 2)
]

# FCFS


def fcfs(processes):
    time = 0
    print("Starting FCFS...") # Debug statement
    for process in sorted(processes, key=lambda x: x.arrival_time):
        print(f"Processing {process.name}") # Debug statement
        if time < process.arrival_time:
            time = process.arrival_time
        process.start_time = time
        time += process.burst_time
        process.finish_time = time
    metrics = compute_metrics(processes)
    print("FCFS finished:", metrics) # Debug statement
    return metrics


# SJF


def sjf(processes):
    time = 0
    sorted_processes = sorted(
        processes, key=lambda x: (x.arrival_time, x.burst_time))
    while sorted_processes:
        # Fetch processes that have arrived by now
        available_processes = [
            p for p in sorted_processes if p.arrival_time <= time]
        if not available_processes:
            time += 1
            continue
        process = min(available_processes, key=lambda x: x.burst_time)  # Shortest job
        process.start_time = time
        time += process.burst_time
        process.finish_time = time
        sorted_processes.remove(process)
    return compute_metrics(processes)


# PS


def ps(processes):
    time = 0
    sorted_processes = sorted(
        processes, key=lambda x: (x.arrival_time, x.priority))
    while sorted_processes:
        # Fetch processes that have arrived by now
        available_processes = [
            p for p in sorted_processes if p.arrival_time <= time]
        if not available_processes:
            time += 1
            continue
        process = min(available_processes, key=lambda x: x.priority)  # Highest priority job
        process.start_time = time
        time += process.burst_time
        process.finish_time = time
        sorted_processes.remove(process)
    return compute_metrics(processes)


# RR


def rr(processes, quantum):
    time = 0
    queue = []
    
    # Initializing the processes list sorted by arrival time
    processes_by_arrival = sorted(processes, key=lambda x: x.arrival_time)
    
    while processes_by_arrival or queue:
        # Move processes from processes_by_arrival to the queue if they've arrived
        while processes_by_arrival and processes_by_arrival[0].arrival_time <= time:
            queue.append(processes_by_arrival.pop(0))
        
        # If queue is empty, then increase the time and continue
        if not queue:
            time += 1
            continue
        
        process = queue.pop(0)
        
        if process.start_time == -1:
            process.start_time = time
        
        # Execute the process
        if process.remaining_time > quantum:
            time += quantum
            process.remaining_time -= quantum
            # After the quantum, only add the process back to the end of the queue if it's not finished
            if process.remaining_time > 0:
                queue.append(process)
        else:
            time += process.remaining_time
            process.finish_time = time
            process.remaining_time = 0

    return compute_metrics(processes)




print("FCFS:", fcfs(processes))
print("SJF:", sjf(processes))
print("PS:", ps(processes))
print("RR:", rr(processes, 4))
