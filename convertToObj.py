#inbetween format structure:
# $objectname = [$coordsarray,$var1,$]

#vertex offsets are needed for merging

# objdefs->objdef->[mdlcode,vertdef,vo,vi,vg]
# the above definition might be totally wrong. read the code lol.

import sys

filename = (sys.argv[1])

objdefs = []

with open(str(filename),"r") as file:
	lines = file.readlines()
	l1 = 0
	vi = 0 #vertex index, needed for offsets
	vg = 0 #vertex group, needed for offsets
	mg = 0 #merge group, needed for offsets
	mdli = 0 #mdl index
	while l1 < len(lines):
		lines[l1] = lines[l1].replace(" ","")#replace all the spaces, makes formatting easier
		if(lines[l1].find('staticconstVtx')!=-1):
			#add in the last 12 - 5 chars to array of vtx/mdls, its the code
			codestart = (len(lines[l1])) - 13
			codeend = (len(lines[l1])) - 5
			mdlcode = (lines[l1][codestart:codeend])
			
			objdef = []#create an array 
			objdef.append(str(mdlcode)) #set first element to be mdlcode
			objdefs.append(objdef) #throw that into the main array
			#print(mdlcode) #in here as a debug
			l2 = l1 #level two index of lines
			vg = vg + 1
			vo = 0 #vertex offset, needed for offsets
			vertdefs = []
			objdefs[vg-1].append(vertdefs)
			while lines[l2].find('};') == -1:
				lines[l2] = lines[l2].replace(" ","")#has to be done due to extra iterations
				if lines[l2].find("{{{") !=-1:
					c = 3
					ci = 0 #character index
					chars = ',',",","}"
					vertdef = "" #whole vertex definition, add more params later
					while ci < len(chars):
						vertcoords = "" #just the coords of the verts
						while lines[l2][c] != chars[ci]:
							#runs char number of times to get first three nums
							vertcoords = vertcoords + lines[l2][c]
							c = c + 1
						#division by one hundred cause n64 objects are MASSIVE
						vertdef = vertdef + " " + (str(int(vertcoords)/100))
						c = c + 1
						ci = ci + 1
					vo = vo + 1
					vi = vi + 1
					# the correct offset to apply can be derived by this eq:
					# (applied offset) = (vertex index) - (vertex offset)
					# then add the applied offset to the merge index + 1
					#print(mdlcode+" v"+vertdef+" vo:"+str(vo)+" vi:"+str(vi)+" vg:"+str(vg))
					print("v"+vertdef)
					objdefs[vg-1][1].append(["v"+str(vertdef),vo,vi,vg,(vi-vo+1)])
				l2 = l2 + 1
		if(lines[l1].find('gsSPVertex')!=-1):
			l2 = l1
			mg = mg + 1
			# EG: gsSPVertex(bbh_seg7_vertex_07020500, 6, 0),
			#index the first comma then move backwords 8 places
			commaloc = lines[l2].index(",")
			codestart = commaloc - 8
			codeend = commaloc - 0
			mdlcode = (lines[l2][codestart:codeend])
			while lines[l2].find('};') == -1:
				lines[l2] = lines[l2].replace(" ","")#has to be done due to extra iterations
				if((lines[l2].find("gsSP2Triangles(")!=-1)or(lines[l2].find("gsSP1Triangles(")!=-1)):
					c = 15 #start at 15 to skip the gssp2 nonsense
					ci = 0 #character index
					if(lines[l2].find("gsSP2Triangles(")!=-1):
						chars = ",",",",",",",",",",",",",",')'
					if(lines[l2].find("gsSP1Triangles(")!=-1):
						chars = ",",",",",",')'
					
					mergedefs = []
					while ci < len(chars):
						mergedef = ""
						while lines[l2][c] != chars[ci]:
							mergedef = mergedef + lines[l2][c]
							c = c + 1
						mergedefs.append(mergedef)
						
						c = c + 1
						ci = ci + 1
					o = objdefs[mdli][1][0][4]
					#3 and 7 are flags we don't need right now
					print("f "+str(int(mergedefs[0])+o)+"// "+str(int(mergedefs[1])+o)+"// "+str(int(mergedefs[2])+o)+"//")
					print("f "+str(int(mergedefs[4])+o)+"// "+str(int(mergedefs[5])+o)+"// "+str(int(mergedefs[6])+o)+"//")
				l2 = l2 + 1
			mdli = mdli + 1
		l1 = l1 + 1

#print(objdefs)
#print(mergedefs)
lo1 = (len(objdefs))
i1 = 0
while i1 < lo1:
	lo2 = (len(objdefs[i1][1]))
	i2 = 0
	while i2 < lo2:
		offset = (objdefs[i1][1][i2][4])
		#print(offset)
		i2 = i2 + 1
	i1 = i1 + 1
