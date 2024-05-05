from urllib.error import HTTPError

from bs4 import BeautifulSoup
from packaging.requirements import Requirement
from packaging.version import Version
import pandas as pd
import pytest
import requests

from pycm import pycm


def test_invalid_package():
    with pytest.raises(HTTPError):
        pycm('never', [])

def test_empty_python_versions():
    assert len(pycm('requests', []).index) == 0

def test_single_python_versions():
    assert len(pycm('requests', ['3.8']).index) == 1

def test_multi_python_versions():
    assert len(pycm('requests', ['3.8', '3.9']).index) == 2

def test_tensorflow():
    res = requests.get('https://www.tensorflow.org/install/source#tested_build_configurations')
    soup = BeautifulSoup(res.text, features='lxml')

    cpu_table, = soup.select('#cpu + table')
    expected_df, = pd.read_html(str(cpu_table))

    actual_df = pycm('tensorflow', ['3.7', '3.8', '3.9', '3.10', '3.11', '3.12', '3.13'], groupby_patch=False)

    for _, expected_row in expected_df.iterrows():
        tf_version_str = expected_row['Version'].replace('tensorflow-', '')
        if Version(tf_version_str) >= Version('2.2.0'):
            min_py, max_py = expected_row['Python version'].split('-')
            py_spec = Requirement(f'python>={min_py},<={max_py}').specifier

            actual_spec = actual_df[tf_version_str].to_dict()
            for actual_py_version, is_supported_str in actual_spec.items():
                expected_is_supported = str(actual_py_version) in py_spec
                actual_is_supported = (is_supported_str == 'Y')
                assert expected_is_supported == actual_is_supported, f'Incorrect result for TF version {tf_version_str} and Python version {actual_py_version}. Found: {actual_spec}'
