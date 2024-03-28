from __future__ import annotations

from collections import defaultdict
from collections.abc import Collection
from itertools import groupby
import json
import re
from urllib.request import urlopen

import click
import pandas as pd
from pkg_resources import Requirement, parse_version

__all__ = ['cli']

# Dummy requirement that cannot be satisfied
BAD_REQUIREMENT = Requirement.parse('python<0,>0')

def _get_requires_python_constraint(dist_data: dict[str, str]) -> Requirement | None:
    requires_python_data: str | None = dist_data.get('requires_python')
    if requires_python_data is None:
        return None

    return Requirement.parse(f'python{requires_python_data}')

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
        bdist_constraint = Requirement.parse(f'python=={major}.{minor}.*')
    else:
        bdist_constraint = Requirement.parse(f'python=={major}.*')

    if requires_python_constraint is None:
        return [bdist_constraint]
    else:
        return [requires_python_constraint, bdist_constraint]

@click.command()
@click.argument('package_name', type=str)
@click.option('--python', 'python_versions', metavar='<VERSIONS>', type=str, required=True, help='A comma-separated list of Python versions to check against')
def cli(package_name: str, python_versions: str) -> None:
    """Show the versions of a PyPI package that are compatible with each Python version."""
    python_versions_lst = python_versions.split(',')
    output = defaultdict(lambda: defaultdict(lambda: ''))

    data = json.load(urlopen(f'https://pypi.org/pypi/{package_name}/json'))
    for package_version, release_data in data['releases'].items():
        for dist_data in release_data:
            python_requirements = _get_python_requirements(dist_data)

            for python_version in python_versions_lst:
                if all(python_version in r for r in python_requirements):
                    output[python_version][package_version] = 'Y'

    output_df = pd.DataFrame.from_dict(data=output, orient='index').fillna('')

    # We only care about the latest patch version for each minor version
    output_columns = tuple(str(c) for c in output_df.columns)
    latest_patches = [
        max(columns, key=parse_version)
        for _, columns in groupby(output_columns, key=lambda s: parse_version(s).release[:2])
    ]

    formatted_output_df = output_df \
        .loc[sorted(output_df.index, key=parse_version), sorted(latest_patches, key=parse_version)] \
        .rename_axis(index='Python (↓)', columns=f'{package_name} (→)')

    click.echo(formatted_output_df)
