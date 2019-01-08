import rhinoscriptsyntax as rs

count = 0
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

#Create a clipping plane


#rs.ObjectLayer(rs.AllObjects(select=True),layer='cli_lay)

#Ask for the resolution of the section view animation
vis_res = rs.GetInteger(message='Please insert the resolution for the animation (number of slices)',number=10,minimum=2,maximum=100)

# #Calculate the step value to move the plane
pla_org = crd_o
vis_ste = obj_dep/vis_res
pla_pos = pla_org

for i in range(vis_res):
    pla_obj = rs.AddClippingPlane(rs.WorldZXPlane(),50,50,views='Perspective')
    rs.MoveObject(pla_obj,pla_pos)
    rs.AddPoint(pla_pos)
    pla_pos[1] = pla_pos[1] + vis_ste
    rs.DeleteObject(pla_obj)
