import joommf.drivers.evolver as evolver



def test_llg_mif():
    t = 1.5e-9
    m_init = (0, 1, 0)
    Ms = 1e6
    alpha = 0.01
    gamma = 2.21e5
    name = 'llgtest'

    llg = evolver.LLG(t, m_init, Ms, alpha, gamma, name)

    mif_string = llg.get_mif()

    lines = mif_string.split('\n')

    assert 'Specify Oxs_RungeKuttaEvolve' in lines[0]
    assert 'alpha 0.01000' in lines[1]
    assert 'gamma_G 221000.00000' in lines[2]
    assert 'start_dm 0.01' in lines[3]


def test_llg_formatting():
    t = 1.5e-9
    m_init = (0, 1, 0)
    Ms = 1e6
    alpha = 0.01
    gamma = 2.21e5
    name = 'test_llg'

    evolver_object = evolver.LLG(t, m_init, Ms, alpha, gamma, name)

    mif_string = evolver_object.get_mif()

    assert mif_string[0] == 'S'
    assert mif_string[-1] == '\n'
    assert mif_string[-2] == '\n'


def test_minevolve():
    m_init = (0, 1, 0)
    Ms = 1e6
    name = 'llgtest'
    evolver_object = evolver.Minimiser(m_init, Ms, name)
    mif_string = evolver_object.get_mif()
    lines = mif_string.split('\n')
    print(lines)
