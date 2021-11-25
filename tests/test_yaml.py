import hiyapyco
import pytest
import yaml
from yaml.scanner import ScannerError


def test_simple_safe_load():
    yml = 'key: 5'

    expected = {'key': 5}

    assert yaml.safe_load(yml) == expected


def test_safe_load_with_nested_mappings():
    yml = ('some_key:\n'
           '  another_key: 2\n'
           '  key_with_list:\n'
           '  - 5\n'
           '  - 6')

    expected = {'some_key': {'another_key': 2, 'key_with_list': [5, 6]}}

    assert yaml.safe_load(yml) == expected


def test_given_config_example_with_safe_load():
    yml_config = ('- image: tfidf_vectorizer:0.1\n'
                  '  imagePullPolicy: IfNotPresent\n'
                  '  name: tfidfvectorizer')

    expected = [{'image': 'tfidf_vectorizer:0.1', 'imagePullPolicy': 'IfNotPresent', 'name': 'tfidfvectorizer'}]

    assert yaml.safe_load(yml_config) == expected


def test_safe_dump():
    d = {
        'some_key': {'some_other_key': [4, 5], 'some_other_key2': True}
    }

    expected = ('some_key:\n'
                '  some_other_key:\n'
                '  - 4\n'
                '  - 5\n'
                '  some_other_key2: true\n')

    assert yaml.safe_dump(d) == expected
