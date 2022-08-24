import friendzone.pyscf2 as fz
from simde import simde, chemist, pluginplay
from mokup import mokup

# The Mokup enumeration for the molecule
m_mol = mokup.molecule.h2

# The Mokup enumeration for the AO basis set
m_aos = mokup.basis_set.sto3g

mol = mokup.get_molecule(m_mol)
sys = chemist.ChemicalSystem(mol, 2)
aos = mokup.get_bases(m_mol, m_aos)

mm = pluginplay.ModuleManager()
fz.load_modules(mm)

[e] = mm.at("PySCF RHF").run_as[simde.AOEnergy](aos, sys)
print(e)
