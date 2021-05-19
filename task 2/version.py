import re
from functools import total_ordering
from tabulate import tabulate

@total_ordering
class Version:
    """
    A version class.

    :param int major: version when you make incompatible API changes.
    :param int minor: version when you add functionality in a backwards-compatible manner.
    :param int patch: version when you make backwards-compatible bug fixes.
    :param str release: an optional prerelease string
    :param str meta: an optional meta information
    """

    regular = '''^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)
                  (?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                  (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
                  (?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'''

    _regex = re.compile(regular, re.X)

    class NotValidVersion(Exception):
        def __init__(self, message):
            self.message = message

    def __init__(self, version :str):
        if self._regex.fullmatch(version):
            self.version = version
            self.parsed = self._regex.search(self.version).groups()
            self.major, self.minor, self.patch, self.release, self.meta = self.parsed
        else:
            raise self.NotValidVersion(f'provided version \'{version}\' is not valid')


    def __lt__(self, another):
        try:
            left = (self.major, self.minor, self.patch, self.release.split('.'))
            right = (another.major, another.minor, another.patch, another.release.split('.'))
        except AttributeError:
            return bool(self.release)
        else:
            return left < right


    def __eq__(self, another):
        return self.parsed == another.parsed


    def __str__(self):
        return self.version


def test():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1-b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ('1.2.3-rc.2', '1.2.3-beta.0'),
    ]

    for version_1, version_2 in to_test:
        ver_1 = Version(version_1)
        ver_2 = Version(version_2)

        print(tabulate(
                        [
                            [f'{version_1} < {version_2} ', ver_1 < ver_2], 
                            [f'{version_1} > {version_2} ', ver_1 > ver_2],
                            [f'{version_1} != {version_2} ', ver_1 != ver_2]
                        ],
                            headers=['expression', 'result'], tablefmt='fancy_grid'
                      )
            )

if __name__ == "__main__":
    test()
    # ver = Version('1.0.1b')
    # is invalid and will throw an exception

### output:
# ╒════════════════╤══════════╕
# │ expression     │ result   │
# ╞════════════════╪══════════╡
# │ 1.0.0 < 2.0.0  │ True     │
# ├────────────────┼──────────┤
# │ 1.0.0 > 2.0.0  │ False    │
# ├────────────────┼──────────┤
# │ 1.0.0 != 2.0.0 │ True     │
# ╘════════════════╧══════════╛
# ╒═════════════════╤══════════╕
# │ expression      │ result   │
# ╞═════════════════╪══════════╡
# │ 1.0.0 < 1.42.0  │ True     │
# ├─────────────────┼──────────┤
# │ 1.0.0 > 1.42.0  │ False    │
# ├─────────────────┼──────────┤
# │ 1.0.0 != 1.42.0 │ True     │
# ╘═════════════════╧══════════╛
# ╒═════════════════╤══════════╕
# │ expression      │ result   │
# ╞═════════════════╪══════════╡
# │ 1.2.0 < 1.2.42  │ True     │
# ├─────────────────┼──────────┤
# │ 1.2.0 > 1.2.42  │ False    │
# ├─────────────────┼──────────┤
# │ 1.2.0 != 1.2.42 │ True     │
# ╘═════════════════╧══════════╛
# ╒══════════════════════════════╤══════════╕
# │ expression                   │ result   │
# ╞══════════════════════════════╪══════════╡
# │ 1.1.0-alpha < 1.2.0-alpha.1  │ True     │
# ├──────────────────────────────┼──────────┤
# │ 1.1.0-alpha > 1.2.0-alpha.1  │ False    │
# ├──────────────────────────────┼──────────┤
# │ 1.1.0-alpha != 1.2.0-alpha.1 │ True     │
# ╘══════════════════════════════╧══════════╛
# ╒══════════════════════════════╤══════════╕
# │ expression                   │ result   │
# ╞══════════════════════════════╪══════════╡
# │ 1.0.1-b < 1.0.10-alpha.beta  │ True     │
# ├──────────────────────────────┼──────────┤
# │ 1.0.1-b > 1.0.10-alpha.beta  │ False    │
# ├──────────────────────────────┼──────────┤
# │ 1.0.1-b != 1.0.10-alpha.beta │ True     │
# ╘══════════════════════════════╧══════════╛
# ╒═════════════════════╤══════════╕
# │ expression          │ result   │
# ╞═════════════════════╪══════════╡
# │ 1.0.0-rc.1 < 1.0.0  │ True     │
# ├─────────────────────┼──────────┤
# │ 1.0.0-rc.1 > 1.0.0  │ False    │
# ├─────────────────────┼──────────┤
# │ 1.0.0-rc.1 != 1.0.0 │ True     │
# ╘═════════════════════╧══════════╛
# ╒════════════════════════════╤══════════╕
# │ expression                 │ result   │
# ╞════════════════════════════╪══════════╡
# │ 1.2.3-rc.2 < 1.2.3-beta.0  │ False    │
# ├────────────────────────────┼──────────┤
# │ 1.2.3-rc.2 > 1.2.3-beta.0  │ True     │
# ├────────────────────────────┼──────────┤
# │ 1.2.3-rc.2 != 1.2.3-beta.0 │ True     │
# ╘════════════════════════════╧══════════╛
###