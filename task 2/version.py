import re
from functools import total_ordering
from tabulate import tabulate

@total_ordering
class Version:
    """
    A version class.

    :param int major: version when you make incompatible API changes.
    :param int minor: version when you add functionality in
                      a backwards-compatible manner.
    :param int patch: version when you make backwards-compatible bug fixes.
    :param str release: an optional prerelease string
    :param str meta: an optional meta information
    """
    # here is mine regexp "^(\d+)\.(\d+)\.(\d+)(?:-(\w+(?:\.(?:\w|\d)+)*))?(?:\+\S+)?$", but the one below is better
    # on a wide variety of inputs, I found it on http://semver.org/
    regular = "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    # if try to break it in a few lines it doesn't work anymore
    precedence = {"alpha": 0, "a": 0, "beta": 1, "b": 1, "rc": 2}
    _regex = re.compile(regular)

    def __init__(self, version :str):
        if self._regex.fullmatch(version):
            self.version = version
            self.parsed = self._regex.search(self.version).groups()
            self.major, self.minor, self.patch, self.release, self.meta = self.parsed
        else:
            class NotValidVersion(Exception):
                def __init__(self, message):
                    self.message = message
            raise NotValidVersion(f'provided version \'{version}\' is not valid')


    def __lt__(self, another): # <
        left = (self.major, self.minor, self.patch)
        right = (another.major, another.minor, another.patch)

        if left != right:
            # by the rules of tuple comparison
            return left < right
        else:
            # here I'm trying to create tuples based on 'release' substring to compare them
            # precedence dictionary stores values for each conventional word (like 'alpha') and makes
            # possible to compare them
            try:
                left_release = [int(self.precedence.get(x, x)) for x in self.release.split('.')]
                right_release = [int(self.precedence.get(x, x)) for x in another.release.split('.')]
            except ValueError:
                # if conventional word wasn't found then I just compare sizes of the strings
                return len(self.release) < len(another.release)
            except AttributeError:
                # if 'release' of one object is 'None'
                return True if self.release else False
            else:
                # if everything went fine
                return left_release < right_release

    
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
    ]

    for version_1, version_2 in to_test:
        print(tabulate(
                        [
                            [f'{version_1} < {version_2} ', Version(version_1) < Version(version_2)], 
                            [f'{version_1} > {version_2} ', Version(version_1) > Version(version_2)],
                            [f'{version_1} != {version_2} ', Version(version_1) != Version(version_2)]
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
###