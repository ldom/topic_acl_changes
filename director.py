import argparse
import subprocess

from cli_utils import read_json_input

commands = {
    "recreates": "recreate_topics.py"
}

def main():
    parser = argparse.ArgumentParser(description="Reads a JSON file with commands to be executed")
    parser.add_argument("json")
    parser.add_argument("cluster")

    args = parser.parse_args()
    json_commands = read_json_input(args.json)

    for command in json_commands.keys():
        if command in ['version', 'environment']:
            continue

        if command in commands:
            kafka_utility_command = ["python", commands[command], args.json, args.cluster]
            print(f'Running: {" ".join(kafka_utility_command)}')
            subprocess.run(kafka_utility_command)
        else:
            raise RuntimeError(f'Invalid Command ("{command}") Specified in "{args.json}" -- Valid Commands: {", ".join(commands.keys())}')


if __name__ == "__main__":
    main()
