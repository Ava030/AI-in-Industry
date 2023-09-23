class Patient:
    def __init__(self, name, treatment_time, urgency):
        self.name = name
        self.treatment_time = treatment_time
        self.urgency = urgency
        self.remaining_time = treatment_time

patients = [
    Patient('A', 30, 3),
    Patient('B', 20, 5),
    Patient('C', 40, 2),
    Patient('D', 15, 4)
]

# FCFS
def fcfs(patients):
    return [patient.name for patient in patients]

# SJF
def sjf(patients):
    return [patient.name for patient in sorted(patients, key=lambda x: x.treatment_time)]

# PS
def ps(patients):
    # Sorting by urgency and then by their order of arrival for tie-breaking
    return [patient.name for patient in sorted(patients, key=lambda x: (x.urgency, -patients.index(x)), reverse=True)]

# RR
def rr(patients, quantum):
    queue = patients.copy()
    order = []
    while queue:
        patient = queue.pop(0)
        if patient.remaining_time > quantum:
            patient.remaining_time -= quantum
            queue.append(patient)
        else:
            order.append(patient.name)
    return order

print("FCFS:", fcfs(patients))
print("SJF:", sjf(patients))
print("PS:", ps(patients))
print("RR:", rr(patients, 10))
