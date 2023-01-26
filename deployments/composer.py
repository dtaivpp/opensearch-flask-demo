import argparse

def runner():
    pass


def cli_parser():
    parser = argparse.ArgumentParser(    
        description='Welcome to parser! A wrapper to run docker compose environments easier.',
        epilog='Contribute here:')

    parser.add_argument("environment", type=str, help="The name of the environment you want to run")
    parser.add_argument("vars", nargs='+')

    runner()

if __name__=="__main__":
    cli_parser()