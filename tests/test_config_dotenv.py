import os
import sys
import tempfile
from pathlib import Path
import pytest


@pytest.fixture
def temp_project_env(monkeypatch: pytest.MonkeyPatch):
    orig_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        # 切换目录
        monkeypatch.chdir(tmpdir)
        # 清理环境变量
        monkeypatch.delenv("LONGPORT_APP_KEY", raising=False)
        monkeypatch.delenv("LONGPORT_APP_SECRET", raising=False)
        monkeypatch.delenv("LONGPORT_ACCESS_TOKEN", raising=False)
        yield tmpdir
        os.chdir(orig_cwd)


def reload_config():
    sys.modules.pop("config", None)
    from config import (
        LONGPORT_APP_KEY,
        LONGPORT_APP_SECRET,
        LONGPORT_ACCESS_TOKEN,
    )

    return LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN


def test_dotenv_loading(temp_project_env: str):
    tmpdir = temp_project_env
    env_path = Path(tmpdir) / ".env"
    env_content = (
        "LONGPORT_APP_KEY=test_key\n"
        "LONGPORT_APP_SECRET=test_secret\n"
        "LONGPORT_ACCESS_TOKEN=test_token\n"
    )
    env_path.write_text(env_content)
    key, secret, token = reload_config()
    assert key == "test_key"
    assert secret == "test_secret"
    assert token == "test_token"


def test_yaml_loading(temp_project_env: str):
    tmpdir = temp_project_env
    yaml_path = Path(tmpdir) / "config.yml"
    yaml_content = """
LONGPORT_APP_KEY: yaml_key
LONGPORT_APP_SECRET: yaml_secret
LONGPORT_ACCESS_TOKEN: yaml_token
"""
    yaml_path.write_text(yaml_content)
    key, secret, token = reload_config()
    assert key == "yaml_key"
    assert secret == "yaml_secret"
    assert token == "yaml_token"


def test_env_overrides_yaml(temp_project_env: str, monkeypatch: pytest.MonkeyPatch):
    tmpdir = temp_project_env
    yaml_path = Path(tmpdir) / "config.yml"
    yaml_content = """
LONGPORT_APP_KEY: yaml_key
LONGPORT_APP_SECRET: yaml_secret
LONGPORT_ACCESS_TOKEN: yaml_token
"""
    yaml_path.write_text(yaml_content)
    monkeypatch.setenv("LONGPORT_APP_KEY", "env_key")
    monkeypatch.setenv("LONGPORT_APP_SECRET", "env_secret")
    monkeypatch.setenv("LONGPORT_ACCESS_TOKEN", "env_token")
    key, secret, token = reload_config()
    assert key == "env_key"
    assert secret == "env_secret"
    assert token == "env_token"


def test_default_values(temp_project_env: str):
    key, secret, token = reload_config()
    assert key == ""
    assert secret == ""
    assert token == ""
