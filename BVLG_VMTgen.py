import bpy
import re
import os
import math

FMT = ".2f"

basetexture = "$basetexture [texture]"
bumpmap = "$bumpmap [texture]"
color2 = "$color2 [RGB field]"

envmap = "$envmap [boolean]"
envmaptint = "$envmaptint [RGB field]"
envmapfresnel = "$envmapfresnel [value]"

phong = "$phong [bool]"
phongboost = "$phongboost [value]"
phongexponent = "$phongexponent [value]"
phongfresnelranges = "$phongfresnelranges [value field]"
phongtint = "$phongtint [RGB field]"
rimlight = "$rimlight [bool]"
rimlightboost = "$rimlightboost [value]"

selfillum = "$selfillum [bool]"

class VLG_VMT :
    def __init__(self) :
        self.basetexture = None
        self.bumpmap = None
        self.color2 = None
        
        self.envmap = None
        self.envmaptint = None
        self.envmapfresnel = None

        self.phong = None
        self.phongboost = None
        self.phongexponent = None
        self.phongfresnelranges = None
        self.phongtint = None
        self.rimlight = None
        self.rimlightboost = None
        
        self.selfillum = None
    
    def find(mat, auto = 0) :
        if not(mat.use_nodes) :
            print(mat.name + " SKIPPED : Not Nodes")
            return None
        nodes = mat.node_tree.nodes
        material_output = None
        for node in nodes:
            if (node.type == "OUTPUT_MATERIAL") and (node.is_active_output):
                material_output = node
                break
        node = material_output
        while (node) and ((node.__class__.__name__ != "ShaderNodeGroup") or (node.node_tree.name != "VertexLitGeneric")) :
            print (node)
            node = node_CrawlUp(node)
        if not (node) :
            if (auto) :
                print(mat.name + " SKIPPED : No BVLG found in NodeTree")
            else:
                print("ERROR : No BVLG found in NodeTree")
            return None
        return node
    
    def load(self, BVLG, cdmaterials = "") :  
        self.basetexture = node_GetImg(node_CrawlUp(BVLG, basetexture))
        if (self.basetexture) :
            self.basetexture = '    $basetexture "' + cdmaterials + self.basetexture + '"'
        self.color2 = node_GetField(BVLG.inputs[color2])
        if (self.color2) :
            self.color2 = '    $color2 ' + self.color2
        
        self.envmap = node_GetField(BVLG.inputs[envmap])
        if (self.envmap != 0) :
            self.envmap = '    $envmap env_cubemap'
            self.envmaptint = node_GetField(BVLG.inputs[envmaptint])
            if (self.envmaptint) :
                self.envmaptint = '    $envmaptint ' + self.envmaptint
            self.envmapfresnel = node_GetField(BVLG.inputs[envmapfresnel])
            if (self.envmapfresnel) :
                self.envmapfresnel = '    $envmapfresnel ' + format(self.envmapfresnel, FMT)

        self.phong = node_GetField(BVLG.inputs[phong])
        if (self.phong != 0) :
            self.phong = '    $phong 1'
            self.phongboost = node_GetField(BVLG.inputs[phongboost])
            self.phongboost = '    $phongboost ' + format(self.phongboost,  FMT)
            self.phongexponent = node_CrawlUp(BVLG, phongexponent)
            if (self.phongexponent) and (self.phongexponent.__class__.__name__ == "ShaderNodeGroup") and (self.phongexponent.node_tree.name == "$phongexponenttexture splitter") :
                self.phongexponent = '    $phongexponenttexture "' + cdmaterials + str(node_GetImg(node_CrawlUp(self.phongexponent, 0))) + '"'
                self.phongtint = node_CrawlUp(BVLG, phongtint)
                if (self.phongtint) and (self.phongtint.__class__.__name__ == "ShaderNodeGroup") and (self.phongtint.node_tree.name == "$phongalbedotint") :
                    self.phongtint = '    $phongalbedotint 1'
            else :
                self.phongexponent = node_GetField(BVLG.inputs[phongexponent])
                self.phongexponent = '    $phongexponent ' + format(self.phongexponent, FMT)
            self.phongfresnelranges = node_GetField(BVLG.inputs[phongfresnelranges])
            if (self.phongfresnelranges) :
                self.phongfresnelranges = '    $phongfresnelranges ' + self.phongfresnelranges
            if not(self.phongtint) :
                self.phongtint = node_GetField(BVLG.inputs[phongtint])
                if (self.phongtint) :
                    self.phongtint = '    $phongtint ' + self.phongtint
            self.rimlight = node_GetField(BVLG.inputs[rimlight])
            if (self.rimlight != 0) :
                self.rimlight = '    $rimlight 1'
                self.rimlightboost = node_GetField(BVLG.inputs[rimlightboost])
                self.rimlightboost = '    $rimlightboost ' + format(self.rimlightboost, FMT)
            
            self.selfillum = node_GetField(BVLG.inputs[selfillum])
            if (self.selfillum != 0) :
                self.selfillum = '    $selfillum 1'

        self.bumpmap = node_GetImg(node_CrawlUp(BVLG, bumpmap))
        if (self.bumpmap) :
            self.bumpmap = '    $bumpmap "'+ cdmaterials + self.bumpmap + '"'
        elif (self.phong) :
            self.bumpmap = '    $bumpmap "dev/bump_normal"'

    def write(self, file) :
        file.write("VertexLitGeneric\n{\n")
        if self.basetexture :
            file.write(self.basetexture + "\n")
        if self.color2 :
            file.write(self.color2 + "\n")
        if self.bumpmap :
            file.write(self.bumpmap + "\n")
        file.write("\n")
        
        if self.envmap :
            file.write(self.envmap + "\n")
            file.write(self.envmaptint + "\n")
            if self.envmapfresnel :
                file.write(self.envmapfresnel + "\n")
            file.write("\n")

        if self.phong :
            file.write(self.phong + "\n")
            file.write(self.phongboost + "\n")
            file.write(self.phongexponent + "\n")
            file.write(self.phongfresnelranges + "\n")
            if self.phongtint :
                file.write(self.phongtint + "\n")
            if (self.rimlight) :
                file.write(self.rimlight + "\n")
                file.write(self.rimlightboost + "\n")
            file.write("\n")
                
        if self.selfillum :
            file.write(self.selfillum + "\n")
        file.write("}")
        

def node_GetImg(node) :
    if not(node) or (node.__class__.__name__ != "ShaderNodeTexImage") :
        return None
    if not(node.image) :
        return None
    name = re.sub('\....$', '', node.image.name)
    return name

def node_GetField(socket) :
    if (socket.__class__.__name__ == "NodeSocketColor") :
        if (socket.default_value[0] == 1 and socket.default_value[1] == 1 and socket.default_value[2] == 1) :
            return None
        return ('"[ ' + format(socket.default_value[0], FMT) + " " + format(socket.default_value[1], FMT) + " " + format(socket.default_value[2], FMT) + ' ]"')
    elif (socket.__class__.__name__ == "NodeSocketVector") :
        return ('"[ ' + format(socket.default_value[0], FMT) + " " + format(socket.default_value[1], FMT) + " " + format(socket.default_value[2], FMT) + ' ]"')
    elif (socket.__class__.__name__ == "NodeSocketFloat") :
        return socket.default_value
    return None

def node_CrawlUp(node_start, index = 0) :
    socket = node_start.inputs[index]
    type = socket.type
    if not(socket.is_linked) :
        return None
    link = socket.links[0]
    socket = link.from_socket
    if (type != socket.type) : #consider mismatched routes as invalid
        return None
    if (socket.node.__class__.__name__ == "NodeReroute") : #recursively crawl up reroutes
        return (node_CrawlUp(socket.node, 0))
    return socket.node

def VMTgen(mat, cdmaterials, folder = "export", mode = "name") :
    if (mode == "name") :
        mat = bpy.data.materials[mat]
    elif (mode != "data") :
        print ("ERROR invalid arguments")
        return
    if (cdmaterials[-1] != '/') :
        cdmaterials += '/'
    node = VLG_VMT.find(mat, mode == "data")
    if (node) :
        
        BVLG = node
        print(node)
        VMT = VLG_VMT()
        VMT.load(BVLG, cdmaterials)
        
        path = os.path.join(bpy.path.abspath("//"), folder) 
        if not(os.path.exists(path)) :
            os.makedirs(path)
        path += "/" + mat.name + ".vmt"
        print(path)
        print(mat.name + ".vmt")
        
        file = open(path, "a+")
        file.truncate(0)
        
        VMT.write(file)
        file.seek(0)
        print("\ngenerated output:")
        print(file.read())
        file.close

def AutoVMTgen(cdmaterials, folder = "export") :
    for mat in bpy.data.materials :
        VMTgen(mat, cdmaterials, folder, "data")
    
if __name__ == "__main__" :
    #print("\n\nnew run:\n")
    AutoVMTgen("cdmaterials")
