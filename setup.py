# rm -rf build/ && python setup.py build_static build && cp build/lib.win-amd64-cpython-310/pysqlite3/_sqlite3.cp310-win_amd64.pyd pysqlite3/ && python setup.py test

# -*- coding: ISO-8859-1 -*-
# setup.py: the distutils script
#
import os
import setuptools
import sys

import distutils.command.build_ext
import setuptools

# If you need to change anything, it should be enough to change setup.cfg.

PACKAGE_NAME = 'pysqlite3'

# define sqlite sources
sources = [os.path.join('src', source)
           for source in ["module.c", "connection.c", "cursor.c", "cache.c",
                          "microprotocols.c", "prepare_protocol.c",
                          "statement.c", "util.c", "row.c", "blob.c"]]

# Work around clang raising hard error for unused arguments
if sys.platform == "darwin":
    os.environ['CFLAGS'] = "-Qunused-arguments"

class AmalgationLibSqliteBuilder(distutils.command.build_ext.build_ext):
    description = "Builds a C extension using a sqlite3 amalgamation"

    amalgamation_root = "."
    amalgamation_header = os.path.join(amalgamation_root, 'sqlite3.h')
    amalgamation_source = os.path.join(amalgamation_root, 'sqlite3.c')

    amalgamation_message = ('Sqlite amalgamation not found. Please download '
                            'or build the amalgamation and make sure the '
                            'following files are present in the pysqlite3 '
                            'folder: sqlite3.h, sqlite3.c')

    def build_extension(self, ext):
        ext.define_macros = [
            ('MODULE_NAME', '"pysqlite3.dbapi2"'),
        # Feature-ful library.
            ('SQLITE_ALLOW_COVERING_INDEX_SCAN', '1'),
            ('SQLITE_ENABLE_FTS3', '1'),
            ('SQLITE_ENABLE_FTS3_PARENTHESIS', '1'),
            ('SQLITE_ENABLE_FTS4', '1'),
            ('SQLITE_ENABLE_FTS5', '1'),
            ('SQLITE_ENABLE_JSON1', '1'),
            ('SQLITE_ENABLE_LOAD_EXTENSION', '1'),
            ('SQLITE_ENABLE_MATH_FUNCTIONS', '1'),
            ('SQLITE_ENABLE_RTREE', '1'),
            ('SQLITE_ENABLE_STAT4', '1'),
            ('SQLITE_ENABLE_UPDATE_DELETE_LIMIT', '1'),
            ('SQLITE_SOUNDEX', '1'),
            ('SQLITE_USE_URI', '1'),
        # Always use memory for temp store.
            ('SQLITE_TEMP_STORE', '3'),
        # Increase the maximum number of "host parameters" which SQLite will accept
            ('SQLITE_MAX_VARIABLE_NUMBER', '250000'),
        # Increase maximum allowed memory-map size to 1TB
            ('SQLITE_MAX_MMAP_SIZE', '1099511627776')
        ]

        ext.include_dirs.append(self.amalgamation_root)
        ext.sources.append(os.path.join(self.amalgamation_root, "sqlite3.c"))

        if sys.platform != "win32":
            # Include math library, required for fts5.
            ext.extra_link_args.append("-lm")

        # ext.libraries.append('sqlite3')
        distutils.command.build_ext.build_ext.build_extension(self, ext)

    def __setattr__(self, k, v):
        # Make sure we don't link against the SQLite
        # library, no matter what setup.cfg says
        if k == "libraries":
            v = None
        self.__dict__[k] = v


def get_setup_args():
    return dict(
        name="pysqlite3",
        version="0.1",
        description="DB-API 2.0 interface for Sqlite 3.x",
        package_dir={"pysqlite3": "pysqlite3"},
        ext_modules=[setuptools.Extension(
            name="pysqlite3._sqlite3",
            sources=sources,
            )
        ],
        cmdclass={
            "build_static": AmalgationLibSqliteBuilder
        }
    )


if __name__ == "__main__":
    setuptools.setup(**get_setup_args())
