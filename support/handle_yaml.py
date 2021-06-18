import os
import yaml


def find_parent_dir(path, times):
    for i in range(times):
        path = os.path.dirname(path)
    return path


def load(path):
    pro_dir = find_parent_dir(__file__, 2)
    with open(os.path.join(pro_dir, path), "r") as f:
        data = yaml.safe_load(f)
    return data


if __name__ == '__main__':
    print(load("data/platform_data/company_platform_menu.yaml"))
