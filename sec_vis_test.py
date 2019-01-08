import rhinoscriptsyntax as rs

obj_all = rs.AllObjects(select=True)
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
rs.Command('-_Top')

pnt_ste = (-20,10,0)

sec_str = crd_x
sec_end = rs.PointAdd(crd_x,pnt_ste)

print(sec_str)
print(sec_end)

rs.AddPoint(sec_str)
rs.AddPoint(sec_end)

rs.Command('-_Section ' + str(sec_str) + ' ' + str(sec_end) + ' _Enter')

rs.ObjectsByType(4)
