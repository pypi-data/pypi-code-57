import subprocess
import os
import yaml
import argparse
import math

def run(command, input_data=""):
    process = subprocess.run(command, input=input_data, text=True, capture_output=True)
    return process.stdout

def generate_testcase(inputter_command, outputter_command):
    input_data = run(inputter_command)
    output_data = run(outputter_command, input_data)
    return input_data, output_data

def generate_batch(config, inputter_command, outputter_command):
    name = config['name']
    testcases_name = config['testcase']['name']
    num_testcases = config['testcase']['num']
    points = config['points']
    testcase_num_digits = int(math.log10(num_testcases))+1

    batch_dir = os.path.join("testcases", name)
    os.mkdir(batch_dir)
    manifest = {'type': 'batch', 'name': name, 'metadata': {'points': points}}
    with open(os.path.join(batch_dir, "manifest.yaml"), "w") as manifest_file:
        yaml.dump(manifest, manifest_file)
    for testcase_num in range(num_testcases):
        input_data, output_data = generate_testcase(inputter_command, outputter_command)
        testcase_name = testcases_name.format(str(testcase_num+1).zfill(testcase_num_digits))
        os.mkdir(os.path.join(batch_dir, testcase_name))
        with open(os.path.join(batch_dir, testcase_name, testcase_name + ".in"), "w") as testcase_input_file:
            testcase_input_file.write(input_data)
        with open(os.path.join(batch_dir, testcase_name, testcase_name + ".out"), "w") as testcase_output_file:
            testcase_output_file.write(output_data)

def main(config):
    inputter_command = config['generator']['input']
    outputter_command = config['generator']['output']
    batches = config['testcase']['batch']
    os.mkdir("testcases")
    for batch in batches:
        generate_batch(batch, inputter_command, outputter_command)

def cli():
    parser = argparse.ArgumentParser(description='Generate testdata in PNOJ format.')
    parser.add_argument('configuration', help='File name of the configuration YAML.')
    args = parser.parse_args()
    with open(args.configuration, "r") as config_file:
        config = yaml.safe_load(config_file)
    main(config)

if __name__ == "__main__":
    cli()
