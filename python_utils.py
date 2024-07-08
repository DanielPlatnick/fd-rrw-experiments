import subprocess
import json
import os


def extract_relevant_data(raw_output):
    """Extract relevant metrics from raw output."""
    lines = raw_output.split('\n')
    metrics = {
        "planner_time": None,
        "search_time": None,
        "total_time": None,
        "plan_length": None,
        "plan_cost": None,
        "expanded_states": None,
        "errors": []
    }
    for line in lines:
        if 'Planner time:' in line:
            metrics['planner_time'] = line.split()[-1]
        elif 'Search time:' in line:
            metrics['search_time'] = line.split()[-1]
        elif 'Total time:' in line:
            metrics['total_time'] = line.split()[-1]
        elif 'Plan length:' in line:
            # metrics['plan_length'] = line.split()[-1]
            parts = line.split("Plan length:")
            if len(parts) > 1:
            # Further split to get the number part before 'step(s)'
                number_part = parts[1].split("step(s)")[0].strip()    
                metrics['plan_length'] = number_part     


        elif 'Plan cost:' in line:
            metrics['plan_cost'] = line.split()[-1]
        elif 'Expanded' in line:
            metrics['expanded_states'] = line.split()[-2]
        elif 'error' in line.lower() or 'failed' in line.lower():
            metrics['errors'].append(line)
    return metrics

# Define the function to run Fast Downward and process output
def run_fast_downward(fast_downward_path, domain_file, problem_file, search_algorithm):
    command = [fast_downward_path, domain_file, problem_file, "--search", search_algorithm]
    process = subprocess.run(command, capture_output=True, text=True)
    return extract_relevant_data(process.stdout)


# # Function to perform experiments dynamically
# def perform_experiments(test_algorithm, domain_name, start_task, end_task, num_runs, fast_downward_path="./fast-downward.py", base_dir="./benchmarks"):

#     #fix indexing
#     start_task -= 1
#     end_task -= 1

#     results = {}
#     domain_path = os.path.join(base_dir, domain_name)

#     if "domain.pddl" in os.listdir(domain_path):
#         domain_file = os.path.join(domain_path, "domain.pddl")

#         if os.path.exists(domain_file):
#             results[domain_name] = {}
#             tasks = sorted([f for f in os.listdir(domain_path) if f.endswith('.pddl') and not f.startswith('domain')])
#             selected_tasks = tasks[start_task:end_task + 1]
#             for task in selected_tasks:
#                 problem_file = os.path.join(domain_path, task)
#                 problem_name = task
#                 results[domain_name][problem_name] = {}
#                 for algorithm in test_algorithm:
#                     results[domain_name][problem_name][algorithm] = []
#                     for run in range(num_runs):
#                         print(f"Running {algorithm} on {problem_name}, run {run+1}")
#                         output = run_fast_downward(fast_downward_path, domain_file, problem_file, algorithm)
#                         results[domain_name][problem_name][algorithm].append(output)
#                         print(f"Finished Run {run+1} for {problem_name} using {algorithm}.")
#         else:
#             print(f"Domain file not found: {domain_file}")
#         return results

#     else: 
#         print('not following struct')
#         pass

def perform_experiments(test_algorithm, domain_name, start_task, end_task, num_runs, fast_downward_path="./fast-downward.py", base_dir="./benchmarks"):
    # Fix indexing to match task ranges as zero-indexed
    start_task -= 1
    end_task -= 1

    results = {}
    domain_path = os.path.join(base_dir, domain_name)
    
    if not os.path.exists(domain_path):
        print(f"Domain path does not exist: {domain_path}")
        return results

    pddl_files = sorted([f for f in os.listdir(domain_path) if f.endswith('.pddl')])

    # Separate domain and task files
    domain_files = [f for f in pddl_files if 'domain' in f]
    task_files = [f for f in pddl_files if 'task' in f]
    selected_tasks = task_files[start_task:end_task + 1]

    if not selected_tasks:
        print(f"No tasks selected from {start_task+1} to {end_task+1}")
        return results

    results[domain_name] = {}
    
    if len(domain_files) == 1:  # Single domain file for all tasks
        domain_file = os.path.join(domain_path, domain_files[0])
        for task in selected_tasks:
            problem_file = os.path.join(domain_path, task)
            problem_name = task
            run_experiments(domain_file, problem_file, problem_name, test_algorithm, num_runs, fast_downward_path, results, domain_name)
    else:  # Assuming each task has a corresponding domain file
        for task in selected_tasks:
            # Assuming domain file names are like domain01.pddl for task01.pddl
            domain_index = task.split('task')[1].split('.')[0]  # This extracts the number from task filenames like task01.pddl
            domain_file = os.path.join(domain_path, f"domain{domain_index}.pddl")
            problem_file = os.path.join(domain_path, task)
            problem_name = task
            if not os.path.exists(domain_file):
                print(f"Missing domain file for {task}: {domain_file}")
                continue
            run_experiments(domain_file, problem_file, problem_name, test_algorithm, num_runs, fast_downward_path, results, domain_name)

    return results


def run_experiments(domain_file, problem_file, problem_name, test_algorithm, num_runs, fast_downward_path, results, domain_name):
    results[domain_name][problem_name] = {}
    for algorithm in test_algorithm:
        results[domain_name][problem_name][algorithm] = []
        for run in range(num_runs):
            print(f"Running {algorithm} on {problem_name}, run {run+1}")
            output = run_fast_downward(fast_downward_path, domain_file, problem_file, algorithm)
            results[domain_name][problem_name][algorithm].append(output)
            print(f"Finished Run {run+1} for {problem_name} using {algorithm}.")

        

# Function to save results to a JSON file
def save_results(results, results_path):
    with open(results_path, 'w') as file:
        json.dump(results, file, indent=4)