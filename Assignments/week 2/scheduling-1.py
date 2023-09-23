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
    for process in sorted(processes, key=lambda x: x.arrival_time):
        if time < process.arrival_time:
            time = process.arrival_time
        process.start_time = time
        time += process.burst_time
        process.finish_time = time
    return compute_metrics(processes)

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
        process = available_processes[0]  # Shortest job
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
        process = available_processes[0]  # Highest priority job
        process.start_time = time
        time += process.burst_time
        process.finish_time = time
        sorted_processes.remove(process)
    return compute_metrics(processes)

# RR


def rr(processes, quantum):
    time = 0
    queue = processes.copy()
    while queue:
        process = queue.pop(0)
        if process.start_time == -1:
            process.start_time = time
        if process.remaining_time > quantum:
            time += quantum
            process.remaining_time -= quantum
            # Re-check the queue and append process back if it's not finished
            for p in processes:
                if p not in queue and p != process and p.arrival_time <= time:
                    queue.append(p)
            queue.append(process)
        else:
            time += process.remaining_time
            process.finish_time = time
            process.remaining_time = 0
            # Add processes that arrived while the current one was executing
            for p in processes:
                if p not in queue and p.arrival_time <= time:
                    queue.append(p)
    return compute_metrics(processes)


print("FCFS:", fcfs(processes))
print("SJF:", sjf(processes))
print("PS:", ps(processes))
print("RR:", rr(processes, 4))
