import socket

from pymongo_inmemory import _utils


def test_find_open_port(monkeypatch):
    open_ports = (123, 125)

    class mock_socket():
        AF_INET = None
        SOCK_STREAM = None

        def __init__(self, *args, **kwargs):
            pass

        def connect_ex(self, obj):
            if obj[1] in open_ports:
                return 0
            return 42

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(socket, "socket", mock_socket)
    assert _utils.find_open_port([123, 124]) == 124
    assert _utils.find_open_port([122, 123]) == 122
    assert _utils.find_open_port([123, 125, 122]) == 122
