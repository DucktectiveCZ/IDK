from dataclasses import dataclass, asdict
import toml
import logging
from pathlib import Path
from platformdirs import user_config_dir


@dataclass
class Config:
    fps: int = 60
    win_width: int = 800
    win_height: int = 600

    def to_toml(self) -> str:
        return toml.dumps(asdict(self))

    @classmethod
    def from_toml(cls, data: str) -> "Config":
        return cls(**toml.loads(data))


def load(app_name: str) -> Config:
    config_dir = Path(user_config_dir(app_name))
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = config_dir / 'settings.toml'
    logging.debug(f"Loading settings at '{config_file}'...")
    try:
        return Config.from_toml(
            config_file.read_text(encoding='utf-8'))

    except FileNotFoundError:
        logging.warning("No config file was found; creating a default one...")

        config = Config()
        try:
            config_file.write_text(config.to_toml())
        except (PermissionError, OSError) as err:
            raise RuntimeError(f"OS Error: {err}")

        return config

    except PermissionError:
        raise RuntimeError(
            "The program doesn't have the"
            "permissions to read its settings"
        )

    except OSError as err:
        raise RuntimeError(f"OS Error: {err}")
