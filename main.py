import tkinter as tk
import rendermath as rm
import time
from typing import List

mw = tk.Tk()


def generate_window():

    mw.geometry("500x500")
    mw.resizable(0, 0)

    back = tk.Canvas(master=mw, bg='black',
                     borderwidth=0, highlightthickness=0)
    back.pack_propagate(0)
    back.pack(fill=tk.BOTH, expand=1)
    return back


class CubeRender(object):

    def render_cube(self):
        print('renderring')
        print(rm.RenderMath.projection_matrix())
        
        print(rm.RenderMath.box_mesh().vector[0].p1.x)
        time.sleep(1)


def main_loop():
    cr = CubeRender()
    while True:
        cr.render_cube()
        mw.update_idletasks()
        mw.update()


def main():
    print("python main function")
    canvas = generate_window()
    print(canvas)
    main_loop()


if __name__ == '__main__':
    main()
