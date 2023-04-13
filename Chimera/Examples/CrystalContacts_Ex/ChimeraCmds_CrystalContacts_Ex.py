import sys
sys.path.append('../../')
from ChimeraCmdGenerator import *

ChimeraCmds = ChimeraCmdGenerator(mrcDirectory='./',
                                  pdbDirectory='./')

print('\n')

importCmd = ChimeraCmds.import_and_initializeChimera()

CrystalContactCmd = ChimeraCmds.ChimeraXtalContactLogFileParser_3Partners(filename='RGA_xtalContactsBreakdown_Chimera_v2.txt',
                                                sym1='5',
                                                sym2='1',
                                                sym3='2',
                                                exceptRes='401')

print('Contact distances are measured from Calpha to Calpha')
print('\nThe sym values may need to be changed.')
print('If more or less symmetry pairs exist, the function will require updating.')