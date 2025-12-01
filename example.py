import numpy as np
import trimesh as trm
import pyglet_vis.model as mdl
import pyglet_vis.geometry as geo
import pyglet_vis.scene as scn
import pyglet_vis.constant as const
import pyglet_vis.world as wd

mesh = trm.load_mesh("bunnysim.stl")
model = mdl.Model(geo.Geometry(verts=mesh.vertices,
                               faces=mesh.faces,
                               rgbs=const.pink))
scene = scn.Scene()
scene.add(model)
base = wd.World()
base.set_scene(scene)
base.run()
