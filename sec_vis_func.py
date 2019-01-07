import rhinoscriptsyntax as rs

def Mod_siz():
    '''Function to calculate the size of the model via bounding box'''

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

    return (obj_wid,obj_dep,obj_hei)
