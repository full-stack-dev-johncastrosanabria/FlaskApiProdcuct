import importlib
import sys


def load_run_module(monkeypatch, flask_env='testing', port=None):
    monkeypatch.setenv('FLASK_ENV', flask_env)

    if port is None:
        monkeypatch.delenv('PORT', raising=False)
    else:
        monkeypatch.setenv('PORT', port)

    sys.modules.pop('run', None)
    return importlib.import_module('run')


def test_get_config_name_defaults_to_development(monkeypatch):
    run = load_run_module(monkeypatch)

    monkeypatch.delenv('FLASK_ENV', raising=False)

    assert run.get_config_name() == 'development'


def test_get_port_defaults_to_5001(monkeypatch):
    run = load_run_module(monkeypatch)

    monkeypatch.delenv('PORT', raising=False)

    assert run.get_port() == 5001


def test_get_port_uses_port_environment_variable(monkeypatch):
    run = load_run_module(monkeypatch, port='7000')

    assert run.get_port() == 7000
