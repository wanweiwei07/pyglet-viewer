import numpy as np
import pyglet.math as pm
from pyglet_vis import decorators as decorators
from pyglet_vis import robot_math as rm


class Camera:

    def __init__(self,
                 pos=(2, 2, 2),
                 look_at=(0, 0, 0),
                 up=(0, 0, 1),
                 fov=60,
                 aspect=1.7778,
                 near=0.01,
                 far=1000.0):
        self._pos = np.asarray(pos, dtype=np.float32)
        self._look_at = np.asarray(look_at, dtype=np.float32)
        self._up = np.asarray(up, dtype=np.float32)
        self._fov = fov
        self._near = near
        self._far = far
        self._view_mat = None
        self._proj_mat = None
        self._aspect = aspect  # default 16:9
        self._view_dirty = True
        self._proj_dirty = True

    def set_to(self, pos, look_at, up=None):
        self._pos = np.asarray(pos, dtype=np.float32)
        self._look_at = np.asarray(look_at, dtype=np.float32)
        if up is not None:
            self._up = np.asarray(up, dtype=np.float32)
        self._mark_view_dirty()

    def rotate_around_lookat(self, dt=None, axis=(0, 0, 1), angle_rad=rm.np.pi / 360):
        direction = self._pos - self._look_at
        rotmat = rm.rotmat_from_axangle(axis, angle_rad)
        direction_rotated = rotmat @ direction
        self._pos = self._look_at + direction_rotated
        self._mark_view_dirty()

    def update_view(self):
        if not self._view_dirty:
            return
        self._view_mat = np.array(pm.Mat4.look_at(position=pm.Vec3(*self._pos),
                                                  target=pm.Vec3(*self._look_at),
                                                  up=pm.Vec3(*self._up)), dtype=np.float32).reshape(4, 4).T
        self._view_dirty = False

    def update_proj(self, width=None, height=None):
        if width is not None and height is not None:
            self._aspect = width / height
        self._proj_mat = np.array(pm.Mat4.perspective_projection(aspect=self._aspect,
                                                                 z_near=self._near,
                                                                 z_far=self._far,
                                                                 fov=self._fov)).reshape(4, 4).T
        self._proj_dirty = False

    # getters and setters
    @property
    def pos(self):
        return self._pos

    @pos.setter
    @decorators.mark_dirty('_mark_view_dirty')
    def pos(self, pos):
        self._pos = np.asarray(pos, dtype=np.float32)

    @property
    def look_at(self):
        return self._look_at

    @look_at.setter
    @decorators.mark_dirty('_mark_view_dirty')
    def look_at(self, look_at):
        self._look_at = np.asarray(look_at, dtype=np.float32)

    @property
    def up(self):
        return self._up

    @up.setter
    @decorators.mark_dirty('_mark_view_dirty')
    def up(self, up):
        self._up = np.asarray(up, dtype=np.float32)

    @property
    def fov(self):
        return self._fov

    @fov.setter
    @decorators.mark_dirty('_mark_proj_dirty')
    def fov(self, fov):
        self._fov = fov

    @property
    def near(self):
        return self._near

    @near.setter
    @decorators.mark_dirty('_mark_proj_dirty')
    def near(self, near):
        self._near = near

    @property
    def far(self):
        return self._far

    @far.setter
    @decorators.mark_dirty('_mark_proj_dirty')
    def far(self, far):
        self._far = far

    # getters for matrices, setting matrices should be done via other methods
    @property
    @decorators.lazy_update('_view_dirty', 'update_view')
    def view_mat(self):
        return self._view_mat

    @property
    @decorators.lazy_update('_proj_dirty', 'update_proj')
    def proj_mat(self):
        return self._proj_mat

    @property
    def vp_mat(self):
        return self.proj_mat @ self.view_mat

    def _mark_view_dirty(self):
        self._view_dirty = True

    def _mark_proj_dirty(self):
        self._proj_dirty = True
