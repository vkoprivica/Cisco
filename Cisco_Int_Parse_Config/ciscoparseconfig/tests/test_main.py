from ciscoparseconfig.__main__ import interfaces_input, parse_interfaces, create_config
from io import StringIO


def test_interfaces_input(monkeypatch):
    user_input = StringIO("eth1/1\n\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert interfaces_input() == [['eth1/1']]

    user_input = StringIO("lo0\n\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert interfaces_input() == [['lo0']]

    user_input = StringIO("Fdksdfkfds\n\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert interfaces_input() == [['fdksdfkfds']]

    user_input = StringIO("Port-channel10\n\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert interfaces_input() == [['port-channel10']]


def test_parse_interfaces():
    interfaces_list = [["eth1/1"], ["eth1/2"],
                       ["lo0"], ["gi0/0"], ['fdksdfkfds'], ['port-channel10']]
    assert parse_interfaces(interfaces_list) == [
        "eth1/1", "eth1/2", "lo0", "gi0/0", "po10"]
