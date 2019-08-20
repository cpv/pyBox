import tkinter as tk
import rendermath as rm
import time
from typing import List
from math import cos, tan, sin
from copy import copy, deepcopy

mw = tk.Tk()
matrixMath = rm.RenderMath().matrix


def generate_window():

    mw.geometry(str(int(rm.RenderMath.fScreenWidth)) +
                "x" + str(int(rm.RenderMath.fScreenHeight)))
    # mw.resizable(0, 0)

    back = tk.Canvas(master=mw, bg='black',
                     borderwidth=0, highlightthickness=0)
    back.pack_propagate(0)
    back.pack(fill=tk.BOTH, expand=1)
    return back


class CubeRender(object):

    def __init__(self, canvas):
        self.canvas = canvas
        w, h = 4, 4
        self.matRotx = [[0 for x in range(w)] for y in range(h)]
        self.matRotz = [[0 for x in range(w)] for y in range(h)]

        self.start_time = time.time()

    def render_cube(self):
        print('renderring')
        self.canvas.delete("all")

        elapsed_time = time.time() - self.start_time
        self.matRotz[0][0] = cos(elapsed_time)
        self.matRotz[0][1] = sin(elapsed_time)
        self.matRotz[1][0] = -sin(elapsed_time)
        self.matRotz[1][1] = cos(elapsed_time)
        self.matRotz[2][2] = 1
        self.matRotz[3][3] = 1

        self.matRotx[0][0] = 1
        self.matRotx[1][1] = cos(elapsed_time*0.5)
        self.matRotx[1][2] = sin(elapsed_time*0.5)
        self.matRotx[2][1] = -sin(elapsed_time*0.5)
        self.matRotx[2][2] = cos(elapsed_time*0.5)
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

            translatedTri.p1.z = t.p1.z + 4.0
            translatedTri.p2.z = t.p2.z + 4.0
            translatedTri.p3.z = t.p3.z + 4.0

            projectedTri = rm.Tri()
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
                projectedTri.p2.x, projectedTri.p2.y,  fill="#fb0")
            self.canvas.create_line(
                projectedTri.p2.x, projectedTri.p2.y,
                projectedTri.p3.x, projectedTri.p3.y, fill="#fb0")
            self.canvas.create_line(
                projectedTri.p3.x, projectedTri.p3.y,
                projectedTri.p1.x, projectedTri.p1.y, fill="#fb0")

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
