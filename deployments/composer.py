import os
import argparse
import subprocess
import json
from dotenv import load_dotenv

def runner(composer_config, extra_args):
    arg_stack = ['docker', 'compose', composer_config, *extra_args]
    print(arg_stack)
    subprocess.run(
        arg_stack,
        env=os.environ
    )


def parse_config():
    config = load_config()
    docker_configs = {}
    for key, value in config.items():
        tmp_config_str = ""

        if "env-file" in value:
            load_dotenv(dotenv_path=value["env-file"])
            
        for compose_file in value["file"]:
            tmp_config_str += f" -f {compose_file}"
    
        docker_configs[key] = tmp_config_str
    
    return docker_configs


def load_config(file_name="setup.json"):
    with open(file_name, "r") as f:
        config = json.load(f)
        return config


def cli_parser():
    parser = argparse.ArgumentParser(    
        description='Welcome to parser! A wrapper to run docker compose environments easier.',
        epilog='Contribute here:')

    parser.add_argument("environment", type=str, help="The name of the environment you want to run")
    parser.add_argument("docker_args", nargs=argparse.REMAINDER)

    args = parser.parse_args()
    docker_configs = parse_config()
    runner(docker_configs[args.environment], args.docker_args)

if __name__=="__main__":
    cli_parser()