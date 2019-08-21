import tkinter as tk
import rendermath as rm
import time
from typing import List
from math import cos, tan, sin
from copy import copy, deepcopy

mw = tk.Tk()
matrixMath = rm.RenderMath().matrix


def save_size(event):
    with open("pythonRender.conf", "w") as conf:
        conf.write(mw.geometry())


def generate_window():

    with open("pythonRender.conf", "r") as conf:
        geom = conf.read()
        if geom:
            mw.geometry(geom)
        else:
            mw.geometry(str(int(rm.RenderMath.fScreenWidth)) +
                        "x" + str(int(rm.RenderMath.fScreenHeight)))
    # mw.resizable(0, 0)

    back = tk.Canvas(master=mw, bg='black',
                     borderwidth=0, highlightthickness=0)
    back.pack_propagate(0)
    back.pack(fill=tk.BOTH, expand=1)

    mw.bind("<Configure>", save_size)

    return back


class CubeRender(object):

    def __init__(self, canvas):
        self.canvas = canvas
        w, h = 4, 4
        self.matRotx = [[0 for x in range(w)] for y in range(h)]
        self.matRotz = [[0 for x in range(w)] for y in range(h)]

        self.start_time = time.time()

    def render_cube(self):
        self.canvas.delete("all")

        # #for rendering rotation with elapsed time.

        # elapsed_time = time.time() - self.start_time
        # elapsed_time /= 3

        # self.matRotz[0][0] = cos(elapsed_time)
        # self.matRotz[0][1] = sin(elapsed_time)
        # self.matRotz[1][0] = -sin(elapsed_time)
        # self.matRotz[1][1] = cos(elapsed_time)
        # self.matRotz[2][2] = 1
        # self.matRotz[3][3] = 1

        # self.matRotx[0][0] = 1
        # self.matRotx[1][1] = cos(elapsed_time*0.5)
        # self.matRotx[1][2] = sin(elapsed_time*0.5)
        # self.matRotx[2][1] = -sin(elapsed_time*0.5)
        # self.matRotx[2][2] = cos(elapsed_time*0.5)
        # self.matRotx[3][3] = 1

        x = mw.winfo_pointerx()
        y = mw.winfo_pointery()
        abs_coord_x = mw.winfo_pointerx() - mw.winfo_vrootx()
        abs_coord_y = mw.winfo_pointery() - mw.winfo_vrooty()

        abs_coord_x/=100
        abs_coord_y/=100
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

            rotatedZTri = deepcopy(t)

            rm.RenderMath.multiplyMatrixVector(
                t.p1, rotatedZTri.p1, self.matRotz)
            rm.RenderMath.multiplyMatrixVector(
                t.p2, rotatedZTri.p2, self.matRotz)
            rm.RenderMath.multiplyMatrixVector(
                t.p3, rotatedZTri.p3, self.matRotz)

            rotatedZXTri = deepcopy(rotatedZTri)

            rm.RenderMath.multiplyMatrixVector(
                rotatedZTri.p1, rotatedZXTri.p1, self.matRotx)
            rm.RenderMath.multiplyMatrixVector(
                rotatedZTri.p2, rotatedZXTri.p2, self.matRotx)
            rm.RenderMath.multiplyMatrixVector(
                rotatedZTri.p3, rotatedZXTri.p3, self.matRotx)

            translatedTri = deepcopy(rotatedZXTri)

            translatedTri.p1.z = rotatedZXTri.p1.z + 4.0
            translatedTri.p2.z = rotatedZXTri.p2.z + 4.0
            translatedTri.p3.z = rotatedZXTri.p3.z + 4.0

            projectedTri = deepcopy(translatedTri)

            rm.RenderMath.multiplyMatrixVector(
                translatedTri.p1, projectedTri.p1, matrixMath)
            rm.RenderMath.multiplyMatrixVector(
                translatedTri.p2, projectedTri.p2, matrixMath)
            rm.RenderMath.multiplyMatrixVector(
                translatedTri.p3, projectedTri.p3, matrixMath)

            projectedTri.p1.x += 1.0
            projectedTri.p1.y += 1.0

            projectedTri.p2.x += 1.0
            projectedTri.p2.y += 1.0

            projectedTri.p3.x += 1.0
            projectedTri.p3.y += 1.0

            projectedTri.p1.x *= 0.5 * rm.RenderMath.fScreenWidth
            projectedTri.p1.y *= 0.5 * rm.RenderMath.fScreenHeight
            projectedTri.p2.x *= 0.5 * rm.RenderMath.fScreenWidth
            projectedTri.p2.y *= 0.5 * rm.RenderMath.fScreenHeight
            projectedTri.p3.x *= 0.5 * rm.RenderMath.fScreenWidth
            projectedTri.p3.y *= 0.5 * rm.RenderMath.fScreenHeight

            self.canvas.create_line(
                projectedTri.p1.x, projectedTri.p1.y,
                projectedTri.p2.x, projectedTri.p2.y,  fill=projectedTri.colour)
            self.canvas.create_line(
                projectedTri.p2.x, projectedTri.p2.y,
                projectedTri.p3.x, projectedTri.p3.y, fill=projectedTri.colour)
            self.canvas.create_line(
                projectedTri.p3.x, projectedTri.p3.y,
                projectedTri.p1.x, projectedTri.p1.y, fill=projectedTri.colour)

        # time.sleep(0.1)


def main_loop(cr):
    while True:
        cr.render_cube()
        mw.update_idletasks()
        mw.update()


def main():

    canvas = generate_window()
    cr = CubeRender(canvas)

    print(canvas)
    main_loop(cr)


if __name__ == '__main__':
    main()
