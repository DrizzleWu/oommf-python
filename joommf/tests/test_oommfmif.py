import os

import pytest

import joommf.oommfmif as o



def test_retrieve_oommf_executable(tmpdir):
    oommf_path = o.get_oommf_path()
    executable = o.retrieve_oommf_executable(oommf_path)
    assert executable in ['oommf', 'oommf.tcl']

    # a directory with no files, should raise an exception
    with pytest.raises(RuntimeError):
        executable = o.retrieve_oommf_executable(str(tmpdir))


def test_get_oommf_version():
    return_string = o.get_version()
    assert return_string[0:4] == "1.2."


def test_get_oommf_path():
    assert isinstance(o.get_oommf_path(), str)


def test_run_oommf_simulation(tmpdir):

    testsim_mif_1 = """# MIF 2.1
# Tiny test problem, OOMMF-Python

Specify Oxs_BoxAtlas:atlas {
  xrange {0 5e-9}
  yrange {0 5e-9}
  zrange {0 10e-9}
}

Specify Oxs_RectangularMesh:mesh {
  cellsize {2.5e-9 2.5e-9 2.5e-9}
  atlas :atlas
}

Specify Oxs_UniformExchange {A  13e-12}

Specify Oxs_EulerEvolve {
  alpha 0.5
  start_dm 0.0001
  gamma_G 0.2211e6
  absolute_step_error 0.02
  relative_step_error 0.02
}

Specify Oxs_Demag {}

Specify Oxs_TimeDriver {
 basename testsim
 evolver Oxs_EulerEvolve
 stopping_dm_dt 0.01
 mesh :mesh
 stage_count 1
 stage_iteration_limit 550000
 total_iteration_limit 2
 Ms { Oxs_UniformScalarField { value 0.86e6 } }
 m0 { Oxs_UniformVectorField {
  norm 1
  vector {1 0 1}
 } }
}

Destination archive mmArchive

Schedule DataTable archive Step 1
Schedule Oxs_TimeDriver::Magnetization archive Stage 1
"""

    # write config file into tmp directory
    open(os.path.join(str(tmpdir), 'testsim.mif'), 'w').write(testsim_mif_1)

    # call ommff
    process = o.call_oommf('boxsi testsim.mif', workdir=tmpdir)

    # wait for oommf to complete
    process.wait()

    # read stdout and stderr, so we can see those in case of error
    # via "py.test -l"
    stdout, stderr = process.stdout.read(), process.stderr.read()
    print("stdout = {}".format(stdout))
    print("stderr = {}".format(stderr))

    files = os.listdir(str(tmpdir))
    print("Files in tmpdirectory are:\n{}".format(files))
    assert "testsim-Oxs_TimeDriver-Magnetization-00-0000002.omf" in files or\
        "testsim-Oxs_TimeDriver-Magnetization-00-0000001.omf" in files

    # I would have expected to only get
    # testsim-Oxs_TimeDriver-Magnetization-00-0000001.omf as the output,
    # and this is the case for the
    # conda-OOMMF install of 1.2.0.6. However, with the from source install of
    # 1.2.0.5, we get the testsim-Oxs_TimeDriver-Magnetization-00-0000002.omf
    # created. So we accept either in this test -- at least OOMMF runs and
    # does something. HF, 1 Nov 2015

    assert 'testsim.odt' in files
