import shutil


def tool_exists(name: str) -> bool:
    return shutil.which(name) is not None