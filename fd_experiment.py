import subprocess

# Define the path to the Fast Downward executable
FAST_DOWNWARD_PATH = "./fast-downward.py"

# Define the path to the domain and problem files
DOMAIN_FILE = "./benchmarks/blocks/domain.pddl"
PROBLEM_FILE = "./benchmarks/blocks/task01.pddl"

# Define the search algorithm
ALGORITHM = "ehc(ff())"

# Function to run Fast Downward
def run_fast_downward(domain_file, problem_file, search_algorithm):
    command = [
        FAST_DOWNWARD_PATH, domain_file, problem_file, "--search", search_algorithm
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    return process.stdout

# Running the planner
output = run_fast_downward(DOMAIN_FILE, PROBLEM_FILE, ALGORITHM)
print("Output from Fast Downward:")
print(output)