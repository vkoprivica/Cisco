from ciscoparseconfig.__main__ import lowercase_transfer, parse_interfaces, create_config
from io import StringIO


def test_interfaces_input():
    assert lowercase_transfer("input_interfaces.txt") == [['lo1'], ["pony"]]


def test_parse_interfaces():
    interfaces_list = [['te2/0/1', 'up', 'up']]
    assert parse_interfaces(interfaces_list) == ["te2/0/1"]
