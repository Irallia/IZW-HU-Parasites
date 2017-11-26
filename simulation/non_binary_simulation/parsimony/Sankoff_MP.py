from rpy2 import robjects
from rpy2.robjects import Formula, Environment
from rpy2.robjects.vectors import IntVector, FloatVector
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr, data
from rpy2.rinterface import RRuntimeError
import warnings

def sankoff_parsimony(tree_clade, nodelist):
    
    # The R 'print' function
    rprint = robjects.globalenv.get("print")
    stats = importr('stats')
    grdevices = importr('grDevices')
    base = importr('base')
    datasets = importr('datasets')


    return






# import math, datetime
# import rpy2.robjects.lib.ggplot2 as ggplot2
# import rpy2.robjects as ro
# from rpy2.robjects.packages import importr
# base = importr('base')

# mtcars = data(datasets).fetch('mtcars')['mtcars']

# pp = ggplot2.ggplot(mtcars) + \
#      ggplot2.aes_string(x='wt', y='mpg', col='factor(cyl)') + \
#      ggplot2.geom_point() + \
#      ggplot2.geom_smooth(ggplot2.aes_string(group = 'cyl'),
#                          method = 'lm')
# pp.plot()
