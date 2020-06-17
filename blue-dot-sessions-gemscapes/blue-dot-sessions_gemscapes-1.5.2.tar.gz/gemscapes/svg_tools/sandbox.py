import sys
import itertools
import xml.etree.ElementTree as ET


import pyclipper

from . import polygon_iter, _vertices_from_points_str, straight_paths2svg, get_root

def get_clip(width, height):
    clip = [[0, 0], [0, width], [width, height], [0, height]]
    clip_scaled = pyclipper.scale_to_clipper(clip)
    return clip, clip_scaled


def union_factory(width, height):
    """
    Not sure why this works
    """
    pc = pyclipper.Pyclipper()
    clip, clip_scaled = get_clip(width, height)
    def union(*vertices):
        total_union = vertices[0]
        for idx in range(1, len(vertices)):
            # pc.AddPath(vertices[idx], pyclipper.PT_CLIP, True)
            # pc.AddPath(total_union, pyclipper.PT_SUBJECT, True)
            pc.AddPath(total_union, pyclipper.PT_CLIP, True)
            pc.AddPath(vertices[idx], pyclipper.PT_SUBJECT, True)

            res = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            # print(f"union: len(res)={len(res)}")
            total_union = res[0]
            # total_union = union(vertices_scaled[idx], total_union)
        pc.Clear()
        # pc.AddPath(clip_scaled, pyclipper.PT_CLIP, True)
        # pc.AddPaths(vertices, pyclipper.PT_SUBJECT, True)
        # exec_result = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

        # solution = vertices[0]
        # for idx in range(1, 2):
            # print(f"union: len(solution)={len(solution)}")
        #     print(f"union: type(solution[0][0])={type(solution[0][0])}")
        #     pc.AddPath(solution, pyclipper.PT_SUBJECT, True)
        #     pc.AddPath(vertices[idx], pyclipper.PT_SUBJECT, True)
        #     solution = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_POSITIVE, pyclipper.PFT_POSITIVE)
        #     pc.Clear()
        # print(solution)
        # solution = []
        # for res in exec_result:
        #     solution.extend(res)

        return total_union
    return union


def intersection_factory(width, height):
    pc = pyclipper.Pyclipper()
    clip, clip_scaled = get_clip(width, height)
    def intersection(vertices0, vertices1):
        # pc.AddPath(clip_scaled, pyclipper.PT_CLIP, True)
        # pc.AddPaths([vertices0, vertices1], pyclipper.PT_SUBJECT, True)
        # solution = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        # pc.Clear()
        # print(f"intersection: len(solution)={len(solution)}")
        # return solution
        pc.AddPath(vertices0, pyclipper.PT_CLIP, True)
        pc.AddPath(vertices1, pyclipper.PT_SUBJECT, True)
        solution = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        pc.Clear()
        print(f"intersection: len(solution)={len(solution)}")
        return solution
    return intersection

def difference_factory(width, height):
    pc = pyclipper.Pyclipper()
    clip, clip_scaled = get_clip(width, height)
    def difference(vertices0, vertices1):
        pc.AddPath(vertices0, pyclipper.PT_CLIP, True)
        pc.AddPath(vertices1, pyclipper.PT_SUBJECT, True)
        solution = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
        print(f"difference: len(solution)={len(solution)}")
        return solution
    return difference


def knock_out(file_path: str):
    vertices = []
    vertices_scaled = []
    dark_vertices = []
    dark_vertices_scaled = []


    with get_root(file_path) as root:
        width, height = float(root.attrib["width"]), float(root.attrib["height"])
        width /= 4
        height /= 4
        g = root.find("g")
        for polygon in itertools.chain(g.findall("path"), g.findall("polygon")):
            if polygon.tag == "path":
                g.remove(polygon._element)
                continue
            # if polygon.attrib["fill"] == "none":
            #     continue

            if polygon.attrib["fill"] == "none":
                if polygon.attrib["stroke"] == "green":
                    points_str = polygon.attrib["points"]
                    paths = _vertices_from_points_str(points_str)
                    dark_vertices.append(paths)
                    dark_vertices_scaled.append(pyclipper.scale_to_clipper(paths))
                continue

            points_str = polygon.attrib["points"]

            paths = _vertices_from_points_str(points_str)
            vertices.append(paths)
            vertices_scaled.append(pyclipper.scale_to_clipper(paths))
    print(f"knock_out: width={width}, height={height}")
    print(f"knock_out: len(dark_vertices_scaled)={len(dark_vertices_scaled)}")
    print(f"knock_out: len(vertices_scaled)={len(vertices_scaled)}")

    union = union_factory(width, height)
    total_union = union(*vertices_scaled)

    # diff = difference_factory(width, height)
    # diffs = []
    intersect = intersection_factory(width, height)
    intersections = []
    for idx in range(len(dark_vertices_scaled)):
        # diffs.append(
        #     diff(total_union, dark_vertices_scaled[idx])
        # )
        intersections.append(
            intersect(total_union, dark_vertices_scaled[idx])
        )

    print(f"knock_out: len(intersections)={len(intersections)}")
    # print(f"knock_out: len(diffs)={len(diffs)}")


    # solution_scaled = pyclipper.scale_from_clipper(solution)
    # solution_str = straight_paths2svg(solution_scaled)

    with get_root(file_path) as root:
        g = root.find("g")
        new_path = ET.Element("path")
        scaled = pyclipper.scale_from_clipper(total_union)
        scaled_str = straight_paths2svg(scaled)
        new_path.attrib["d"] = scaled_str
        new_path.attrib["fill"] = "#000000"
        new_path.attrib["stroke"] = "blue"
        new_path.attrib["stroke-width"] = "0.5"
        g._element.insert(0, new_path)

        for idx in range(len(intersections)):
            for intersect in intersections[idx]:
                new_path = ET.Element("path")
                print(f"knock_out: idx={idx}, len(intersect)={len(intersect)}")
                scaled = pyclipper.scale_from_clipper(intersect)
                print(f"knock_out: idx={idx}, scaled={scaled}")

                scaled_str = straight_paths2svg(scaled)
                new_path.attrib["d"] = scaled_str
                new_path.attrib["fill"] = "orange"
                g._element.append(new_path)
                # new_path.attrib["stroke"] = "orange"
                # new_path.attrib["stroke-width"] = "0.5"


def main():
    file_path = sys.argv[1]

    knock_out(file_path)


main()
