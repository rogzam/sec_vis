import rhinoscriptsyntax as rs

#Define the image paremeters
img_zoo = 5
img_fol = '/Users/Rog/Desktop/test'
img_pfx = '/axo/img_'
sec_pfx = '/sec/sec_'
img_wid = 1280
img_hei = 800
img_sca = 1

#Create a layer for the section curves

sec_lay = rs.AddLayer(name='sec_lay',color=(255,255,0),visible=True)
pla_lay = rs.AddLayer(name='pla_lay',visible=False)

rs.LayerPrintColor('sec_lay',color=(255,255,0))

#Select all visible objects
obj_all = rs.AllObjects(select=True)

#Change their name and create a list of the points for the object bounding box
rs.ObjectName(obj_all,'obj_main')
obj_box = rs.BoundingBox(obj_all)

#Print coordinades with tags for visualization purposes
#for i, point in enumerate(obj_box)
#    rs.AddTextDot(i,point)

#Grab the relevant coordinades from the list only and name them O, X , Y and Z
crd_rel = []
ind_rel = [0,1,3,4]

for i in ind_rel:
    crd_rel.append(obj_box[i])
    #pnt = rs.AddPoint(obj_box[i])
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
print('The model is: {}(width) * {}(depth) * {}(height)'.format(obj_wid,obj_hei,obj_hei))

#Create a layer to hide the clipping plane
#rs.AddLayer(name='cli_lay',visible=False)

#Ask for the resolution of the section view animation
#vis_res = rs.GetInteger(message='Please insert the resolution for the animation (number of slices)',number=10,minimum=2,maximum=100)
vis_res = 5

#Calculate the step value to move the plane
pla_org = -crd_o
vis_ste = obj_dep/vis_res
pla_org[1] = pla_org[1] + (vis_ste/2)
pla_pos = pla_org

#Create the start and end points for the section curve
pnt_ste = (-obj_wid,0,0)

#Center the objects with respect to the camera
#rs.Command('-_Perspective')

rs.CurrentView(view='Perspective')
rs.SelectObjects(obj_all)
rs.ZoomSelected()
rs.UnselectAllObjects()
for i in range(img_zoo):
    rs.Command('Zoom Out')

#Main loop taking the shots on each iteration
for i in range(vis_res+2):

    pla_obj = rs.AddClippingPlane(rs.WorldZXPlane(),50,50,views='Perspective')
    rs.ObjectLayer(pla_obj,'pla_lay')
    rs.MoveObject(pla_obj,pla_pos)

    sec_str = pla_pos
    sec_end = rs.PointAdd(pla_pos,pnt_ste)
    rs.CurrentLayer(layer='sec_lay')
    rs.SelectObjects(obj_all)
    rs.CurrentView('Top')
    rs.Command('-_Section ' + str(sec_str) + ' ' + str(sec_end) + ' _Enter')
    sec_cur = rs.ObjectsByType(4)
    img_des = img_fol + img_pfx + str(i) + '.png'
    rs.CurrentView('Perspective')
    rs.Command('-_ViewCaptureToFile ' + img_des + ' _DrawGrid=No' + ' _Width=' + str(img_wid) + ' _Height=' + str(img_hei) + ' _Scale=' + str(img_sca) + ' _TransparentBackground=No' + ' _Enter' + ' _Enter')
    #rs.AddPoint(sec_str)
    #rs.AddPoint(sec_end)
    pla_pos[1] = pla_pos[1] - vis_ste

    rs.DeleteObjects(pla_obj)
    rs.DeleteObjects(sec_cur)

rs.CurrentLayer(layer='Default')

rs.PurgeLayer('sec_lay')
rs.PurgeLayer('pla_lay')

ces_lay = rs.AddLayer(name='ces_lay',visible=True)
alp_lay = rs.AddLayer(name='alp_lay',visible=False)

pla_org = -crd_o
vis_ste = obj_dep/vis_res
pla_org[1] = pla_org[1] + (vis_ste/2)
pla_pos = pla_org

rs.CurrentView(view='Front')
rs.SelectObjects(obj_all)
rs.ZoomSelected()
rs.UnselectAllObjects()
for i in range(img_zoo):
    rs.Command('Zoom Out')

for i in range(vis_res+2):

    pla_obj = rs.AddClippingPlane(rs.WorldZXPlane(),50,50,views='Perspective')
    rs.ObjectLayer(pla_obj,'alp_lay')
    rs.MoveObject(pla_obj,pla_pos)

    sec_str = pla_pos
    sec_end = rs.PointAdd(pla_pos,pnt_ste)
    rs.CurrentLayer(layer='ces_lay')
    rs.SelectObjects(obj_all)
    rs.CurrentView('Top')
    rs.Command('-_Section ' + str(sec_str) + ' ' + str(sec_end) + ' _Enter')
    img_des = img_fol + sec_pfx + str(i) + '.png'
    rs.CurrentView('Front')
    rs.HideObjects(obj_all)
    rs.UnselectAllObjects()
    rs.Command('-_ViewCaptureToFile ' + img_des + ' _DrawGrid=No' + ' _Width=' + str(img_wid) + ' _Height=' + str(img_hei) + ' _Scale=' + str(img_sca) + ' _TransparentBackground=No' + ' _Enter' + ' _Enter')
    #rs.AddPoint(sec_str)
    #rs.AddPoint(sec_end)
    pla_pos[1] = pla_pos[1] - vis_ste

    rs.ShowObjects(obj_all)
    rs.DeleteObjects(pla_obj)
    sec_cur = rs.ObjectsByType(4)
    rs.DeleteObjects(sec_cur)

rs.CurrentLayer(layer='Default')

print ('\n Section views ready! \n')
