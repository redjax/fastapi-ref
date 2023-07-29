from __future__ import annotations

import os

from dynaconf import Dynaconf, LazySettings
from dynaconf.strategies.filtering import PrefixFilter

## Load ENV string from environment variable, or default to "prod"
ENV: str = os.environ.get("ENV", "prod")

## Define directory where Dynaconf should search for settings files
settings_root: str = "conf"

## Load default/"main" settings.toml file
settings: LazySettings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[f"{settings_root}/settings.toml", f"{settings_root}/.secrets.toml"],
)

## Load API settings from api/ dir
api_settings: LazySettings = Dynaconf(
    envvar_prefix="API",
    settings_files=[
        f"{settings_root}/api/settings.toml",
        f"{settings_root}/api/.secrets.toml",
    ],
)

db_settings: LazySettings = Dynaconf(
    envvar_prefix="DB",
    settings_files=[
        f"{settings_root}/db/settings.toml",
        f"{settings_root}/db/.secrets.toml",
    ],
)

## Append ENV to settings
settings["env"] = ENV

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
