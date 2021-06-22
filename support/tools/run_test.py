from load_config import config
import os
import shutil
import pytest
import allure


def go_allure(is_clear=False):
    allure_path = config.get_file_path("allure")
    pro_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xml_path = pro_path + "/output/report/xml/"
    html_path = pro_path + "/output/report/html/"
    command = allure_path + "allure generate " + xml_path + " -o " + html_path + " --clean"
    os.popen(command)
    if is_clear:
        shutil.rmtree(xml_path)
        os.mkdir(xml_path)
        log_path = pro_path + "/output/log/"
        shutil.rmtree(log_path)
        os.mkdir(log_path)


def run(file_name, is_clear=False):
    if is_clear:
        go_allure(True)
    pro_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xml_path = pro_dir + "/output/report/xml/"
    pytest.main(
        ['-vs', file_name, '--alluredir', xml_path])  # 正式 "--reruns","2"
    go_allure()


def run_certain(file_name, class_name=None, function_name=None, is_clear=False):
    if class_name:
        file_name = "::".join([file_name, class_name])
    if function_name:
        file_name = "::".join([file_name, function_name])
    run(file_name, is_clear=is_clear)


def record(body, title: str = ""):
    allure.attach(str(body), str(title), allure.attachment_type.TEXT)


if __name__ == '__main__':
    go_allure()
