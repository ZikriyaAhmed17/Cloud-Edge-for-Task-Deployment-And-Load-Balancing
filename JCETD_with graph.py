import heapq
import random
import matplotlib.pyplot as plt

class Task:
    def __init__(self, id, arrival_time, service_time, location, latency_requirement):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.location = location  
        self.latency_requirement = latency_requirement

    def __lt__(self, other):
        return (self.latency_requirement, self.service_time) < (other.latency_requirement, other.service_time)

class VirtualMachine:
    def __init__(self, id):
        self.id = id
        self.current_time = 0

    def execute_task(self, task):
        self.current_time += task.service_time

class Datacenter:
    def __init__(self, id, num_vms):
        self.id = id
        self.virtual_machines = [VirtualMachine(i) for i in range(num_vms)]
        self.task_queue = []

    def schedule_task(self, task):
        vm = min(self.virtual_machines, key=lambda x: x.current_time)
        start_time = max(vm.current_time, task.arrival_time)
        end_time = start_time + task.service_time
        vm.execute_task(task)
        return (task.id, vm.id, task.location, start_time, end_time, end_time - task.arrival_time)

    def calculate_load_balance_degree(self):
        utilizations = [vm.current_time for vm in self.virtual_machines]
        return max(utilizations) - min(utilizations)

def generate_tasks(num_tasks):
    tasks = []
    for i in range(num_tasks):
        arrival_time = int(input(f"Enter the arrival time for Task-{i}: "))
        service_time = int(input(f"Enter the service time for Task-{i}: "))
        latency_requirement = int(input(f"Enter the latency requirement for Task-{i} (1-5): "))  
        location = 'edge' if latency_requirement <= 3 else 'cloud'
        task = Task(f"Task-{i}", arrival_time, service_time, location, latency_requirement)
        tasks.append(task)
    return tasks

def simulate(datacenters, tasks):
    load_balance_degrees = []
    for task in tasks:
        if task.location == 'cloud':
            heapq.heappush(datacenters[0].task_queue, task)
        else:
            least_loaded_datacenter = min(datacenters[1:], key=lambda d: d.calculate_load_balance_degree())
            heapq.heappush(least_loaded_datacenter.task_queue, task)

        load_balance_degrees.append([datacenter.calculate_load_balance_degree() for datacenter in datacenters])

    schedule = []
    for datacenter in datacenters:
        while datacenter.task_queue:
            task = heapq.heappop(datacenter.task_queue)
            schedule.append(datacenter.schedule_task(task))
            load_balance_degrees.append([datacenter.calculate_load_balance_degree() for datacenter in datacenters])

    return schedule, load_balance_degrees

def main():
    num_datacenters = 6
    datacenters = [Datacenter(f"Datacenter-{i}", 6) for i in range(num_datacenters)]

    num_tasks = int(input("Enter the number of tasks: "))
    tasks = generate_tasks(num_tasks)

    schedule, load_balance_degrees = simulate(datacenters, tasks)

    print("Task ID\tVM ID\tLocation\tStart Time\tEnd Time\tTurnaround Time")
    for task in schedule:
        print(f"{task[0]}\t{task[1]}\t\t{task[2]}\t{task[3]}\t\t{task[4]}\t\t{task[5]}")

    time_steps = list(range(len(load_balance_degrees)))
    for i, datacenter in enumerate(datacenters):
        plt.plot(time_steps, [degree[i] for degree in load_balance_degrees], label=f"Datacenter-{i}")

    plt.xlabel('Time Step')
    plt.ylabel('Load Balance Degree')
    plt.title('Load Balance Degree over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
