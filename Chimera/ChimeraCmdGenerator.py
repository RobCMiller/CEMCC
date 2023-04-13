# General Code for generating a Chimera script to input .mrc/.pdb files 

# Imports
import re

class ChimeraCmdGenerator:
  '''

  '''

  def __init__(self,
               mrcDirectory='',
               pdbDirectory=''):
    '''

    '''
    # self.mrcDirectory = input('List full path to the directory containing .mrc files (even if it is just one), ending the path with a forward slash: ')
    self.mrcDirectory = mrcDirectory
    self.pdbDirectory = pdbDirectory

    self.displaySettings = 'lighting mode two-point ;  lighting brightness 1.12 ; lighting contrast 0.73 ; lighting ratio 1.55 ;  set dcStart 0.25 ;  set dcEnd 0.5 ;  set depthCue ;   set silhouetteWidth 6 ;  set silhouette ;  set singleLayer ;'

    if self.mrcDirectory != '':
      print('The available functions are: ')
      for j in dir(self):
        if '__' not in j and 'Directory' not in j:
          print(j)
      print('')
      print('All commands should accept the helpCmd=True flag and list the function inputs/outputs')
    if self.mrcDirectory.endswith('/') != True:
      self.mrcDirectory = self.mrcDirectory + '/*.mrc'
    else:
      self.mrcDirectory = self.mrcDirectory + '*.mrc'
    if self.pdbDirectory.endswith('/') != True:
      self.pdbDirectory = self.pdbDirectory + '/*.pdb'
    else:
      self.pdbDirectory = self.pdbDirectory + '*.pdb'


  def import_and_initializeChimera(self,helpCmd=False):
    '''
    Describe
    '''
    if helpCmd==True:
      print('This command requires no inputs')
      print('It will generate a set of commands that import .mrc and .pdb files from a particular directory and change the view settings of the session.')
      import_and_initializeCmd = 'No Command Generated - Help command called'
    else:
      import_and_initializeCmd = 'open ' + self.mrcDirectory + ' ; ' + 'open ' + self.pdbDirectory+ ' ; ' + self.displaySettings
      print(import_and_initializeCmd)

    return import_and_initializeCmd

  def colorByLocalResolution(self,
                             helpCmd=False,
                             surface='#0',
                             LocResMap='#1',
                             resolutionRange=['2.5','3.5','6.0'],
                             resolutionColors=['#1177c2','#9b9c9c','#da2f05']):
    '''
    returns command for color surface by local resolution and generating the corresponding color key
    '''
    if helpCmd == True:
      colorByLocalResolutionCmd, colorKey = ['No surface color command generated.','No color key generated.']
      print('This command requires 4 inputs:')
      print('surface: the surface to be colored (default #0')
      print('LocResMap: data file used to color surface (default #1')
      print('resolutionRange: range of data values to color surface over (default [\'2.5\',\'3.5\',\'6.0\'])')
      print('resolutionColors: colors to map over the range of data values (default [\'#1177c2\',\'#9b9c9c\',\'#da2f05\'])')
    else:
      resCmds = []
      for j,z in zip(resolutionRange, resolutionColors):
        resCmds.append('%s,%s:'%(str(j), str(z)))

      resCmds[-1] = resCmds[-1].replace(':','')
      resCmds = ''.join(resCmds)
      colorByLocalResolutionCmd = 'scolor %s volume %s cmap %s ; surftransparency 30 #0 ; '%(str(surface), str(LocResMap), str(resCmds))

      resCmds2 = []
      for j,z in zip(resolutionRange, resolutionColors):
        resCmds2.append('%s %s'%(str(j), str(z)))
      resCmds2 = ''.join(resCmds2)

      colorKey = 'colorkey 0.94,0.9 0.97,0.1 fontSize 48 fontStyle bold borderColor black borderWidth 8 %s'%str(resCmds2)

      print(colorByLocalResolutionCmd)
      print(colorKey)
    return colorByLocalResolutionCmd, colorKey

  def buildZoneMap(self,
                   helpCmd=False,
                   map='#0',
                   model='#1',
                   specifier='1-20.A@ca', # first twenty residues of chain, Calphas
                   cutRadius = 1.5):
    '''
    specifier: PALA in chain C
    '''
    if helpCmd == True:
      print('This function requires 4 inputs:')
      print('map: the map to cut out of (default: #0)')
      print('model: reference model for cutting map around (default: #1)')
      print('specifier: where specifically in the map/model to cut the zone map (default: 1-20.A@ca - residues 1-20 of chain A, just the alpha carbons)')
      print('cutRadius: diameter of zone map to cut around, which is adjusted via threshold values (default: 1.5 - in Angstroms)')
      zoneCmd = 'No zone command generated.'
    else:
      zoneCmd = 'vop zone %s %s:%s radius %s'%(str(map),str(model),str(specifier),str(cutRadius))
      print(zoneCmd)

    return zoneCmd

  def ChimeraXtalContactLogFileParser_3Partners(self,filename,
                                                sym1='5',
                                                sym2='1',
                                                sym3='2',
                                                exceptRes=None):
    '''
    group 1 = ID
    group 2 = Res #
    group 3 = chain ID

    group 5 = ID 2
    group 6 = Res # 2
    group 7 = chain ID 2
    group 9 = symexp

    for symexp 
    symexp 5 = model #1
    symexp 1 = model #2
    symexp 2 = model #3

    reference model = model #0
    '''
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    p = re.compile(r'\s+[A-Z]{3}')
    p2 = re.compile(r'\s+([A-Z]{3})\s(\d+)\s([A-Z]{1})\s*(\d)\s*([A-Z]{3})\s(\d+)\s([A-Z]{1})\s*(\d)\s*(\d)')

    cmdList = []

    for j in lines:
      if p.match(j) is not None:
        if p2.match(j).group(9) == sym1:
          model = '1'
        elif p2.match(j).group(9) == sym2:
          model = '2'
        elif p2.match(j).group(9) == sym3:
          model = '3'
        cmd = 'distance #%s:%s.%s@ca #%s:%s.%s@ca ; '%( '0', p2.match(j).group(2), p2.match(j).group(3), str(model), p2.match(j).group(6), p2.match(j).group(7) )

        if exceptRes is None:
          cmdList.append(cmd)
        elif str(exceptRes) in cmd:
          continue
        else:
          cmdList.append(cmd)

    print("".join(cmdList))

    return "".join(cmdList)

  def localCorrelationBtwVolumes(self):
    '''

    '''
    locCorCmd = 'vop localCor ;lkajd;lkajds;lkj'

  def morphBtwMaps(self):
    '''

    '''
    morphBtwMapCmd = ''
    print(morphBtwMapsCmd)

  def alignMaps(self):
    '''

    '''
    print('Hello World')

  def alignStructures(self):
    '''
    '''
    print('Hello World')












ChimeraClass_Tests = ChimeraCmdGenerator()