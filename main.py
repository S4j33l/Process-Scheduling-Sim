import tkinter as tk
from tkinter import *
import tkinter.messagebox
import matplotlib.pyplot as plt
import identity_savior
GREY = "#606060"
LIME_PUNCH = "#D6ED17"
PC_FONT = "RecMonoCasual Nerd Font Propo"


def fcfs(processes):
    processes.sort(key=lambda x: x[0])
    waiting_time = [0] * len(processes)
    turnaround_time = [0] * len(processes)
    completion_time = [0] * len(processes)
    start_time = [0] * len(processes)

    start_time[0] = processes[0][0]
    completion_time[0] = processes[0][0] + processes[0][1]
    turnaround_time[0] = completion_time[0] - processes[0][0]
    waiting_time[0] = turnaround_time[0] - processes[0][1]

    for i in range(1, len(processes)):
        start_time[i] = max(completion_time[i - 1], processes[i][0])
        waiting_time[i] = start_time[i] - processes[i][0]
        completion_time[i] = start_time[i] + processes[i][1]
        turnaround_time[i] = completion_time[i] - processes[i][0]

    avg_waiting_time = sum(waiting_time) / len(processes)
    avg_turnaround_time = sum(turnaround_time) / len(processes)
    print(f"{'=' * 70}\nFirst Come First Serve (FCFS) Scheduling Algorithm\n{'=' * 70}")
    print('Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time')
    for i in range(len(processes)):
        print(f'{i + 1}\t\t{processes[i][0]}\t\t{processes[i]
              [1]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}')
    print(f'Average Waiting Time: {avg_waiting_time.__round__(2)}')
    print(f'Average Turnaround Time: {avg_turnaround_time.__round__(2)}')
    with open(identity_savior.fcfs_result_file, 'w') as file:
        for i in range(len(processes)):
            file.write(f'{i + 1}\t{processes[i][0]}\t{processes[i][1]}\t{
                       waiting_time[i]}\t{turnaround_time[i]}\n')
        file.write(f'Average Waiting Time: {avg_waiting_time.__round__(2)}\n')
        file.write(f'Average Turnaround Time: {
                   avg_turnaround_time.__round__(2)}\n')


def generate_gantt_chart_for_fcfs(processes):

    fig, ax = plt.subplots()
    ytick_labels = []
    ytick_positions = []

    start_time = [0] * len(processes)
    completion_time = [0] * len(processes)

    start_time[0] = processes[0][0]
    completion_time[0] = processes[0][0] + processes[0][1]

    for i in range(1, len(processes)):
        start_time[i] = max(completion_time[i - 1], processes[i][0])
        completion_time[i] = start_time[i] + processes[i][1]

    for idx, (arrival, burst) in enumerate(processes):
        bar_height = 0.8
        y_position = 10 * (idx + 1)
        ax.broken_barh([(start_time[idx], completion_time[idx] - start_time[idx])],
                       (y_position, bar_height), facecolors=('tab:blue'))

        ax.text(start_time[idx] - 0.5, y_position + bar_height / 2,
                f'P{idx + 1}', va='center', ha='right', color='red', fontsize=8)

        ytick_labels.append(f'P{idx + 1}')
        ytick_positions.append(y_position + bar_height / 2)

    ax.set_ylim(5, 10 * (len(processes) + 1))
    ax.set_xlim(0, max(completion_time) + 1)
    ax.set_xlabel('Time')
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(ytick_labels)
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.show()


def read_fcfs_data_from_file():
    with open(identity_savior.fcfs_process_file, 'r') as file:
        data = file.readlines()
        processes = []
        for line in data:
            arrival_time, burst_time = map(int, line.split())
            processes.append((arrival_time, burst_time))
        return processes


def sjf(processes):
    processes.sort(key=lambda x: x[0])
    n = len(processes)
    schedule = []
    turnaround_time = [0] * n
    waiting_time = [0] * n

    current_time = 0
    completed = [False] * n
    completed_processes = 0

    while completed_processes < n:
        idx = -1
        shortest_burst_time = float('inf')
        for i in range(n):
            if processes[i][0] <= current_time and not completed[i] and processes[i][1] < shortest_burst_time:
                idx = i
                shortest_burst_time = processes[i][1]

        if idx != -1:
            start_time = current_time
            current_time += processes[idx][1]
            end_time = current_time
            schedule.append((idx, start_time, end_time))
            completed[idx] = True
            completed_processes += 1

            turnaround_time[idx] = end_time - processes[idx][0]
            waiting_time[idx] = turnaround_time[idx] - processes[idx][1]
        else:
            current_time += 1
    avg_turnaround_time = sum(turnaround_time) / n
    avg_waiting_time = sum(waiting_time) / n
    print(f"{'=' * 70}\nShortest Job First (SJF) Scheduling Algorithm\n{'=' * 70}")
    print('Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time')
    for i in range(len(processes)):
        print(f'{i + 1}\t\t{processes[i][0]}\t\t{processes[i]
              [1]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}')
    print(f'Average Waiting Time: {avg_waiting_time.__round__(2)}')
    print(f'Average Turnaround Time: {avg_turnaround_time.__round__(2)}')
    with open(identity_savior.sjf_result_file, 'w') as file:
        for i in range(len(processes)):
            file.write(f'{i + 1}\t{processes[i][0]}\t{processes[i][1]}\t{
                       waiting_time[i]}\t{turnaround_time[i]}\n')
        file.write(f'Average Waiting Time: {avg_waiting_time.__round__(2)}\n')
        file.write(f'Average Turnaround Time: {
                   avg_turnaround_time.__round__(2)}\n')

    return schedule


def generate_gantt_chart_for_sjf(schedule):
    fig, ax = plt.subplots()
    ytick_labels = []
    ytick_positions = []

    for idx, (process_id, start, end) in enumerate(schedule):
        bar_height = 0.8
        y_position = 10 * (idx + 1)
        ax.broken_barh([(start, end - start)], (y_position,
                       bar_height), facecolors=('tab:blue'))

        ax.text(start - 0.5, y_position + bar_height / 2,
                f'P{process_id + 1}', va='center', ha='right', color='red', fontsize=8)

        ytick_labels.append(f'P{process_id + 1}')
        ytick_positions.append(y_position + bar_height / 2)

    ax.set_ylim(5, 10 * (len(schedule) + 1))
    ax.set_xlim(0, max(end for _, _, end in schedule) + 1)
    ax.set_xlabel('Time')
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(ytick_labels)
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.show()


def read_sjf_data_from_file():
    with open(identity_savior.sjf_process_file, 'r') as file:
        data = file.readlines()
        processes = []
        for line in data:
            arrival_time, burst_time = map(int, line.split())
            processes.append((arrival_time, burst_time))
        return processes


def srtf(processes):
    processes.sort(key=lambda x: x[0])
    n = len(processes)
    schedule = []
    waiting_time = [0] * n
    turnaround_time = [0] * n
    remaining_time = [process[1] for process in processes]

    time = 0
    completed_processes = 0
    last_start_time = [-1] * n
    current_process = -1

    while completed_processes < n:
        idx = -1
        shortest_remaining_time = float('inf')
        for i in range(n):
            if processes[i][0] <= time and remaining_time[i] > 0 and remaining_time[i] < shortest_remaining_time:
                idx = i
                shortest_remaining_time = remaining_time[i]

        if idx != -1:
            if current_process != idx:
                if current_process != -1:
                    schedule.append(
                        (current_process, last_start_time[current_process], time))
                last_start_time[idx] = time
                current_process = idx

            remaining_time[idx] -= 1
            time += 1
            if remaining_time[idx] == 0:
                schedule.append((idx, last_start_time[idx], time))
                completed_processes += 1
                turnaround_time[idx] = time - processes[idx][0]
                waiting_time[idx] = turnaround_time[idx] - processes[idx][1]
                current_process = -1
        else:
            time += 1
    avg_turnaround_time = sum(turnaround_time) / n
    avg_waiting_time = sum(waiting_time) / n
    print(
        f"{'=' * 70}\nShortest Remaining Time First (SRTF) Scheduling Algorithm\n{'=' * 70}")
    print('Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time')
    for i in range(len(processes)):
        print(f'{i + 1}\t\t{processes[i][0]}\t\t{processes[i][1]}\t\t{
            waiting_time[i]}\t\t{turnaround_time[i]}')

    print(f'Average Waiting Time: {avg_waiting_time.__round__(2)}')
    print(f'Average Turnaround Time: {avg_turnaround_time.__round__(2)}')
    with open(identity_savior.srtf_result_file, 'w') as file:
        for i in range(n):
            file.write(f'{i + 1}\t{processes[i][0]}\t{processes[i][1]}\t{
                waiting_time[i]}\t{turnaround_time[i]}\n')
        file.write(f'Average Waiting Time: {
            avg_waiting_time.__round__(2)}\n')
        file.write(f'Average Turnaround Time: {
            avg_turnaround_time.__round__(2)}\n')
    return schedule


def generate_gantt_chart_for_srtf(schedule):
    fig, ax = plt.subplots()
    ytick_labels = []
    ytick_positions = []

    for idx, (process_id, start, end) in enumerate(schedule):
        bar_height = 0.8
        y_position = 10 * (idx + 1)
        ax.broken_barh([(start, end - start)], (y_position,
                       bar_height), facecolors=('tab:blue'))

        ax.text(start - 0.5, y_position + bar_height / 2,
                f'P{process_id}', va='center', ha='right', color='red', fontsize=8)

        if f'P{process_id}' not in ytick_labels:
            ytick_labels.append(f'P{process_id}')
            ytick_positions.append(y_position + bar_height / 2)

    ax.set_ylim(5, 10 * (len(schedule) + 1))
    ax.set_xlim(0, max(end for _, _, end in schedule) + 1)
    ax.set_xlabel('Time')
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(ytick_labels)
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.show()


def read_srtf_data_from_file():
    with open(identity_savior.srtf_process_file, 'r') as file:
        data = file.readlines()
        processes = []
        for line in data:
            arrival_time, burst_time = map(int, line.split())
            processes.append((arrival_time, burst_time))
        return processes


def round_robin(processes, quantum):
    processes.sort(key=lambda x: x[0])
    n = len(processes)
    schedule = []
    turnaround_time = [0] * n
    waiting_time = [0] * n

    current_time = 0
    completed = [False] * n
    completed_processes = 0
    remaining_burst_time = [process[1] for process in processes]

    while completed_processes < n:
        done = True
        for i in range(n):
            if not completed[i] and processes[i][0] <= current_time:
                done = False
                start_time = current_time
                if remaining_burst_time[i] > quantum:
                    current_time += quantum
                    remaining_burst_time[i] -= quantum
                else:
                    current_time += remaining_burst_time[i]
                    remaining_burst_time[i] = 0
                    completed[i] = True
                    completed_processes += 1
                    turnaround_time[i] = current_time - processes[i][0]
                    waiting_time[i] = turnaround_time[i] - processes[i][1]
                schedule.append((i, start_time, current_time))
        if done:
            current_time += 1
    print(f"{'=' * 70}\nRound Robin (RR) Scheduling Algorithm\n{'=' * 70}")
    print('Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time')
    for i in range(len(processes)):
        print(f'{i + 1}\t\t{processes[i][0]}\t\t{processes[i]
              [1]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}')

    avg_turnaround_time = sum(turnaround_time) / n
    avg_waiting_time = sum(waiting_time) / n
    print(f'Time Quantum: {quantum}')
    print(f'Average Waiting Time: {avg_waiting_time.__round__(2)}')
    print(f'Average Turnaround Time: {avg_turnaround_time.__round__(2)}')
    with open(identity_savior.rr_result_file, "w") as file:
        for i in range(len(processes)):
            file.write(f"{i + 1}\t{processes[i][0]}\t{processes[i][1]}\t{
                       waiting_time[i]}\t{turnaround_time[i]}\n")
        file.write(f"Time Quantum: {quantum}\n")
        file.write(f"Average Waiting Time: {avg_waiting_time.__round__(2)}\n")
        file.write(f"Average Turnaround Time: {
                   avg_turnaround_time.__round__(2)}\n")
    return schedule


def generate_gantt_chart_for_rr(schedule):
    fig, ax = plt.subplots()
    ytick_labels = []
    ytick_positions = []

    for idx, (process_id, start, end) in enumerate(schedule):
        bar_height = 0.8
        y_position = 10 * (idx + 1)
        ax.broken_barh([(start, end - start)], (y_position,
                       bar_height), facecolors=('tab:blue'))
        ax.text(start - 0.5, y_position + bar_height / 2,
                f'P{process_id + 1}', va='center', ha='right', color='red', fontsize=8)

        if f'P{process_id + 1}' not in ytick_labels:
            ytick_labels.append(f'P{process_id + 1}')
            ytick_positions.append(y_position + bar_height / 2)

    ax.set_ylim(5, 10 * (len(schedule) + 1))
    ax.set_xlim(0, max(end for _, _, end in schedule) + 1)
    ax.set_xlabel('Time')
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(ytick_labels)
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.show()


def read_rr_data_from_file():
    with open(identity_savior.rr_process_file, 'r') as file:
        data = file.readlines()
        processes = []
        time_quantum = int(data[0].split()[2])
        print(f'Time Quantum: {time_quantum}')
        for i in range(1, len(data)):
            arrival_time, burst_time = map(int, data[i].split())
            processes.append((arrival_time, burst_time))
        return (processes, time_quantum)


def priority_scheduling(processes):
    n = len(processes)
    schedule = [[] for _ in range(n)]
    turnaround_time = [0] * n
    waiting_time = [0] * n
    remaining_burst_times = [p[1] for p in processes]

    current_time = 0
    completed_processes = 0
    running_process = None

    while completed_processes < n:
        idx = -1
        highest_priority = float('inf')
        earliest_arrival = float('inf')
        for i in range(n):
            if processes[i][0] <= current_time and remaining_burst_times[i] > 0:
                if processes[i][2] < highest_priority or (processes[i][2] == highest_priority and processes[i][0] < earliest_arrival):
                    idx = i
                    highest_priority = processes[i][2]
                    earliest_arrival = processes[i][0]

        if idx != -1:
            if running_process is not None and running_process != idx:
                schedule[running_process][-1] = (
                    schedule[running_process][-1][0], current_time)
            if idx != running_process or not schedule[idx]:
                schedule[idx].append((current_time, None))
            remaining_burst_times[idx] -= 1
            if remaining_burst_times[idx] == 0:
                completed_processes += 1
                end_time = current_time + 1
                schedule[idx][-1] = (schedule[idx][-1][0], end_time)
                turnaround_time[idx] = end_time - processes[idx][0]
                waiting_time[idx] = turnaround_time[idx] - processes[idx][1]
            running_process = idx
        current_time += 1
    print(f"{'=' * 70}\nPriority Scheduling Algorithm\n{'=' * 70}")
    print('Process ID\tArrival Time\tBurst Time\tPriority\tWaiting Time\tTurnaround Time')
    for i, process in enumerate(processes):
        print(f'{i + 1}\t\t{process[0]}\t\t{process[1]}\t\t{process[2]
                                                            }\t\t{waiting_time[i]}\t\t{turnaround_time[i]}')

    avg_turnaround_time = sum(turnaround_time) / n
    avg_waiting_time = sum(waiting_time) / n
    print(f'Average Waiting Time: {avg_waiting_time.__round__(2)}')
    print(f'Average Turnaround Time: {avg_turnaround_time.__round__(2)}')
    with open(identity_savior.ps_result_file, "w") as file:
        for i, process in enumerate(processes):
            file.write(f"{i + 1}\t{process[0]}\t{process[1]}\t{process[2]}\t{
                       waiting_time[i]}\t{turnaround_time[i]}\n")
        file.write(f"Average Waiting Time: {avg_waiting_time.__round__(2)}\n")
        file.write(f"Average Turnaround Time: {
                   avg_turnaround_time.__round__(2)}\n")
    return schedule


def generate_gantt_chart_for_ps(schedule):
    fig, ax = plt.subplots()
    process_positions = {}
    next_y_position = 10

    for process_id, slices in enumerate(schedule):
        if process_id not in process_positions:
            process_positions[process_id] = next_y_position
            next_y_position += 10

        bar_height = 0.8
        y_position = process_positions[process_id]
        for start, end in slices:
            ax.broken_barh([(start, end - start)], (y_position,
                           bar_height), facecolors=('tab:blue'))

    ytick_labels = [f'P{pid + 1}' for pid in sorted(process_positions)]
    ytick_positions = [process_positions[pid]
                       for pid in sorted(process_positions)]

    ax.set_ylim(5, next_y_position)
    ax.set_xlim(0, max(max(end for _, end in slices)
                for slices in schedule if slices) + 1)
    ax.set_xlabel('Time')
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(ytick_labels)
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.show()


def read_ps_data_from_file():
    with open(identity_savior.ps_process_file, 'r') as file:
        data = file.readlines()
        processes = []
        for line in data:
            arrival_time, burst_time, priority = map(
                int, line.split())
            processes.append((arrival_time, burst_time, priority))
        return processes


root = tk.Tk()
root.title("Process Scheduling Simulator")
width = 600
height = 500
width_of_screen = root.winfo_screenwidth()
height_of_screen = root.winfo_screenheight()
x = (width_of_screen/2) - (width/2)
y = (height_of_screen/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(False, False)
base_frame = tk.Frame(root, bg=GREY)
base_frame.pack(fill="both", expand=True)
base_frame.grid_rowconfigure(0, weight=1)
base_frame.grid_columnconfigure(0, weight=1)


def show_frame(frame):
    frame.tkraise()


start_page_frame = tk.Frame(base_frame, bg=GREY)
fcfs_page_frame = tk.Frame(base_frame, bg=GREY)
sjf_page_frame = tk.Frame(base_frame, bg=GREY)
srtf_page_frame = tk.Frame(base_frame, bg=GREY)
rr_page_frame = tk.Frame(base_frame, bg=GREY)
ps_page_frame = tk.Frame(base_frame, bg=GREY)
examples_page_frame = tk.Frame(base_frame, bg=GREY)
fcfs_example_page_frame = tk.Frame(base_frame, bg=GREY)
sjf_example_page_frame = tk.Frame(base_frame, bg=GREY)
srtf_example_page_frame = tk.Frame(base_frame, bg=GREY)
rr_example_page_frame = tk.Frame(base_frame, bg=GREY)
ps_example_page_frame = tk.Frame(base_frame, bg=GREY)
fcfs_results_frame = tk.Frame(base_frame, bg=GREY)
sjf_results_frame = tk.Frame(base_frame, bg=GREY)
rr_results_frame = tk.Frame(base_frame, bg=GREY)
ps_results_frame = tk.Frame(base_frame, bg=GREY)
srtf_results_frame = tk.Frame(base_frame, bg=GREY)


for frame in (start_page_frame, fcfs_page_frame, sjf_page_frame, srtf_page_frame, rr_page_frame, ps_page_frame, examples_page_frame, fcfs_example_page_frame, sjf_example_page_frame, srtf_example_page_frame, rr_example_page_frame, ps_example_page_frame, fcfs_results_frame, sjf_results_frame, srtf_results_frame, rr_results_frame, ps_results_frame, srtf_results_frame):
    frame.grid(row=0, column=0, sticky="nsew")


def show_start_page():
    show_frame(start_page_frame)


def show_fcfs_page():
    show_frame(fcfs_page_frame)


def show_sjf_page():
    show_frame(sjf_page_frame)


def show_srtf_page():
    show_frame(srtf_page_frame)


def show_srtf_results_page():
    show_frame(srtf_results_frame)


def show_rr_page():
    show_frame(rr_page_frame)


def show_ps_page():
    show_frame(ps_page_frame)


def show_examples_page():
    show_frame(examples_page_frame)


def show_fcfs_example_page(frame_to_destroy):
    frame_to_destroy.destroy()
    show_frame(fcfs_example_page_frame)


def show_sjf_example_page():
    show_frame(sjf_example_page_frame)


def show_srtf_example_page():
    show_frame(srtf_example_page_frame)


def show_rr_example_page():
    show_frame(rr_example_page_frame)


def show_ps_example_page():
    show_frame(ps_example_page_frame)


def show_fcfs_results_page():
    show_frame(fcfs_results_frame)


def show_sjf_results_page():
    show_frame(sjf_results_frame)


def show_rr_results_page():
    show_frame(rr_results_frame)


def show_ps_results_page():
    show_frame(ps_results_frame)


def show_example_for_fcfs():
    fcfs_example_frame_main_label = tk.Label(fcfs_example_page_frame, text="First Come First Serve (FCFS) Scheduling Algorithm", font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    fcfs_example_frame_description = tk.Label(fcfs_example_page_frame, text="In this algorithm, the process that arrives first is executed first. The process that arrives first is the first to get executed. This is a non-preemptive algorithm.", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
    fcfs_example_frame_example_label = tk.Label(fcfs_example_page_frame, text="Example", font=(
        PC_FONT, 15), bg=GREY, fg=LIME_PUNCH).place(x=300, y=200, anchor="center")
    fcfs_example_frame_example_text = tk.Text(fcfs_example_page_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=10, width=60)
    with open(identity_savior.fcfs_process_file, 'r') as file:
        fcfs_example_frame_example_text.insert(tk.END, file.read())
    fcfs_example_frame_example_text.config(state="disabled")
    fcfs_example_frame_example_text.place(x=50, y=250)
    fcfs_example_frame_back_button = tk.Button(fcfs_example_page_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_examples_page(fcfs_page_frame)).place(x=275, y=425)
    show_fcfs_example_page()


def show_example_for_sjf():
    sjf_example_frame_main_label = tk.Label(sjf_example_page_frame, text="Shortest Job First (SJF) Scheduling Algorithm", font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    sjf_example_frame_description = tk.Label(sjf_example_page_frame, text="In this algorithm, the process with the smallest burst time is executed first. This is a non-preemptive algorithm.", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
    sjf_example_frame_example_label = tk.Label(sjf_example_page_frame, text="Example", font=(
        PC_FONT, 15), bg=GREY, fg=LIME_PUNCH).place(x=300, y=200, anchor="center")
    sjf_example_frame_example_text = tk.Text(sjf_example_page_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=10, width=60)
    with open(identity_savior.sjf_process_file, 'r') as file:
        sjf_example_frame_example_text.insert(tk.END, file.read())
    sjf_example_frame_example_text.config(state="disabled")
    sjf_example_frame_example_text.place(x=50, y=250)
    sjf_example_frame_back_button = tk.Button(sjf_example_page_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_examples_page(sjf_page_frame)).place(x=275, y=425)
    show_sjf_example_page()


def show_example_for_srtf():
    srtf_example_frame_main_label = tk.Label(srtf_example_page_frame, text="Shortest Remaining Time First (SRTF) Scheduling Algorithm", font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    srtf_example_frame_description = tk.Label(srtf_example_page_frame, text="In this algorithm, the process with the smallest remaining burst time is executed first. This is a preemptive algorithm.", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
    srtf_example_frame_example_label = tk.Label(srtf_example_page_frame, text="Example", font=(
        PC_FONT, 15), bg=GREY, fg=LIME_PUNCH).place(x=300, y=200, anchor="center")
    srtf_example_frame_example_text = tk.Text(srtf_example_page_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=10, width=60)
    with open(identity_savior.srtf_process_file, 'r') as file:
        srtf_example_frame_example_text.insert(tk.END, file.read())
    srtf_example_frame_example_text.config(state="disabled")
    srtf_example_frame_example_text.place(x=50, y=250)
    srtf_example_frame_back_button = tk.Button(srtf_example_page_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_examples_page(srtf_page_frame)).place(x=275, y=425)
    show_srtf_example_page()


def show_example_for_rr():
    rr_example_frame_main_label = tk.Label(rr_example_page_frame, text="Round Robin (RR) Scheduling Algorithm", font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    rr_example_frame_description = tk.Label(rr_example_page_frame, text="In this algorithm, each process is assigned a fixed time slice in cyclic order. The time slice is called a quantum. If a process completes its execution within the time slice, it gets terminated. If it does not complete within the time slice, it is moved to the end of the queue.", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
    rr_example_frame_example_label = tk.Label(rr_example_page_frame, text="Example", font=(
        PC_FONT, 15), bg=GREY, fg=LIME_PUNCH).place(x=300, y=200, anchor="center")
    rr_example_frame_example_text = tk.Text(rr_example_page_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=10, width=60)
    with open(identity_savior.rr_process_file, 'r') as file:
        rr_example_frame_example_text.insert(tk.END, file.read())
    rr_example_frame_example_text.config(state="disabled")
    rr_example_frame_example_text.place(x=50, y=250)
    rr_example_frame_back_button = tk.Button(rr_example_page_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_examples_page(rr_page_frame)).place(x=275, y=425)
    show_rr_example_page()


def show_example_for_ps():
    ps_example_frame_main_label = tk.Label(ps_example_page_frame, text="Priority Scheduling Algorithm", font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    ps_example_frame_description = tk.Label(ps_example_page_frame, text="In this algorithm, the process with the highest priority is executed first. This is a non-preemptive algorithm.", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
    ps_example_frame_example_label = tk.Label(ps_example_page_frame, text="Example", font=(
        PC_FONT, 15), bg=GREY, fg=LIME_PUNCH).place(x=300, y=200, anchor="center")
    ps_example_frame_example_text = tk.Text(ps_example_page_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=10, width=60)
    with open(identity_savior.ps_process_file, 'r') as file:
        ps_example_frame_example_text.insert(tk.END, file.read())
    ps_example_frame_example_text.config(state="disabled")
    ps_example_frame_example_text.place(x=50, y=250)
    ps_example_frame_back_button = tk.Button(ps_example_page_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_examples_page(ps_page_frame)).place(x=275, y=425)
    show_ps_example_page()


def show_results_page_and_display_results_for_fcfs():
    results = read_fcfs_data_from_file()
    fcfs(results)
    generate_gantt_chart_for_fcfs(results)
    fcfs_results_frame_main_label = tk.Label(fcfs_results_frame, text="Results",  font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    fcfs_results_frame_process_id_label = tk.Label(
        fcfs_results_frame, text="PID", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=50, y=130)
    fcfs_results_frame_arrival_time_label = tk.Label(
        fcfs_results_frame, text="AT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=110, y=130)
    fcfs_results_frame_burst_time_label = tk.Label(
        fcfs_results_frame, text="BT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=170, y=130)
    fcfs_results_frame_waiting_time_label = tk.Label(
        fcfs_results_frame, text="WT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=240, y=130)
    fcfs_results_frame_turnaround_time_label = tk.Label(
        fcfs_results_frame, text="TAT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=130)
    fcfs_results_frame_results_text = tk.Text(fcfs_results_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=15, width=60)
    with open(identity_savior.fcfs_result_file, 'r') as file:
        fcfs_results_frame_results_text.insert(tk.END, file.read())
    fcfs_results_frame_results_text.config(state="disabled")
    fcfs_results_frame_results_text.place(x=50, y=150)
    fcfs_results_frame_back_button = tk.Button(fcfs_results_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_fcfs_page).place(x=275, y=425)
    show_fcfs_results_page()


def show_results_page_and_display_results_for_sjf():
    results = read_sjf_data_from_file()
    schedule_for_sjf = sjf(results)
    generate_gantt_chart_for_sjf(schedule_for_sjf)
    sjf_results_frame_main_label = tk.Label(sjf_results_frame, text="Results",  font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    sjf_results_frame_process_id_label = tk.Label(
        sjf_results_frame, text="PID", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=50, y=130)
    sjf_results_frame_arrival_time_label = tk.Label(
        sjf_results_frame, text="AT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=110, y=130)
    sjf_results_frame_burst_time_label = tk.Label(
        sjf_results_frame, text="BT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=170, y=130)
    sjf_results_frame_waiting_time_label = tk.Label(
        sjf_results_frame, text="WT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=240, y=130)
    sjf_results_frame_turnaround_time_label = tk.Label(
        sjf_results_frame, text="TAT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=130)
    sjf_results_frame_results_text = tk.Text(sjf_results_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=15, width=60)
    with open(identity_savior.sjf_result_file, 'r') as file:
        sjf_results_frame_results_text.insert(tk.END, file.read())
    sjf_results_frame_results_text.config(state="disabled")
    sjf_results_frame_results_text.place(x=50, y=150)
    sjf_results_frame_back_button = tk.Button(sjf_results_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_sjf_page).place(x=275, y=425)
    show_sjf_results_page()


def show_results_page_and_display_results_for_srtf():
    processes = read_srtf_data_from_file()
    schedule = srtf(processes)
    generate_gantt_chart_for_srtf(schedule)
    srtf_results_frame_main_label = tk.Label(srtf_results_frame, text="Results",  font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    srtf_results_frame_process_id_label = tk.Label(
        srtf_results_frame, text="PID", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=50, y=130)
    srtf_results_frame_arrival_time_label = tk.Label(
        srtf_results_frame, text="AT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=110, y=130)
    srtf_results_frame_burst_time_label = tk.Label(
        srtf_results_frame, text="BT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=170, y=130)
    srtf_results_frame_waiting_time_label = tk.Label(
        srtf_results_frame, text="WT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=240, y=130)
    srtf_results_frame_turnaround_time_label = tk.Label(
        srtf_results_frame, text="TAT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=130)
    srtf_results_frame_results_text = tk.Text(srtf_results_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=15, width=60)
    with open(identity_savior.srtf_result_file, 'r') as file:
        srtf_results_frame_results_text.insert(tk.END, file.read())
    srtf_results_frame_results_text.config(state="disabled")
    srtf_results_frame_results_text.place(x=50, y=150)
    srtf_results_frame_back_button = tk.Button(srtf_results_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_srtf_page).place(x=275, y=425)
    show_srtf_results_page()


def show_results_page_and_display_results_for_rr():
    results = read_rr_data_from_file()
    schedule_for_rr = round_robin(results[0], results[1])
    generate_gantt_chart_for_rr(schedule_for_rr)
    rr_results_frame_main_label = tk.Label(rr_results_frame, text="Results",  font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    rr_results_frame_process_id_label = tk.Label(
        rr_results_frame, text="PID", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=50, y=130)
    rr_results_frame_arrival_time_label = tk.Label(
        rr_results_frame, text="AT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=110, y=130)
    rr_results_frame_burst_time_label = tk.Label(
        rr_results_frame, text="BT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=170, y=130)
    rr_results_frame_waiting_time_label = tk.Label(
        rr_results_frame, text="WT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=240, y=130)
    rr_results_frame_turnaround_time_label = tk.Label(
        rr_results_frame, text="TAT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=130)
    rr_results_frame_results_text = tk.Text(rr_results_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=15, width=60)
    with open(identity_savior.rr_result_file, 'r') as file:
        rr_results_frame_results_text.insert(tk.END, file.read())
    rr_results_frame_results_text.config(state="disabled")
    rr_results_frame_results_text.place(x=50, y=150)
    rr_results_frame_back_button = tk.Button(rr_results_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_rr_page).place(x=275, y=425)
    show_rr_results_page()


def show_results_page_and_display_results_for_ps():
    results = read_ps_data_from_file()
    schedule_for_ps = priority_scheduling(results)
    generate_gantt_chart_for_ps(schedule_for_ps)
    ps_results_frame_main_label = tk.Label(ps_results_frame, text="Results",  font=(
        PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
    ps_results_frame_process_id_label = tk.Label(
        ps_results_frame, text="PID", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=50, y=130)
    ps_results_frame_arrival_time_label = tk.Label(
        ps_results_frame, text="AT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=110, y=130)
    ps_results_frame_burst_time_label = tk.Label(
        ps_results_frame, text="BT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=175, y=130)
    ps_results_frame_priority_label = tk.Label(
        ps_results_frame, text="Priority", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=210, y=130)
    ps_results_frame_waiting_time_label = tk.Label(
        ps_results_frame, text="WT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=300, y=130)
    ps_results_frame_turnaround_time_label = tk.Label(
        ps_results_frame, text="TAT", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=360, y=130)
    ps_results_frame_results_text = tk.Text(ps_results_frame, font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, height=15, width=60)
    with open(identity_savior.ps_result_file, 'r') as file:
        ps_results_frame_results_text.insert(tk.END, file.read())
    ps_results_frame_results_text.config(state="disabled")
    ps_results_frame_results_text.place(x=50, y=150)
    ps_results_frame_back_button = tk.Button(ps_results_frame, text="Back", font=(
        PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_ps_page).place(x=275, y=425)
    show_ps_results_page()


start_page_main_label = tk.Label(
    start_page_frame, text="Process Scheduling", font=(PC_FONT, 24), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
start_page_choice_label = tk.Label(
    start_page_frame, text="Please choose from any of the available options", font=(PC_FONT, 12), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
start_page_fcfs_button = tk.Button(start_page_frame, text="First Come First Serve", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_fcfs_page).place(x=50, y=150)
start_page_sjf_button = tk.Button(start_page_frame, text="Shortest Job First", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_sjf_page).place(x=350, y=150)
start_page_rr_button = tk.Button(start_page_frame, text="Round Robin", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_rr_page).place(x=50, y=250)
start_page_ps_button = tk.Button(start_page_frame, text="Priority Scheduling", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_ps_page).place(x=350, y=250)
start_page_srtf_button = tk.Button(start_page_frame, text="Shortest Time Remaining First", font=(
    PC_FONT, 10), width=30, height=2, bg=GREY, fg=LIME_PUNCH, command=show_srtf_page).place(x=50, y=350)
examples_page_button = tk.Button(start_page_frame, text="Examples", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_examples_page).place(x=350, y=350)
start_page_creators_label = tk.Label(
    start_page_frame, text=f"Created by --------, ------- --- & ----- -------", font=(PC_FONT, 8), bg=GREY, fg=LIME_PUNCH).place(x=250, y=475)

examples_page_main_label = tk.Label(
    examples_page_frame, text="Examples", font=(PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
examples_page_fcfs_button = tk.Button(examples_page_frame, text="First Come First Serve", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_fcfs).place(x=50, y=150)
examples_page_sjf_button = tk.Button(examples_page_frame, text="Shortest Job First", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_sjf).place(x=350, y=150)
examples_page_rr_button = tk.Button(examples_page_frame, text="Round Robin", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_rr).place(x=50, y=250)
examples_page_ps_button = tk.Button(examples_page_frame, text="Priority Scheduling", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_ps).place(x=350, y=250)
examples_page_srtf_button = tk.Button(examples_page_frame, text="Shortest Time Remaining First", font=(
    PC_FONT, 10), width=30, height=2, bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_srtf).place(x=50, y=350)
examples_page_back_button = tk.Button(examples_page_frame, text="Back", font=(
    PC_FONT, 10), width=25, height=2, bg=GREY, fg=LIME_PUNCH, command=show_start_page).place(x=350, y=350)


def write_data_to_file_fcfs(arrival_time, burst_time):
    with open(identity_savior.fcfs_process_file, 'a') as file:
        file.write(f"{arrival_time}")
        file.write(f"\t{burst_time}\n")


def submit_data_for_fcfs():
    a_time = fcfs_page_arrival_time.get()
    b_time = fcfs_page_burst_time.get()
    write_data_to_file_fcfs(arrival_time=a_time, burst_time=b_time)
    fcfs_page_arrival_time_entry.delete(0, 'end')
    fcfs_page_burst_time_entry.delete(0, 'end')
    tkinter.messagebox.showinfo(
        "Success", "Data has been submitted successfully")
    fcfs_page_arrival_time_entry.focus()


fcfs_page_arrival_time = tk.StringVar(fcfs_page_frame)
fcfs_page_burst_time = tk.StringVar(fcfs_page_frame)
fcfs_page_main_label = tk.Label(
    fcfs_page_frame, text="FCFS", font=(PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
fcfs_page_secondary_label = tk.Label(fcfs_page_frame, text="Please enter the required details", font=(
    PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
fcfs_page_arrival_time_label = tk.Label(
    fcfs_page_frame, text="Arrival Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=180)
fcfs_page_burst_time_label = tk.Label(
    fcfs_page_frame, text="Burst Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=230)
fcfs_page_arrival_time_entry = tk.Entry(
    fcfs_page_frame, textvariable=fcfs_page_arrival_time)
fcfs_page_arrival_time_entry.place(x=225, y=200)
fcfs_page_burst_time_entry = tk.Entry(
    fcfs_page_frame, textvariable=fcfs_page_burst_time)
fcfs_page_burst_time_entry.place(x=225, y=250)
fcfs_page_back_button = tk.Button(fcfs_page_frame, text="Back", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_start_page).place(x=150, y=350)
fcfs_page_submit_button = tk.Button(fcfs_page_frame, text="Submit", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=submit_data_for_fcfs).place(x=250, y=350)
fcfs_page_show_results_button = tk.Button(fcfs_page_frame, text="Show Results", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_fcfs).place(x=350, y=350)


def write_data_to_file_sjf(arrival_time, burst_time):
    with open(identity_savior.sjf_process_file, 'a') as file:
        file.write(f"{arrival_time}")
        file.write(f"\t{burst_time}\n")


def submit_data_for_sjf():
    a_time = sjf_page_arrival_time.get()
    b_time = sjf_page_burst_time.get()
    write_data_to_file_sjf(arrival_time=a_time, burst_time=b_time)
    sjf_page_arrival_time_entry.delete(0, "end")
    sjf_page_burst_time_entry.delete(0, "end")
    tkinter.messagebox.showinfo(
        "Success", "Data has been submitted successfully")
    sjf_page_arrival_time_entry.focus()


sjf_page_arrival_time = tk.StringVar(sjf_page_frame)
sjf_page_burst_time = tk.StringVar(sjf_page_frame)
sjf_page_main_label = tk.Label(
    sjf_page_frame, text="SJF", font=(PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
sjf_page_secondary_label = tk.Label(sjf_page_frame, text="Please enter the required details", font=(
    PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
sjf_page_arrival_time_label = tk.Label(
    sjf_page_frame, text="Arrival Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=180)
sjf_page_burst_time_label = tk.Label(
    sjf_page_frame, text="Burst Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=230)
sjf_page_arrival_time_entry = tk.Entry(
    sjf_page_frame, textvariable=sjf_page_arrival_time)
sjf_page_arrival_time_entry.place(x=225, y=200)
sjf_page_burst_time_entry = tk.Entry(
    sjf_page_frame, textvariable=sjf_page_burst_time)
sjf_page_burst_time_entry.place(x=225, y=250)
sjf_page_back_button = tk.Button(sjf_page_frame, text="Back", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_start_page).place(x=150, y=350)
sjf_page_submit_button = tk.Button(sjf_page_frame, text="Submit", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=submit_data_for_sjf).place(x=250, y=350)
sjf_page_show_results_button = tk.Button(sjf_page_frame, text="Show Results", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_sjf).place(x=350, y=350)


def write_data_to_file_srtf(arrival_time, burst_time):
    with open(identity_savior.srtf_process_file, 'a') as file:
        file.write(f"{arrival_time}")
        file.write(f"\t{burst_time}\n")


def submit_data_for_srtf():
    a_time = srtf_page_arrival_time.get()
    b_time = srtf_page_burst_time.get()
    write_data_to_file_srtf(arrival_time=a_time, burst_time=b_time)
    srtf_page_arrival_time_entry.delete(0, "end")
    srtf_page_burst_time_entry.delete(0, "end")
    tkinter.messagebox.showinfo(
        "Success", "Data has been submitted successfully")
    srtf_page_arrival_time_entry.focus()


srtf_page_arrival_time = tk.StringVar(srtf_page_frame)
srtf_page_burst_time = tk.StringVar(srtf_page_frame)
srtf_page_main_label = tk.Label(
    srtf_page_frame, text="SRTF", font=(PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
srtf_page_secondary_label = tk.Label(srtf_page_frame, text="Please enter the required details", font=(
    PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
srtf_page_arrival_time_label = tk.Label(
    srtf_page_frame, text="Arrival Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=180)
srtf_page_burst_time_label = tk.Label(
    srtf_page_frame, text="Burst Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=230)
srtf_page_arrival_time_entry = tk.Entry(
    srtf_page_frame, textvariable=srtf_page_arrival_time)
srtf_page_arrival_time_entry.place(x=225, y=200)
srtf_page_burst_time_entry = tk.Entry(
    srtf_page_frame, textvariable=srtf_page_burst_time)
srtf_page_burst_time_entry.place(x=225, y=250)
srtf_page_back_button = tk.Button(srtf_page_frame, text="Back", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_start_page).place(x=150, y=350)
srtf_page_submit_button = tk.Button(srtf_page_frame, text="Submit", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=submit_data_for_srtf).place(x=250, y=350)
srtf_page_show_results_button = tk.Button(srtf_page_frame, text="Show Results", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_srtf).place(x=350, y=350)


def write_data_to_file_rr(arrival_time, burst_time, time_quantum):
    with open(identity_savior.rr_process_file, 'a') as file:
        file.write(f"{arrival_time}")
        file.write(f"\t{burst_time}")
        if time_quantum is None:
            file.write(f"\t")
        else:
            file.write(f"\t{time_quantum}\n")


def submit_data_for_rr():
    a_time = rr_page_arrival_time.get()
    b_time = rr_page_burst_time.get()
    tq = rr_page_time_quantum.get()
    write_data_to_file_rr(arrival_time=a_time,
                          burst_time=b_time, time_quantum=tq)
    rr_page_arrival_time_entry.delete(0, "end")
    rr_page_burst_time_entry.delete(0, "end")
    rr_page_time_quantum_entry.delete(0, "end")
    rr_page_time_quantum_entry.config(state="disabled")
    tkinter.messagebox.showinfo(
        "Success", "Data has been submitted successfully")
    rr_page_arrival_time_entry.focus()


rr_page_arrival_time = tk.StringVar(rr_page_frame)
rr_page_burst_time = tk.StringVar(rr_page_frame)
rr_page_time_quantum = tk.StringVar(rr_page_frame)
rr_page_main_label = tk.Label(
    rr_page_frame, text="Round Robin", font=((PC_FONT, 20)), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
rr_page_secondary_label = tk.Label(rr_page_frame, text="Please enter the required details", font=(
    PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
rr_page_arrival_time_label = tk.Label(
    rr_page_frame, text="Arrival Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=160)
rr_page_burst_time_label = tk.Label(
    rr_page_frame, text="Burst Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=210)
rr_page_time_quantum_label = tk.Label(
    rr_page_frame, text="Time Quantum", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=260)
rr_page_arrival_time_entry = tk.Entry(
    rr_page_frame, textvariable=rr_page_arrival_time)
rr_page_arrival_time_entry.place(x=225, y=180)
rr_page_burst_time_entry = tk.Entry(
    rr_page_frame, textvariable=rr_page_burst_time)
rr_page_burst_time_entry.place(x=225, y=230)
rr_page_time_quantum_entry = tk.Entry(
    rr_page_frame, textvariable=rr_page_time_quantum)
rr_page_time_quantum_entry.place(x=225, y=280)
rr_page_back_button = tk.Button(rr_page_frame, text="Back", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_start_page).place(x=150, y=350)
rr_page_submit_button = tk.Button(rr_page_frame, text="Submit", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=submit_data_for_rr).place(x=250, y=350)
rr_page_show_results_button = tk.Button(rr_page_frame, text="Show Results", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_rr).place(x=375, y=350)


def write_data_to_file_ps(arrival_time, burst_time, priority):
    with open(identity_savior.ps_process_file, 'a') as file:
        file.write(f"{arrival_time}")
        file.write(f"\t{burst_time}")
        file.write(f"\t{priority}\n")


def submit_data_for_ps():
    a_time = ps_page_arrival_time.get()
    b_time = ps_page_burst_time.get()
    p = ps_page_priority.get()
    write_data_to_file_ps(arrival_time=a_time,
                          burst_time=b_time, priority=p)
    ps_page_arrival_time_entry.delete(0, "end")
    ps_page_burst_time_entry.delete(0, "end")
    ps_page_priority_entry.delete(0, "end")
    tkinter.messagebox.showinfo(
        "Success", "Data has been submitted successfully")
    ps_page_arrival_time_entry.focus()


ps_page_arrival_time = tk.StringVar(ps_page_frame)
ps_page_burst_time = tk.StringVar(ps_page_frame)
ps_page_priority = tk.StringVar(ps_page_frame)
ps_page_main_label = tk.Label(
    ps_page_frame, text="Priority Scheduling", font=(PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=50, anchor="center")
ps_page_secondary_label = tk.Label(ps_page_frame, text="Please enter the required details", font=(
    PC_FONT, 20), bg=GREY, fg=LIME_PUNCH).place(x=300, y=100, anchor="center")
ps_page_arrival_time_label = tk.Label(
    ps_page_frame, text="Arrival Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=160)
ps_page_burst_time_label = tk.Label(
    ps_page_frame, text="Burst Time", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=210)
ps_page_time_quantum_label = tk.Label(
    ps_page_frame, text="Priority", font=(PC_FONT, 10), bg=GREY, fg=LIME_PUNCH).place(x=225, y=260)
ps_page_arrival_time_entry = tk.Entry(
    ps_page_frame, textvariable=ps_page_arrival_time)
ps_page_arrival_time_entry.place(x=225, y=180)
ps_page_burst_time_entry = tk.Entry(
    ps_page_frame, textvariable=ps_page_burst_time)
ps_page_burst_time_entry.place(x=225, y=230)
ps_page_priority_entry = tk.Entry(
    ps_page_frame, textvariable=ps_page_priority)
ps_page_priority_entry.place(x=225, y=280)
ps_page_back_button = tk.Button(ps_page_frame, text="Back", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_start_page).place(x=150, y=350)
ps_page_submit_button = tk.Button(ps_page_frame, text="Submit", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=submit_data_for_ps).place(x=250, y=350)
ps_page_show_results_button = tk.Button(ps_page_frame, text="Show Results", font=(
    PC_FONT, 10), bg=GREY, fg=LIME_PUNCH, command=show_results_page_and_display_results_for_ps).place(x=375, y=350)


show_frame(start_page_frame)
root.mainloop()
