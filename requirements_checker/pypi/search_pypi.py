from httpx import AsyncClient
from requirements_checker.logger import LOGGER
from requirements_checker.pypi.version_pypi import PyPiVersion


async def search_pypi(async_client: AsyncClient, packaget_name: str) -> PyPiVersion:
    """Function to search the package into pypi and return the latest version

    Args:
        async_client (AsyncClient): httpx asyncio client to connect to the api
        packaget_name (str): The name of the package

    Returns:
        PyPiVersion: A Wrapper to make it possible to compare pypi versions number and suffixes
    """
    latest_version = PyPiVersion("0.0.0")
    try:
        r = await async_client.get(f"https://pypi.org/pypi/{packaget_name}/json")
        if r.status_code == 200:
            # In case we need to check all previous version ... enable this block
            # ---------
            # versions = [PyPiVersion(version) for version in list(r.json()["releases"].keys())]
            # versions.sort()
            # latest_version = versions[-1]
            # ---------
            # Latest release only
            latest_version = PyPiVersion(str(r.json()["info"]["version"]))
    except Exception as e:
        LOGGER.error(f"ERROR: Checking the pypi API for |{packaget_name}| => {str(e)}")
    return latest_version
