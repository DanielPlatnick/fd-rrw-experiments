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

# Function to perform experiments dynamically
def perform_experiments(test_algorithm, domain_name, start_task, end_task, num_runs, fast_downward_path="./fast-downward.py", base_dir="./benchmarks"):

    #fix indexing
    start_task -= 1
    end_task -= 1

    results = {}
    domain_path = os.path.join(base_dir, domain_name)
    domain_file = os.path.join(domain_path, "domain.pddl")
    if os.path.exists(domain_file):
        results[domain_name] = {}
        tasks = sorted([f for f in os.listdir(domain_path) if f.endswith('.pddl') and not f.startswith('domain')])
        selected_tasks = tasks[start_task:end_task + 1]
        for task in selected_tasks:
            problem_file = os.path.join(domain_path, task)
            problem_name = task
            results[domain_name][problem_name] = {}
            for algorithm in test_algorithm:
                results[domain_name][problem_name][algorithm] = []
                for run in range(num_runs):
                    print(f"Running {algorithm} on {problem_name}, run {run+1}")
                    output = run_fast_downward(fast_downward_path, domain_file, problem_file, algorithm)
                    results[domain_name][problem_name][algorithm].append(output)
                    print(f"Finished Run {run+1} for {problem_name} using {algorithm}.")
    else:
        print(f"Domain file not found: {domain_file}")
    return results

# Function to save results to a JSON file
def save_results(results, results_path):
    with open(results_path, 'w') as file:
        json.dump(results, file, indent=4)