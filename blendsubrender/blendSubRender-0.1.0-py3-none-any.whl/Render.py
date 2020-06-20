import bpy
import sys


def render(start_frame, end_frame):
    """
    For this sub process, set the start and end frame then render
    """
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    bpy.ops.render.render(animation=True)


if __name__ == '__main__':
    start, end = sys.argv[len(sys.argv) - 1].split(" ")
    render(int(start), int(end))


