import rhinoscriptsyntax as rs
from sec_vis_func import Mod_siz

print('The model is: {}(w) * {}(d) * {}(h).'.format(Mod_siz()[0],Mod_siz()[1],Mod_siz()[2]))

print(Mod_siz()[5])
