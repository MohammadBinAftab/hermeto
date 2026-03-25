from pydantic import BaseModel, PositiveInt

class DebianPackage(BaseModel):
    url: str
    checksum: str | None = None
    size: int | None = None


class DebianArch(BaseModel):
    arch: str
    packages: list[DebianPackage]


class DebianLockfile(BaseModel):
    lockfileVersion: PositiveInt
    lockfileVendor: str
    arches: list[DebianArch]