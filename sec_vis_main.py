import rhinoscriptsyntax as rs

#Define the image paremeters
img_zoo = 5
img_fol = '/Users/Rog/Desktop/test'
img_wid = 1280
img_hei = 800
img_sca = 1

pfx_axo = '/axo/img_'
pfx_sec = '/sec/sec_'

#Create a working layer
lay_wor = rs.AddLayer(name='lay_wor',visible=True)
rs.CurrentLayer(lay_wor)

#Select object to be sliced, copy it, group it and move it to the working layer
obj_sel = rs.GetObjects(message='Select the objects to be visualized:', group=True)
obj_cop = rs.CopyObject(obj_sel)

rs.AddGroup(group_name='obj_all')
rs.AddObjectToGroup(obj_cop,'obj_all')

obj_all = rs.ObjectsByGroup('obj_all')
rs.ObjectLayer(obj_all,'lay_wor')

#Turn off all layers but the working one
lay_lis = rs.LayerNames()

for i in range(len(lay_lis)):
    if lay_lis[i] == 'lay_wor':
        rs.LayerVisible(lay_lis[i],visible=True)
    else:
        rs.LayerVisible(lay_lis[i],visible=False)

#Create the layers needed to highlight the section views and hide the clipping plane
lay_axo_sec = rs.AddLayer(name='lay_axo_sec',color=(255,255,0),visible=True)
lay_axo_pla = rs.AddLayer(name='lay_axo_pla',visible=False)
lay_fro_sec = rs.AddLayer(name='lay_fro_sec',visible=True)
lay_fro_pla = rs.AddLayer(name='lay_fro_pla',visible=False)

rs.LayerPrintColor('lay_axo_sec',color=(255,255,0))
rs.LayerPrintWidth('lay_fro_sec')

#Change the main object name and create a list of the points for the bounding box to be used to align with origin
rs.ObjectName(obj_all,'obj_main')
obj_cen = rs.BoundingBox(obj_all,view_or_plane='Perspective')

#Move selection to the origin of the working plane
env_org = rs.coerce3dpoint([0,0,0])
obj_cor = (obj_cen[0]+obj_cen[6])/2
rs.MoveObject(obj_all,env_org-obj_cor)

#Create a proper bounding box now that the part is centered
obj_box = rs.BoundingBox(obj_all,view_or_plane='Perspective')

# #Print coordinades with tags for visualization purposes
# for i, point in enumerate(obj_box):
#     rs.AddTextDot(i,point)

#Grab the relevant coordinades from the list only and name them O, X , Y and Z
crd_rel = []
ind_rel = [0,1,3,4]

for i in ind_rel:
    crd_rel.append(obj_box[i])
    if i == 0:
        crd_o = obj_box[i]
    if i == 1:
        crd_x = obj_box[i]
    if i == 3:
        crd_y = obj_box[i]
    if i == 4:
        crd_z = obj_box[i]
    else:
        pass

#Calculate the height, width and depth of the model
obj_hei = round(rs.Distance(crd_o,crd_z),2)
obj_wid = round(rs.Distance(crd_o,crd_x),2)
obj_dep = round(rs.Distance(crd_o,crd_y),2)

#Print the bounding box dimensions
print('The model is: {}(width) * {}(height) * {}(depth)'.format(obj_wid,obj_hei,obj_dep))

#Ask for the resolution of the section view animation and calculate the step value
#vis_res = rs.GetInteger(message='Please insert the resolution for the animation (number of slices)',number=10,minimum=2,maximum=100)
vis_res = 5
vis_ste = obj_dep/vis_res

#Calculate the starting point for the clipping plane
pla_org = -crd_o
pla_org[1] = pla_org[1] + (vis_ste/2)
pla_pos = pla_org

#Transform the width of the object into a 3D point
pnt_ste = (-obj_wid,0,0)

#Prepare the view for the axonometric view captures
rs.CurrentView(view='Perspective')
rs.ObjectsByName('obj_main',select=True)
rs.ZoomSelected()
rs.UnselectAllObjects()
for i in range(img_zoo):
    rs.Command('Zoom Out')

#Main loop taking the axonometry shots on each iteration
for i in range(vis_res+2):

    #Clipping plane
    pla_obj = rs.AddClippingPlane(rs.WorldZXPlane(),obj_wid,obj_hei,views='Perspective')
    rs.ObjectLayer(pla_obj,'lay_axo_pla')
    rs.MoveObject(pla_obj,pla_pos)

    #Section start and end
    sec_str = pla_pos
    sec_end = rs.PointAdd(pla_pos,pnt_ste)

    #Create and select the section curve
    rs.CurrentLayer(layer='lay_axo_sec')
    rs.ObjectsByName('obj_main',select=True)
    rs.CurrentView('Top')
    rs.Command('-_Section ' + str(sec_str) + ' ' + str(sec_end) + ' _Enter')
    sec_cur = rs.ObjectsByType(4)

    #Take the shot
    rs.CurrentView('Perspective')
    img_des = img_fol + pfx_axo + str(i) + '.png'
    rs.Command('-_ViewCaptureToFile ' + img_des + ' _DrawGrid=No' + ' _Width=' + str(img_wid) + ' _Height=' + str(img_hei) + ' _Scale=' + str(img_sca) + ' _TransparentBackground=No' + ' _Enter' + ' _Enter')

    #Prepare the environment for the next iteration
    pla_pos[1] = pla_pos[1] - vis_ste
    rs.DeleteObjects(pla_obj)
    rs.DeleteObjects(sec_cur)

rs.CurrentLayer(layer='lay_wor')

#Reset the plane origin coordinates
pla_org = -crd_o
pla_org[1] = pla_org[1] + (vis_ste/2)
pla_pos = pla_org

#Prepare the view for the frontal view captures
rs.CurrentView(view='Front')
rs.ObjectsByName('obj_main',select=True)
rs.ZoomSelected()
rs.UnselectAllObjects()
for i in range(img_zoo):
    rs.Command('Zoom Out')

for i in range(vis_res+2):

    #Clipping plane
    pla_obj = rs.AddClippingPlane(rs.WorldZXPlane(),obj_wid,obj_hei,views='Perspective')
    rs.ObjectLayer(pla_obj,'lay_fro_pla')
    rs.MoveObject(pla_obj,pla_pos)

    #Section start and end points
    sec_str = pla_pos
    sec_end = rs.PointAdd(pla_pos,pnt_ste)

    #Create the section view
    rs.CurrentLayer(layer='lay_fro_sec')
    rs.SelectObjects(obj_all)
    rs.CurrentView('Top')
    rs.Command('-_Section ' + str(sec_str) + ' ' + str(sec_end) + ' _Enter')

    #Prepare the shot
    rs.CurrentView('Front')
    rs.HideObjects(obj_all)
    rs.UnselectAllObjects()

    #Take the shot
    img_des = img_fol + pfx_sec + str(i) + '.png'
    rs.Command('-_ViewCaptureToFile ' + img_des + ' _DrawGrid=No' + ' _Width=' + str(img_wid) + ' _Height=' + str(img_hei) + ' _Scale=' + str(img_sca) + ' _TransparentBackground=No' + ' _Enter' + ' _Enter')

    #Prepare the environment for the next iteration
    pla_pos[1] = pla_pos[1] - vis_ste
    rs.ShowObjects(obj_all)
    rs.DeleteObjects(pla_obj)
    sec_cur = rs.ObjectsByType(4)
    rs.DeleteObjects(sec_cur)

if 'Default' in lay_lis:
    rs.CurrentLayer(layer='Default')
else:
    rs.AddLayer(name='Default')
    rs.CurrentLayer(layer='Default')

#Purge the environment
rs.PurgeLayer('lay_axo_sec')
rs.PurgeLayer('lay_axo_pla')
rs.PurgeLayer('lay_fro_sec')
rs.PurgeLayer('lay_fro_pla')
rs.PurgeLayer('lay_wor')

print ('\n Section views ready! \n')
