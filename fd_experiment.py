from python_utils import *
        

def main():

    """
    Note: 
    -need to modify run_fast_downward() to parse command line arguements better
    -need to verify there's no issue with parsing output by implementing a stochastic algorithm    
    """

    # Define the base directory where the domains and their tasks are stored
    # base_dir = "./benchmarks"
    # Define the path to the Fast Downward executable
    # fast_downward_path = "./fast-downward.py"

    # Define the search algorithms to use
    ALGORITHMS = [
        ["ehc(ff())"], 
        ['astar(ff())'], 
        ["eager_greedy([ff()], boost=100)"], 
        ["ehcrw(ff())"]
    ]


    ehc = ALGORITHMS[0]
    gbfs = ALGORITHMS[2]
    ehcrw = ALGORITHMS[3]

    # need to fix parsing arguments
    custom_random_gbfs = [
    "--evaluator", "h=ff()",
    "--search", "lazy_greedy([h], randomize_successors=true, random_seed=5)"
]

    # domain_list = [domain for domain in os.listdir('benchmarks') if domain != 'README.md' and domain != 'experiment_output']
    domain_list = ['blocks', 'movie', 'depot', 'freecell', 'transport', 'parcprinter', 'tpp', 'woodworking', 'pegsol', 
                   'gripper', 'elevators', 'psr-small', 'zenotravel', 'scanalyzer', 'airport', 'satellite', 'rovers', 
                   'openstacks', 'logistics', 'sokoban', 'miconic']
    
    # ehc is bad at depot
    domain_list.remove('depot')

    print(domain_list)


    run_experiments_across_domains(algorithm=ehc, domains=domain_list, start_task=1, stop_task=3, num_runs=1)
    # run_experiments_across_domains(algorithm=ehcrw, domains=domain_list, start_task=1, stop_task=3, num_runs=1)
    # run_experiments_across_domains(algorithm=gbfs, domains=domain_list, start_task=1, stop_task=10, num_runs=2)
    # run_experiments_across_domains(algorithm=custom_random_gbfs, domains=domain_list[:3], start_task=1, stop_task=4, num_runs=3)




if __name__ == "__main__":
    main()