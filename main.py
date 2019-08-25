import tkinter as tk
import rendermath as rm
import time
from typing import List
from math import cos, tan, sin
from copy import copy, deepcopy

# ================= Note to the Reader =============================
#
# First and formost...  Hi there! I dont know what you would
# be doing reading this. Just wanted to clarify a few things if you are...
# 1. Dont look into this for any form of accurate maths or logic
# 2. Dont look into this for any good python practices.
#             (I have no experience in python whatsoever)
# 3. Ignore my overuse of globals/dodgy messaging patterns/..
#       bad class structure/bad practices/code dupes/other misc badboys
# 4. This is purely just a test for me to see what limits I can push
#       with python + tkinter.
#
#
# UPDATE:
# My laptop started getting really hot so I think im gonna switch out 
# and try something else to make this in. Preferably not tkinter ;)
#
#
# ==================================================================

mw = tk.Tk()
global mathInstance
global matrixMath
global back  # canvas


# Settings Toggles. (Should encapsulate in its own settings manager class.)
# -- -- -- -- -- -- -- -- -- -- -- --
wireframe_enable = True
planar_enable = True
# -- -- -- -- -- -- -- -- -- -- -- --


def save_size(event):
    global mathInstance
    global matrixMath
    global back

    with open("pythonRender.conf", "w") as conf:
        conf.write(mw.geometry())
    # need to figure out how python handles broadcasting messages/notifications to update.
    mathInstance.updateRenderSize(mathInstance, back)
    matrixMath = mathInstance.matrix


def generate_window():
    global mathInstance
    global matrixMath
    global back  # canvas

    with open("pythonRender.conf", "r") as conf:
        geom = conf.read()
        if geom:
            mw.geometry(geom)
        else:
            mw.geometry("500x500")
    # mw.resizable(0, 0)

    back = tk.Canvas(master=mw, bg='black',
                     borderwidth=0, highlightthickness=0)
    back.pack_propagate(0)
    back.pack(fill=tk.BOTH, expand=1)

    # so that the screen size gets set for our matrix setup.
    mw.update_idletasks()
    mw.update()

    mathInstance = rm.RenderMath(back)
    matrixMath = mathInstance.matrix

    mw.bind("<Configure>", save_size)

    return back


class CubeRender(object):

    def __init__(self, canvas):
        self.canvas = canvas
        w, h = 4, 4
        self.matRotx = [[0 for x in range(w)] for y in range(h)]
        self.matRotz = [[0 for x in range(w)] for y in range(h)]

        self.start_time = time.time()

    def multiplyByMatrix(self, ti, to, m):
        rm.RenderMath.multiplyMatrixVector(
            ti.p1, to.p1, m)
        rm.RenderMath.multiplyMatrixVector(
            ti.p2, to.p2, m)
        rm.RenderMath.multiplyMatrixVector(
            ti.p3, to.p3, m)

    # where object is a matrix that represents a set of points to make a mesh.
    def apply_rotational_geometry(self, vertex):
        gridZRotate = deepcopy(vertex)
        self.multiplyByMatrix(vertex, gridZRotate, self.matRotz)
        gridZXRotate = deepcopy(gridZRotate)
        self.multiplyByMatrix(gridZRotate, gridZXRotate, self.matRotx)
        self.project_to_dimensions(gridZXRotate)
        return gridZXRotate

    def project_to_dimensions(self, tri):
        tri.p1.x += 1.0
        tri.p1.y += 1.0

        tri.p2.x += 1.0
        tri.p2.y += 1.0

        tri.p3.x += 1.0
        tri.p3.y += 1.0

        tri.p1.x *= 0.5 * mathInstance.fScreenWidth
        tri.p1.y *= 0.5 * mathInstance.fScreenHeight
        tri.p2.x *= 0.5 * mathInstance.fScreenWidth
        tri.p2.y *= 0.5 * mathInstance.fScreenHeight
        tri.p3.x *= 0.5 * mathInstance.fScreenWidth
        tri.p3.y *= 0.5 * mathInstance.fScreenHeight

    def render_cube(self):

        global planar_enable

        self.canvas.delete("all")

        x = mw.winfo_pointerx()
        y = mw.winfo_pointery()
        abs_coord_x = mw.winfo_pointerx() - mw.winfo_vrootx()
        abs_coord_y = mw.winfo_pointery() - mw.winfo_vrooty()

        abs_coord_x = abs_coord_x/100
        abs_coord_y = abs_coord_y/100
        # for rendering rotation with mousepos.
        self.matRotz[0][0] = cos(abs_coord_x)
        self.matRotz[0][1] = sin(abs_coord_x)
        self.matRotz[1][0] = -sin(abs_coord_x)
        self.matRotz[1][1] = cos(abs_coord_x)
        self.matRotz[2][2] = 1
        self.matRotz[3][3] = 1

        self.matRotx[0][0] = 1
        self.matRotx[1][1] = cos(abs_coord_y)
        self.matRotx[1][2] = sin(abs_coord_y)
        self.matRotx[2][1] = -sin(abs_coord_y)
        self.matRotx[2][2] = cos(abs_coord_y)
        self.matRotx[3][3] = 1

        for t in rm.RenderMath.box_mesh().vector:
            # todo: express this better.
            # todo: translation helper functions.
            rotatedZTri = deepcopy(t)
            self.multiplyByMatrix(t, rotatedZTri, self.matRotz)
            rotatedZXTri = deepcopy(rotatedZTri)
            self.multiplyByMatrix(rotatedZTri, rotatedZXTri, self.matRotx)
            translatedTri = deepcopy(rotatedZXTri)

            translatedTri.p1.z = rotatedZXTri.p1.z + 3.0
            translatedTri.p2.z = rotatedZXTri.p2.z + 3.0
            translatedTri.p3.z = rotatedZXTri.p3.z + 3.0

            projectedTri = deepcopy(translatedTri)
            self.multiplyByMatrix(translatedTri, projectedTri, matrixMath)

            self.project_to_dimensions(projectedTri)
            global planar_enable

            if planar_enable:
                # generate plane on d,0,d
                # planar_enable = False

                for x in range(-10,10,1):
                    x /= 2
                    #todo: figure out grid math.
                    gridTriVert = rm.Tri(rm.Vec3D(0, x, -2), rm.Vec3D(0, x, 2))
                    gridTriHori = rm.Tri(rm.Vec3D(0, -2, x), rm.Vec3D(0, 2, x))
                    gridTriVert = self.apply_rotational_geometry(
                        vertex=gridTriVert)
                    gridTriHori = self.apply_rotational_geometry(
                        vertex=gridTriHori)
                    self.canvas.create_line(
                        gridTriVert.p1.x, gridTriVert.p1.y,
                        gridTriVert.p2.x, gridTriVert.p2.y,  fill="#1d1d1d")
                    self.canvas.create_line(
                        gridTriHori.p1.x, gridTriHori.p1.y,
                        gridTriHori.p2.x, gridTriHori.p2.y,  fill="#1d1d1d")

            global wireframe_enable

            if(wireframe_enable):
                self.canvas.create_line(
                    projectedTri.p1.x, projectedTri.p1.y,
                    projectedTri.p2.x, projectedTri.p2.y,  fill=projectedTri.colour)
                self.canvas.create_line(
                    projectedTri.p2.x, projectedTri.p2.y,
                    projectedTri.p3.x, projectedTri.p3.y, fill=projectedTri.colour)
                self.canvas.create_line(
                    projectedTri.p3.x, projectedTri.p3.y,
                    projectedTri.p1.x, projectedTri.p1.y, fill=projectedTri.colour)
            else:
                self.canvas.create_polygon((projectedTri.p1.x, projectedTri.p1.y, projectedTri.p2.x,
                                            projectedTri.p2.y, projectedTri.p3.x, projectedTri.p3.y), fill=projectedTri.colour)


def main_loop(cr):
    while True:
        cr.render_cube()
        mw.update_idletasks()
        mw.update()
        # time.sleep(1./25)


# make a generic settings toggle for things like this.
# -- -- -- -- -- -- --
def wireframe_toggle(self):
    global wireframe_enable
    wireframe_enable = not wireframe_enable


def planar_toggle(self):
    global planar_enable
    planar_enable = not planar_enable
# -- -- -- -- -- -- --


def setup_keybinds():

    mw.bind('<w>', wireframe_toggle)
    mw.bind('<p>', planar_toggle)


def main():

    canvas = generate_window()
    cr = CubeRender(canvas)
    setup_keybinds()
    main_loop(cr)


if __name__ == '__main__':
    main()
