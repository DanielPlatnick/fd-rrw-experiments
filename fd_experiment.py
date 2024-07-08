from python_utils import *


def main():


    # Define the base directory where the domains and their tasks are stored
    # base_dir = "./benchmarks"
    # Define the path to the Fast Downward executable
    # fast_downward_path = "./fast-downward.py"

    # Define the search algorithms to use
    ALGORITHMS = [["ehc(ff())"], ['astar(ff())']]

    ehc = ALGORITHMS[0]
    # a_star = ALGORITHMS[1]

    domain_list = [domain for domain in os.listdir('benchmarks') if domain != 'README.md' and domain != 'experiment_output']

    print(domain_list)


    domain = 'scanalyzer'


    ehc_results_path = 'benchmarks/experiment_output/results_ehc.json'

    results = perform_experiments(ehc, domain, start_task=1, end_task=15, num_runs=3)  # Example: Run tasks 1 to 3 in the 'blocks' domain
    save_results(results, ehc_results_path)


if __name__ == "__main__":
    main()