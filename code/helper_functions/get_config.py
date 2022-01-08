from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.toml'],
)


def get_config():
    aspect_ratio = tuple(settings.aspect_ratio)
    return aspect_ratio[0], aspect_ratio[1], bool(settings.fullscreen)
