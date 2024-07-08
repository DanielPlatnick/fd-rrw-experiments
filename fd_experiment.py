from python_utils import *


def main():


    # Define the base directory where the domains and their tasks are stored
    # base_dir = "./benchmarks"
    # Define the path to the Fast Downward executable
    # fast_downward_path = "./fast-downward.py"

    # Define the search algorithms to use
    ALGORITHMS = [["ehc(ff())"], ['astar(ff())']]

    ehc = ALGORITHMS[0]
    a_star = ALGORITHMS[1]
    domain = 'blocks'

    ehc_results_path = 'experiment_output/results_ehc.json'
    a_star_results_path = 'experiment_output/results_astar.json'


    results = perform_experiments(ehc, domain, start_task=1, end_task=7, num_runs=3)  # Example: Run tasks 1 to 3 in the 'blocks' domain
    save_results(results, ehc_results_path)

    results_2 = perform_experiments(a_star, domain, start_task=1, end_task=7, num_runs=3)
    save_results(results_2, a_star_results_path)

if __name__ == "__main__":
    main()