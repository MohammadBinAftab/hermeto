from pathlib import Path
from hermeto.core.package_managers.debian.main import fetch_debian_source

fetch_debian_source(
    Path("debian.lock.yaml"),
    Path("deps/debian")
)