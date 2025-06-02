import os
from dotenv import load_dotenv
from pathlib import Path
import yaml

# 1. 加载 .env 文件
load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)


# 2. 加载 config.yml
def load_yaml_config(path: Path = Path.cwd() / "config.yml") -> dict[str, str]:
    if os.path.exists(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)
    return {}


yaml_config = load_yaml_config()


# 3. 获取配置，优先用环境变量
def get_config(key: str, default: str = "") -> str:
    return os.getenv(key.upper()) or yaml_config.get(key.upper(), default)


# 4. 导出常用配置
LONGPORT_APP_KEY: str = get_config("LONGPORT_APP_KEY", "")
LONGPORT_APP_SECRET: str = get_config("LONGPORT_APP_SECRET", "")
LONGPORT_ACCESS_TOKEN: str = get_config("LONGPORT_ACCESS_TOKEN", "")
