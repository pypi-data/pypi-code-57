"""
FIXME: insert program metadata
"""


"""
This method uses the 'type of dependencies' statistics pulled by the server tool
to calculate the total number of dependencies a package has.
"""
def find_total_dependencies_of_package(input_data, package=None):
    if package is not None:
        return input_data[package]['transitive_dependencies'] + \
            input_data[package]['explicit_dependencies']
    
    package_dependencies = {}
    for package in input_data:
        package_dependencies[package] = \
            input_data[package]['transitive_dependencies'] + \
            input_data[package]['explicit_dependencies']
    return package_dependencies


def find_transitive_to_explicit_ratio(input_data, package):
    return input_data[package]['transitive_dependencies'] / \
        input_data[package]['explicit_dependencies']


def calculate_average_transitive_to_explicit_ratio(input_data):
    total_ratio = 0
    count_with_no_explicit = 0

    for package in input_data:
        if data[package]['explicit_dependencies'] == 0:
            count_with_no_explicit += 1
            continue
        total_ratio += (input_data[package]['transitive_dependencies'] / \
            input_data[package]['explicit_dependencies'])

    return ((total_ratio / (len(input_data) - count_with_no_explicit)),
        count_with_no_explicit)


"""
This method is used to find the average number of consumers a package has.
A consumer is any other package that uses this package as part of its supply
chain.
"""
def calculate_average_consumers(input_data):
    all_packages = set()
    total_consumption = 0

    for package in input_data:
        all_packages.add(package)
        total_consumption += len(input_data.get(package))
        for consumer in input_data.get(package):
            all_packages.add(consumer)
    
    total_packages = len(all_packages)

    return total_consumption / total_packages
