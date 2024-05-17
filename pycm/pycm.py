from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Collection, Hashable, Iterable
import json
import re
from typing import TypeVar
from urllib.request import urlopen

from packaging.requirements import Requirement
from packaging.version import Version
import pandas as pd

__all__ = ['pycm']

# Dummy requirement that cannot be satisfied
BAD_REQUIREMENT = Requirement('python<0,>0')

def _get_requires_python_constraint(dist_data: dict[str, str]) -> Requirement | None:
    requires_python_data: str | None = dist_data.get('requires_python')
    if requires_python_data is None:
        return None

    return Requirement(f'python{requires_python_data}')

def _get_python_requirements(dist_data: dict[str, str]) -> Collection[Requirement]:
    requires_python_constraint = _get_requires_python_constraint(dist_data)

    python_version_data: str | None = dist_data.get('python_version')
    if python_version_data is None or python_version_data == 'source':
        return [] if requires_python_constraint is None else [requires_python_constraint]

    m = re.match(r'[a-z]{2}([0-9])([0-9]*)', python_version_data)
    if m is None:
        return [BAD_REQUIREMENT] if requires_python_constraint is None else [requires_python_constraint]

    major, minor = m.groups()
    if minor:
        bdist_constraint = Requirement(f'python=={major}.{minor}.*')
    else:
        bdist_constraint = Requirement(f'python=={major}.*')

    if requires_python_constraint is None:
        return [bdist_constraint]
    else:
        return [requires_python_constraint, bdist_constraint]

_K = TypeVar('_K', bound=Hashable)
_V = TypeVar('_V')

def _full_groupby(values: Iterable[_V], *, key: Callable[[_V], _K]):
    """Unlike :class:`itertools.groupby`, groups are not broken by non-contiguous data."""
    groups: dict[_K, list[_V]] = defaultdict(list)

    for value in values:
        groups[key(value)].append(value)

    return groups.items()

def pycm(package_name: str, python_versions: list[str], *, groupby_patch: bool = True) -> pd.DataFrame:
    """Show the versions of a PyPI package that are compatible with each Python version."""
    output = defaultdict(lambda: defaultdict(lambda: ''))

    data = json.load(urlopen(f'https://pypi.org/pypi/{package_name}/json'))
    for package_version, release_data in data['releases'].items():
        for dist_data in release_data:
            python_requirements = _get_python_requirements(dist_data)

            for python_version in python_versions:
                if all(python_version in r.specifier for r in python_requirements):
                    output[python_version][package_version] = 'Y'

    output_df = pd.DataFrame.from_dict(data=output, orient='index').fillna('')

    if groupby_patch:
        # We only care about the latest patch version for each minor version
        output_columns = tuple(str(c) for c in output_df.columns)
        output_columns = [
            max(columns, key=Version)
            for _, columns in _full_groupby(output_columns, key=lambda s: Version(s).release[:2])
        ]
    else:
        output_columns = output_df.columns

    return output_df \
        .loc[sorted(output_df.index, key=Version), sorted(output_columns, key=Version)] \
        .rename_axis(index='Python (↓)', columns=f'{package_name} (→)')
