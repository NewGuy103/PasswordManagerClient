import logging
from enum import Enum
from pathlib import Path

from platformdirs import PlatformDirs
from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict

from .version import __version__

dirs = PlatformDirs("passwordmanager-client", "newguy103", version=__version__)
logger: logging.Logger = logging.getLogger('passwordmanager-client')


class AppFilePaths(BaseModel):
    log_file: Path = Path(dirs.user_config_dir) / 'client.log'
    sqlite_file: Path = Path(dirs.user_data_dir) / 'localdb.db'
    config_file: Path = Path(dirs.user_config_dir) / 'config.json'


app_file_paths = AppFilePaths()


def setup_logger(level: int):
    global logger
    Path(dirs.user_config_dir).mkdir(exist_ok=True, parents=True)

    logger.setLevel(level)

    formatter: logging.Formatter = logging.Formatter(
        '[%(name)s]: [%(module)s | %(funcName)s] - [%(asctime)s] - [%(levelname)s] - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler: logging.FileHandler = logging.FileHandler(app_file_paths.log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


class LogLevels(int, Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL


class AvailableLogins(BaseModel):
    username: str = ''
    server_url: HttpUrl = HttpUrl(url='http://localhost:8000')
    is_default: bool = False


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(json_file=app_file_paths.config_file, validate_assignment=True)

    logins: list[AvailableLogins] = []
    log_level: LogLevels = LogLevels.debug.value

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)

    def save_settings(self):
        with open(app_file_paths.config_file, 'w') as file:
            file.write(self.model_dump_json(indent=4))
