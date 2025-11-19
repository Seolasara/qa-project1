import configparser
import os

def read_config(section="helpychat"):

    config = configparser.ConfigParser()

    # 현재 파일 기준으로 project_root/src/config/config.ini 경로 지정
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_path, "config", "config.ini")

    # 파일을 직접 열어서 BOM 제거 후 파싱
    with open(config_path, "r", encoding="utf-8-sig") as f:
        config.read_file(f)

    if not config.has_section(section):
        available = config.sections()
        raise KeyError(
            f"❌ Section '{section}' not found in {config_path}\n"
        )
    return dict(config[section])