# BlenderVertexLitGeneric
hereon as BVLG
Simplify asset creation for the Source engine through blender with these node networks and node groups

Nodegroups that take in textures and values outputing rendered graphics as close as possible to source engine's VertexLitGeneric shader

## Install
there are two ways of implementing this into your project file, I reccomend the first but the second might be required if you need to add it to an existing project
### Saving as startup file
1. open the .blend librairy file (current name is "sycreation's default")
2. navigate to File->Defaults->Save Startup File
this will let you directly use the shader by default on every new blender file you start.
you can also edit the default scene to your liking and save that as startup, the key elements are those in the next section
### Appending necessary elements
1. open your blender file
2. navigate to file->append and select the BVLG librairy file (current name is "sycreation's default")
3. select all the files in the NodeTree folder
4. repeat step 2 and select the element in the World folder
you're almost done, but $phong will not render properly without the next steps
5. in the World tab of the proprieties panel, set the world to be Source Engine World
6. in the 3D view, select material preview as shading and in the shading dropdown top right check "scene lights" and "scene world"

## Using the shader
in a newly created material you can add the main VertexLitGeneric node group and connect it to a material output

Primary inputs are flagged with the format they expect in the source engine, texture, value, RGB field, boolean etc.
several extensions allow more features that are not as common or simple as the main few: base color and color2, bumpmap, envmap and phong
these extentions include for now $phongalbedotint, $phongexponenttexture and $alphatest.
They can be added before or after the main node by following socket names: sockets that share the same name must be connected.


certain effects like $nocull are lower level than the shader nodes and are set in blender or the material's setting

$allowalphatocoverage requires the material's "Blend Mode" setting to be set to alpha hashed for accurate result, tho low sample counts will yield pixelated mess

## Notes
BVLG works with cycles but will yield more realistic results with ray traced reflections instead of phong, all other effects will not be affected.

a lot of the effects still need ajusting, their intensity may not be linear and my version may not be matching how it actually looks in engine, however because of limitations in HLMV and the slowness of repeated testing in game I have yet to have reliable side by side compairaison to refine curves and multipliers
### Future plans
I'd like to see this made into an addon and maybe even implemented into blender source tools
The final goal would be to make this into an exporter that would automatically generate the vmt based on the node setup
