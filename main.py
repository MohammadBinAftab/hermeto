import yaml
import subprocess
from pathlib import Path
from hermeto.core.package_managers.general import async_download_files
from hermeto.core.package_managers.debian.lockfile import DebianLockfile

from hermeto.core.models.sbom import Component

def create_component(metadata):
    name = metadata.get("Package")
    version = metadata.get("Version")

    purl = f"pkg:deb/debian/{name}@{version}"

    component = Component(
        name=name,
        version=version,
        purl=purl
    )

    return component

component = create_component(metadata)
print(component)

def extract_deb_metadata(deb_path: Path):
    result = subprocess.run(
        ["dpkg-deb", "-f", str(deb_path)],
        capture_output=True,
        text=True,
        check=True,
    )

    metadata = {}

    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    return metadata


def fetch_debian_source(lockfile_path: Path, output_dir: Path):
    with open(lockfile_path) as f:
        data = yaml.safe_load(f)

    lockfile = DebianLockfile.model_validate(data)

    files = {}
    downloaded_files = []

    for arch in lockfile.arches:
        for pkg in arch.packages:
            filename = pkg.url.split("/")[-1]
            dest = output_dir / arch.arch / filename
            dest.parent.mkdir(parents=True, exist_ok=True)

            files[pkg.url] = str(dest)
            downloaded_files.append(dest)

    import asyncio
    asyncio.run(async_download_files(files, concurrency_limit=5))

    print("Download complete.")

    for deb in downloaded_files:
        metadata = extract_deb_metadata(deb)
        print(f"\nMetadata for {deb.name}:")
        print(metadata)


if __name__ == "__main__":
    fetch_debian_source(
        Path("debian.lock.yaml"),
        Path("deps/debian")
    )