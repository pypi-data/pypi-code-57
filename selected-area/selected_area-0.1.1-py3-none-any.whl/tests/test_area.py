from selected_area import Segment, Point, SelectedArea


def test_segments():
    """
    https://postimg.cc/HcH38dt1
    """
    area = SelectedArea(Point(1, 2), Point(4, 4))               # diagonal AC

    segment1 = Segment(Point(2, 1.5), Point(4.5, 3.5))          # EF
    segment2 = Segment(Point(1, 1.5), Point(1, 4.5))            # GH
    segment3 = Segment(Point(3, 1), Point(4.5, 2.5))            # IJ
    segment4 = Segment(Point(4, 1), Point(5, 3))                # KL
    segment5 = Segment(Point(1.5, 1), Point(3.5, 4.5))          # MN
    segment6 = Segment(Point(1.73, 3.19), Point(2.5, 3.5))      # OP
    segment7 = Segment(Point(0.28, 2.93), Point(2.42, 3.82))    # QR
    segment8 = Segment(Point(2, 0.5), Point(5.5, 0.5))          # ST
    segment9 = Segment(Point(5.5, 2), Point(5.5, 4))            # UV
    segment10 = Segment(Point(2, 1), Point(5.63, 1.8))          # WZ

    assert area.contains(segment1)
    assert area.contains(segment2)
    assert area.contains(segment3)
    assert not area.contains(segment4)
    assert area.contains(segment5)
    assert area.contains(segment6)
    assert area.contains(segment7)
    assert not area.contains(segment8)
    assert not area.contains(segment9)
    assert not area.contains(segment10)
    assert repr(segment4) == 'Segment(p1=Point(x=4, y=1), p2=Point(x=5, y=3))'
