from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.toml'],
)


def get_config():
    return list(settings.aspect_ratio)
