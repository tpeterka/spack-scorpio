# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scorpio(CMakePackage):
    """Software for Caching Output and Reads for Parallel I/O (SCORPIO)"""

    # this is the actual public repo of the E3SM-Project (use this)
    homepage = "https://github.com/E3SM-Project/scorpio.git"
    url      = "https://github.com/E3SM-Project/scorpio.git"
    git      = "https://github.com/E3SM-Project/scorpio.git"

    # the following uses my fork for testing
    #homepage = "https://github.com/tpeterka/scorpio.git"
    #url      = "https://github.com/tpeterka/scorpio.git"
    #git      = "https://github.com/tpeterka/scorpio.git"

    # the following uses my local repo (for debugging)
    #homepage = "/home/tpeterka/software/tpeterka-scorpio"
    #url      = "/home/tpeterka/software/tpeterka-scorpio"
    #git      = "/home/tpeterka/software/tpeterka-scorpio"

    version('master', branch='master')

    depends_on('mpich@4.0.2')
    depends_on('hdf5+mpi+hl@1.12.1 ^mpich', type='link')
    depends_on('netcdf-c@4.8.1 +mpi ^mpich', type='link')
    depends_on('parallel-netcdf@1.12.2 -shared', type='link')

    variant("netcdf", default=True, description="Build with NetCDF")
    variant("hdf5", default=False, description="Build with HDF5")
    variant("tests", default=False, description="Build tests")
    variant("examples", default=False, description="Build examples")

    def cmake_args(self):
        args = ['-DCMAKE_C_COMPILER=%s' % self.spec['mpich'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpich'].mpicxx,
                '-DCMAKE_FC_COMPILER=%s' % self.spec['mpich'].mpifc,
                '-DBUILD_SHARED_LIBS=true',
                '-DPIO_USE_MALLOC=true',
                '-DCMAKE_C_FLAGS=-fPIC',
                '-DCMAKE_CXX_FLAGS=-fPIC',
                '-DPIO_ENABLE_TIMING=false',
                self.define_from_variant("WITH_NETCDF", "netcdf"),
                self.define_from_variant("WITH_HDF5", "hdf5"),
                self.define_from_variant("PIO_ENABLE_TESTS", "tests"),
                self.define_from_variant("PIO_ENABLE_EXAMPLES", "tests"),
                '-DHDF5_PATH=%s' % self.spec['hdf5'].prefix,
                '-DNetCDF_PATH=%s' % self.spec['netcdf-c'].prefix,
                '-DPnetCDF_PATH=%s' % self.spec['parallel-netcdf'].prefix]

        return args
