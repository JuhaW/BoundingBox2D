import bpy
import bmesh
from mathutils import Matrix, Vector

def makemesh(coord1,coord2,coord3,coord4):

	Verts = [coord1, coord2, coord3, coord4]
	Edges = [[0,2],[2,3],[3,1],[1,0]]
	Faces = [[0,1,3,2]]
	profile_mesh = bpy.data.meshes.new("2D Bounding box")
	profile_mesh.from_pydata(Verts, [], Faces)
	profile_mesh.update()

	profile_object = bpy.data.objects.new("2D Bounding box", profile_mesh)
	profile_object.data = profile_mesh  # this line is redundant .. it simply overwrites .data

	scene = bpy.context.scene
	scene.objects.link(profile_object)
	bpy.ops.object.select_all(action="DESELECT")
	profile_object.select = True
	bpy.context.scene.objects.active = profile_object
##########################################################
lsw_minx = lnw_minx = lsw_miny = lse_miny = minz = 9999999
lse_maxx = lne_maxx = lnw_maxy = lne_maxy = -9999999

#get empties with dupligroup
empties =(ob for ob in bpy.context.selected_objects if ob.type == 'EMPTY' and ob.dupli_type == 'GROUP')
objects=[]
group_names=[]
hoplaa ={}
c = 0

group_objects=[]
for ob in empties:
	objects.append(ob)
	hoplaa[0,c] = ob
	c += 1
print (hoplaa)
print ()
print ("Len hoplaa",len(hoplaa))
print ("halipusu2")

#get objects of dupligroup
if len(objects) >0:
	group_objects=[]
	for ob in objects:
		a = ob.dupli_group.name
		b = bpy.data.groups[a].objects
		#add emptys groupname to the list
		group_names.append(a)
		print ("Empty ",ob.name," location:",ob.location)
		for ob in b:
			group_objects.append(ob)

	for e in group_names:
		print ("Group names:",group_names)
	print ("Group objects:",group_objects)

obj = group_objects + bpy.context.selected_objects
print ("OBJECTS:",obj)
objects =(ob for ob in obj if ob.type == 'MESH' or ob.type == 'CURVE')

#for ob in bpy.context.selected_objects if ob.type != 'EMPTY':
print ("objects:",objects)


for ob in objects:

	mat = ob.matrix_world
	#lsw = mat * Vector(ob.bound_box[0])
	#print ("1.lsw",lsw)

	#ob1 = ob.copy()
	#ob1.data = ob.data.copy()
	#ob1.data.transform(mat)
	#ob1.matrix_world = Matrix()
	#mat = ob1.matrix_world
	#ob = ob1
	print (ob)
	#L = low, H = high,n = north, e = east,s = south, w = west
	#Lsw,Hsw,Hnw,Lnw
	#Lse,Hse,Hne,Lne

	lsw = mat * Vector(ob.bound_box[0])
	lnw = mat * Vector(ob.bound_box[3])
	lse = mat * Vector(ob.bound_box[4])
	lne = mat * Vector(ob.bound_box[7])
	#print ("lsw",lsw)
	#print ("lne",lne)

	lsw_minx = min(lsw[0],lsw_minx)
	lnw_minx = min(lnw[0],lnw_minx)
	lse_maxx = max(lse[0],lse_maxx)
	lne_maxx = max(lne[0],lne_maxx)

	lsw_miny = min(lsw[1],lsw_miny)
	lnw_maxy = max(lnw[1],lnw_maxy)
	lse_miny = min(lse[1],lse_miny)
	lne_maxy = max(lne[1],lne_maxy)

	#lowest point to set 2d bounding plane
	minz = min(lsw[2],lnw[2],lse[2],lne[2],minz)

makemesh(Vector([lsw_minx,lsw_miny,0]),
		 Vector([lse_maxx,lse_miny,0]),
		 Vector([lnw_minx,lnw_maxy,0]),
		 Vector([lne_maxx,lne_maxy,0]))

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
#bpy.context.space_data.cursor_location[2] = minz
bpy.context.object.location[2] = minz
bpy.ops.view3d.snap_cursor_to_selected()
