import tkinter as tk
import rendermath as rm
import time
from typing import List

mw = tk.Tk()
matrixMath = rm.RenderMath().matrix


def generate_window():

    mw.geometry(str(rm.RenderMath.fScreenWidth) +
                "x" + str(rm.RenderMath.fScreenHeight))
    mw.resizable(0, 0)

    back = tk.Canvas(master=mw, bg='black',
                     borderwidth=0, highlightthickness=0)
    back.pack_propagate(0)
    back.pack(fill=tk.BOTH, expand=1)
    return back


class CubeRender(object):

    def __init__(self, canvas):
        self.canvas = canvas

    def render_cube(self):
        print('renderring')

        for t in rm.RenderMath.box_mesh().vector:
            projectedTri = rm.Tri()
            rm.RenderMath.multiplyMatrixVector(
                t.p1, projectedTri.p1, matrixMath)
            rm.RenderMath.multiplyMatrixVector(
                t.p2, projectedTri.p2, matrixMath)
            rm.RenderMath.multiplyMatrixVector(
                t.p3, projectedTri.p3, matrixMath)

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

            print(projectedTri)

            self.canvas.create_line(projectedTri.p1.x, projectedTri.p1.y,
                                    projectedTri.p2.x, projectedTri.p2.y,
                                    projectedTri.p3.x, projectedTri.p3.y, fill="#fb0")

        time.sleep(1)


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
