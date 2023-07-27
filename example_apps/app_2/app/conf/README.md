# Dynaconf configuration

Define settings files here to be loaded by `Dynaconf`. The `app/config.py` file reaches into this `conf/` directory to find settings files, defined as `.toml`, `.json`, `.yaml`, etc files that `Dynaconf` can read.

The file at `conf/settings.toml` is the "main" settings file. It contains limited app settings.

Settings for `FastAPI` exist in `conf/api`. Things like the app's title, the port it runs on, etc, are divided into 2 environments sections, `[prod]` and `[dev]`. The environment loaded by the app is determined by a `$ENV` variable.

Declare `$ENV` by setting it as an environment variable (`docker run -e ENV=(prod/dev)`, `export ENV=(prod/dev)`, etc). Defaults to `prod`, where `debug` is disabled and the `Uvicorn` server does not auto-reload on file changes.

## Override settings files with .local.toml versions

Create a `settings.local.toml` and `.secrets.local.toml` by making a copy of the original (`settings.toml/.secrets.toml`). Files with `.local.toml` will be ignored by the `.gitignore`, and are safe to use for local development purposes (i.e. if running outside of Docker).
