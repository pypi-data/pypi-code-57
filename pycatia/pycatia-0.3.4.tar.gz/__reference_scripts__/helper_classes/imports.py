import inflection


def create_imports(returns):

    # print(returns)

    imports = []


    # knowledge interfaces
    if 'Angle' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.angle import Angle')
    if 'BoolParam' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.bool_param import BoolParam')
    if 'Check' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.check import Check')
    if 'DesignTable' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.design_table import DesignTable')
    if 'Dimension' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.dimension import Dimension')
    if 'EnumParam' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.enum_param import EnumParam')
    if 'Formula' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.formula import Formula')
    if 'IntParam' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.int_param import IntParam')
    if 'KnowledgeActivateObject' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.knowledge_activate_object import KnowledgeActivateObject')
    if 'KnowledgeObject' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.knowledge_object import KnowledgeObject')
    if 'Law' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.law import Law')
    if 'Length' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.length import Length')
    if 'List' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.list import List')
    if 'ListParameter' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.list_parameter import ListParameter')
    if 'Parameter' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.parameter import Parameter')
    if 'Parameters' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.parameters import Parameters')
    if 'ParamSets' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.parameter_sets import ParamSets')
    if 'RealParam' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.real_param import RealParam')
    if 'Relation' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.relation import Relation')
    if 'Relations' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.relations import Relations')
    if 'Rule' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.rule import Rule')
    if 'SetOfEquation' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.set_of_equation import SetOfEquation')
    if 'StrParam' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.str_param import StrParam')
    if 'Unit' in returns:
        imports.append(f'from pycatia.knowledge_interfaces.unit import Unit')

    # hybrid shape interfaces
    if 'HybridShape3DCurveOffset' in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape3_d_curve_offset import HybridShape3DCurveOffset')
    if 'HybridShapeAffinity' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_affinity import HybridShapeAffinity')
    if 'HybridShapeAssemble' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_assemble import HybridShapeAssemble')
    if 'HybridShapeAxisLine' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_axis_line import HybridShapeAxisLine')
    if 'HybridShapeAxisToAxis' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_axis_to_axis import HybridShapeAxisToAxis')
    if 'HybridShapeBlend' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_blend import HybridShapeBlend')
    if 'HybridShapeBoundary' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_boundary import HybridShapeBoundary')
    if 'HybridShapeBump' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_bump import HybridShapeBump')
    if inflection.camelize("hybrid_shape_circle") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle import {inflection.camelize("hybrid_shape_circle")}')
    if inflection.camelize("hybrid_shape_circle2_points_rad") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle2_points_rad import {inflection.camelize("hybrid_shape_circle2_points_rad")}')
    if inflection.camelize("hybrid_shape_circle3_points") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle3_points import {inflection.camelize("hybrid_shape_circle3_points")}')
    if inflection.camelize("hybrid_shape_circle_bitangent_point") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_bitangent_point import {inflection.camelize("hybrid_shape_circle_bitangent_point")}')
    if inflection.camelize("hybrid_shape_circle_bitangent_radius") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_bitangent_radius import {inflection.camelize("hybrid_shape_circle_bitangent_radius")}')
    if inflection.camelize("hybrid_shape_circle_center_axis") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_center_axis import {inflection.camelize("hybrid_shape_circle_center_axis")}')
    if inflection.camelize("hybrid_shape_circle_center_tangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_center_tangent import {inflection.camelize("hybrid_shape_circle_center_tangent")}')
    if inflection.camelize("hybrid_shape_circle_ctr_pt") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_ctr_pt import {inflection.camelize("hybrid_shape_circle_ctr_pt")}')
    if inflection.camelize("hybrid_shape_circle_ctr_rad") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_ctr_rad import {inflection.camelize("hybrid_shape_circle_ctr_rad")}')
    if inflection.camelize("hybrid_shape_circle_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_explicit import {inflection.camelize("hybrid_shape_circle_explicit")}')
    if inflection.camelize("hybrid_shape_circle_tritangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_circle_tritangent import {inflection.camelize("hybrid_shape_circle_tritangent")}')
    if inflection.camelize("hybrid_shape_combine") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_combine import {inflection.camelize("hybrid_shape_combine")}')
    if inflection.camelize("hybrid_shape_conic") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_conic import {inflection.camelize("hybrid_shape_conic")}')
    if inflection.camelize("hybrid_shape_connect") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_connect import {inflection.camelize("hybrid_shape_connect")}')
    if inflection.camelize("hybrid_shape_corner") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_corner import {inflection.camelize("hybrid_shape_corner")}')
    if inflection.camelize("hybrid_shape_curve_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_curve_explicit import {inflection.camelize("hybrid_shape_curve_explicit")}')
    if inflection.camelize("hybrid_shape_curve_par") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_curve_par import {inflection.camelize("hybrid_shape_curve_par")}')
    if inflection.camelize("hybrid_shape_curve_smooth") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_curve_smooth import {inflection.camelize("hybrid_shape_curve_smooth")}')
    if inflection.camelize("hybrid_shape_cylinder") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_cylinder import {inflection.camelize("hybrid_shape_cylinder")}')
    if inflection.camelize("hybrid_shape_develop") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_develop import {inflection.camelize("hybrid_shape_develop")}')
    if 'HybridShapeDirection' in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.hybrid_shape_direction import HybridShapeDirection')
    if inflection.camelize("hybrid_shape_extract") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_extract import {inflection.camelize("hybrid_shape_extract")}')
    if inflection.camelize("hybrid_shape_extract_multi") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_extract_multi import {inflection.camelize("hybrid_shape_extract_multi")}')
    if inflection.camelize("hybrid_shape_extrapol") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_extrapol import {inflection.camelize("hybrid_shape_extrapol")}')
    if inflection.camelize("hybrid_shape_extremum") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_extremum import {inflection.camelize("hybrid_shape_extremum")}')
    if inflection.camelize("hybrid_shape_extremum_polar") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_extremum_polar import {inflection.camelize("hybrid_shape_extremum_polar")}')
    if inflection.camelize("hybrid_shape_extrude") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_extrude import {inflection.camelize("hybrid_shape_extrude")}')
    if inflection.camelize("hybrid_shape_factory") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_factory import {inflection.camelize("hybrid_shape_factory")}')
    if inflection.camelize("hybrid_shape_fill") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_fill import {inflection.camelize("hybrid_shape_fill")}')
    if inflection.camelize("hybrid_shape_fillet_bi_tangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_fillet_bi_tangent import {inflection.camelize("hybrid_shape_fillet_bi_tangent")}')
    if inflection.camelize("hybrid_shape_fillet_tri_tangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_fillet_tri_tangent import {inflection.camelize("hybrid_shape_fillet_tri_tangent")}')
    if inflection.camelize("hybrid_shape_healing") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_healing import {inflection.camelize("hybrid_shape_healing")}')
    if inflection.camelize("hybrid_shape_helix") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_helix import {inflection.camelize("hybrid_shape_helix")}')
    if inflection.camelize("hybrid_shape_integrated_law") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_integrated_law import {inflection.camelize("hybrid_shape_integrated_law")}')
    if inflection.camelize("hybrid_shape_intersection") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_intersection import {inflection.camelize("hybrid_shape_intersection")}')
    if inflection.camelize("hybrid_shape_inverse") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_inverse import {inflection.camelize("hybrid_shape_inverse")}')
    if inflection.camelize("hybrid_shape_law_dist_proj") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_law_dist_proj import {inflection.camelize("hybrid_shape_law_dist_proj")}')
    if inflection.camelize("hybrid_shape_line_angle") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_angle import {inflection.camelize("hybrid_shape_line_angle")}')
    if inflection.camelize("hybrid_shape_line_bi_tangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_bi_tangent import {inflection.camelize("hybrid_shape_line_bi_tangent")}')
    if inflection.camelize("hybrid_shape_line_bisecting") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_bisecting import {inflection.camelize("hybrid_shape_line_bisecting")}')
    if inflection.camelize("hybrid_shape_line_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_explicit import {inflection.camelize("hybrid_shape_line_explicit")}')
    if inflection.camelize("hybrid_shape_line_normal") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_normal import {inflection.camelize("hybrid_shape_line_normal")}')
    if inflection.camelize("hybrid_shape_line_pt_dir") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_pt_dir import {inflection.camelize("hybrid_shape_line_pt_dir")}')
    if inflection.camelize("hybrid_shape_line_pt_pt") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_pt_pt import {inflection.camelize("hybrid_shape_line_pt_pt")}')
    if inflection.camelize("hybrid_shape_line_tangency") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_line_tangency import {inflection.camelize("hybrid_shape_line_tangency")}')
    if inflection.camelize("hybrid_shape_loft") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_loft import {inflection.camelize("hybrid_shape_loft")}')
    if inflection.camelize("hybrid_shape_mid_surface") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_mid_surface import {inflection.camelize("hybrid_shape_mid_surface")}')
    if inflection.camelize("hybrid_shape_near") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_near import {inflection.camelize("hybrid_shape_near")}')
    if inflection.camelize("hybrid_shape_offset") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_offset import {inflection.camelize("hybrid_shape_offset")}')
    if inflection.camelize("hybrid_shape_plane1_curve") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane1_curve import {inflection.camelize("hybrid_shape_plane1_curve")}')
    if inflection.camelize("hybrid_shape_plane1_line1_pt") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane1_line1_pt import {inflection.camelize("hybrid_shape_plane1_line1_pt")}')
    if inflection.camelize("hybrid_shape_plane2_lines") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane2_lines import {inflection.camelize("hybrid_shape_plane2_lines")}')
    if inflection.camelize("hybrid_shape_plane3_points") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane3_points import {inflection.camelize("hybrid_shape_plane3_points")}')
    if inflection.camelize("hybrid_shape_plane_angle") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_angle import {inflection.camelize("hybrid_shape_plane_angle")}')
    if inflection.camelize("hybrid_shape_plane_equation") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_equation import {inflection.camelize("hybrid_shape_plane_equation")}')
    if inflection.camelize("hybrid_shape_plane_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_explicit import {inflection.camelize("hybrid_shape_plane_explicit")}')
    if inflection.camelize("hybrid_shape_plane_mean") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_mean import {inflection.camelize("hybrid_shape_plane_mean")}')
    if inflection.camelize("hybrid_shape_plane_normal") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_normal import {inflection.camelize("hybrid_shape_plane_normal")}')
    if inflection.camelize("hybrid_shape_plane_offset") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_offset import {inflection.camelize("hybrid_shape_plane_offset")}')
    if inflection.camelize("hybrid_shape_plane_offset_pt") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_offset_pt import {inflection.camelize("hybrid_shape_plane_offset_pt")}')
    if inflection.camelize("hybrid_shape_plane_tangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_plane_tangent import {inflection.camelize("hybrid_shape_plane_tangent")}')
    if inflection.camelize("hybrid_shape_point_between") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_between import {inflection.camelize("hybrid_shape_point_between")}')
    if inflection.camelize("hybrid_shape_point_center") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_center import {inflection.camelize("hybrid_shape_point_center")}')
    if inflection.camelize("hybrid_shape_point_coord") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_coord import {inflection.camelize("hybrid_shape_point_coord")}')
    if inflection.camelize("hybrid_shape_point_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_explicit import {inflection.camelize("hybrid_shape_point_explicit")}')
    if inflection.camelize("hybrid_shape_point_on_curve") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_on_curve import {inflection.camelize("hybrid_shape_point_on_curve")}')
    if inflection.camelize("hybrid_shape_point_on_plane") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_on_plane import {inflection.camelize("hybrid_shape_point_on_plane")}')
    if inflection.camelize("hybrid_shape_point_on_surface") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_on_surface import {inflection.camelize("hybrid_shape_point_on_surface")}')
    if inflection.camelize("hybrid_shape_point_tangent") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_point_tangent import {inflection.camelize("hybrid_shape_point_tangent")}')
    if inflection.camelize("hybrid_shape_polyline") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_polyline import {inflection.camelize("hybrid_shape_polyline")}')
    if inflection.camelize("hybrid_shape_position_transfo") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_position_transfo import {inflection.camelize("hybrid_shape_position_transfo")}')
    if inflection.camelize("hybrid_shape_project") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_project import {inflection.camelize("hybrid_shape_project")}')
    if inflection.camelize("hybrid_shape_reflect_line") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_reflect_line import {inflection.camelize("hybrid_shape_reflect_line")}')
    if inflection.camelize("hybrid_shape_revol") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_revol import {inflection.camelize("hybrid_shape_revol")}')
    if inflection.camelize("hybrid_shape_rolling_offset") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_rolling_offset import {inflection.camelize("hybrid_shape_rolling_offset")}')
    if inflection.camelize("hybrid_shape_rotate") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_rotate import {inflection.camelize("hybrid_shape_rotate")}')
    if inflection.camelize("hybrid_shape_scaling") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_scaling import {inflection.camelize("hybrid_shape_scaling")}')
    if inflection.camelize("hybrid_shape_section") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_section import {inflection.camelize("hybrid_shape_section")}')
    if inflection.camelize("hybrid_shape_sphere") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_sphere import {inflection.camelize("hybrid_shape_sphere")}')
    if inflection.camelize("hybrid_shape_spine") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_spine import {inflection.camelize("hybrid_shape_spine")}')
    if inflection.camelize("hybrid_shape_spiral") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_spiral import {inflection.camelize("hybrid_shape_spiral")}')
    if inflection.camelize("hybrid_shape_spline") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_spline import {inflection.camelize("hybrid_shape_spline")}')
    if inflection.camelize("hybrid_shape_split") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_split import {inflection.camelize("hybrid_shape_split")}')
    if inflection.camelize("hybrid_shape_surface_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_surface_explicit import {inflection.camelize("hybrid_shape_surface_explicit")}')
    if inflection.camelize("hybrid_shape_sweep") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_sweep import {inflection.camelize("hybrid_shape_sweep")}')
    if inflection.camelize("hybrid_shape_sweep_circle") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_sweep_circle import {inflection.camelize("hybrid_shape_sweep_circle")}')
    if inflection.camelize("hybrid_shape_sweep_conic") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_sweep_conic import {inflection.camelize("hybrid_shape_sweep_conic")}')
    if inflection.camelize("hybrid_shape_sweep_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_sweep_explicit import {inflection.camelize("hybrid_shape_sweep_explicit")}')
    if inflection.camelize("hybrid_shape_sweep_line") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_sweep_line import {inflection.camelize("hybrid_shape_sweep_line")}')
    if inflection.camelize("hybrid_shape_symmetry") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_symmetry import {inflection.camelize("hybrid_shape_symmetry")}')
    if inflection.camelize("hybrid_shape_thickness") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_thickness import {inflection.camelize("hybrid_shape_thickness")}')
    if inflection.camelize("hybrid_shape_transfer") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_transfer import {inflection.camelize("hybrid_shape_transfer")}')
    if inflection.camelize("hybrid_shape_translate") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_translate import {inflection.camelize("hybrid_shape_translate")}')
    if inflection.camelize("hybrid_shape_trim") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_trim import {inflection.camelize("hybrid_shape_trim")}')
    if inflection.camelize("hybrid_shape_unfold") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_unfold import {inflection.camelize("hybrid_shape_unfold")}')
    if inflection.camelize("hybrid_shape_volume_explicit") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_volume_explicit import {inflection.camelize("hybrid_shape_volume_explicit")}')
    if inflection.camelize("hybrid_shape_wrap_curve") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_wrap_curve import {inflection.camelize("hybrid_shape_wrap_curve")}')
    if inflection.camelize("hybrid_shape_wrap_surface") in returns:
        imports.append(
            f'from pycatia.hybrid_shape_interfaces.hybrid_shape_wrap_surface import {inflection.camelize("hybrid_shape_wrap_surface")}')
    if inflection.camelize("line") in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.line import {inflection.camelize("line")}')
    if inflection.camelize("plane") in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.plane import {inflection.camelize("plane")}')
    if inflection.camelize("point") in returns:
        imports.append(f'from pycatia.hybrid_shape_interfaces.point import {inflection.camelize("point")}')

    # mec mod interfaces
    if 'AxisSystem' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.axis_system import AxisSystem')
    if 'AxisSystems' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.axis_systems import AxisSystems')
    if 'BiDimFeatEdge' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.bi_dim_feat_edge import BiDimFeatEdge')
    if 'Bodies' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.bodies import Bodies')
    if 'Body' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.body import Body')
    if 'Boundary' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.boundary import Boundary')
    if 'Constraint' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.constraint import Constraint')
    if 'Constraints' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.constraints import Constraints')
    if 'CylindricalFace' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.cylindrical_face import CylindricalFace')
    if 'Edge' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.edge import Edge')
    if 'Face' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.face import Face')
    if 'Factory' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.factory import Factory')
    if 'FixTogether' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.fix_together import FixTogether')
    if 'FixTogethers' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.fix_togethers import FixTogethers')
    if 'GeometricElements' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.geometric_elements import GeometricElements')
    if 'HybridBodies' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.hybrid_bodies import HybridBodies')
    if 'HybridBody' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.hybrid_body import HybridBody')
    if 'HybridShape' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.hybrid_shape import HybridShape')
    if 'HybridShapeInstance' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.hybrid_shape_instance import HybridShapeInstance')
    if 'HybridShapes' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.hybrid_shapes import HybridShapes')
    if 'InstanceFactory' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.instance_factory import InstanceFactory')
    if 'MonoDimFeatEdge' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.mono_dim_feat_edge import MonoDimFeatEdge')
    if 'NotWireBoundaryMonoDimFeatVertex' in returns:
        imports.append(
            f'from pycatia.mec_mod_interfaces.not_wire_boundary_mono_dim_feat_vertex import NotWireBoundaryMonoDimFeatVertex')
    if 'OrderedGeometricalSet' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.ordered_geometrical_set import OrderedGeometricalSet')
    if 'OrderedGeometricalSets' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.ordered_geometrical_sets import OrderedGeometricalSets')
    if 'OriginElements' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.origin_elements import OriginElements')
    if 'Part' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.part import Part')
    if 'PartDocument' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.part_document import PartDocument')
    if 'PartInfrastructureSettingAtt' in returns:
        imports.append(
            f'from pycatia.mec_mod_interfaces.part_infrastructure_setting_att import PartInfrastructureSettingAtt')
    if 'PlanarFace' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.planar_face import PlanarFace')
    if 'RectilinearBiDimFeatEdge' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.rectilinear_bi_dim_feat_edge import RectilinearBiDimFeatEdge')
    if 'RectilinearMonoDimFeatEdge' in returns:
        imports.append(
            f'from pycatia.mec_mod_interfaces.rectilinear_mono_dim_feat_edge import RectilinearMonoDimFeatEdge')
    if 'RectilinearTriDimFeatEdge' in returns:
        imports.append(
            f'from pycatia.mec_mod_interfaces.rectilinear_tri_dim_feat_edge import RectilinearTriDimFeatEdge')
    if 'Shape' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.shape import Shape')
    if 'ShapeInstance' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.shape_instance import ShapeInstance')
    if 'Shapes' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.shapes import Shapes')
    if 'Sketches' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.sketches import Sketches')
    if 'Solid' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.solid import Solid')
    if 'TriDimFeatEdge' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.tri_dim_feat_edge import TriDimFeatEdge')
    if 'TriDimFeatVertexOrBiDimFeatVertex' in returns:
        imports.append(
            f'from pycatia.mec_mod_interfaces.tri_dim_feat_vertex_or_bi_dim_feat_vertex import TriDimFeatVertexOrBiDimFeatVertex')
    if 'Vertex' in returns:
        imports.append(f'from pycatia.mec_mod_interfaces.vertex import Vertex')
    if 'ZeroDimFeatVertexOrWireBoundaryMonoDimFeatVertex' in returns:
        imports.append(
            f'from pycatia.mec_mod_interfaces.zero_dim_feat_vertex_or_wire_boundary_mono_dim_feat_vertex import ZeroDimFeatVertexOrWireBoundaryMonoDimFeatVertex')

    # drafting
    if 'DraftingSettingAtt' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drafting_setting_att import DraftingSettingAtt')
    if 'DrawingArrow' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_arrow import DrawingArrow')
    if 'DrawingArrows' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_arrows import DrawingArrows')
    if 'DrawingComponent' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_component import DrawingComponent')
    if 'DrawingComponents' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_components import DrawingComponents')
    if 'DrawingDimExtLine' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_dim_ext_line import DrawingDimExtLine')
    if 'DrawingDimLine' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_dim_line import DrawingDimLine')
    if 'DrawingDimValue' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_dim_value import DrawingDimValue')
    if 'DrawingDimension' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_dimension import DrawingDimension')
    if 'DrawingDimensions' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_dimensions import DrawingDimensions')
    if 'DrawingDocument' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_document import DrawingDocument')
    if 'DrawingLeader' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_leader import DrawingLeader')
    if 'DrawingLeaders' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_leaders import DrawingLeaders')
    if 'DrawingPageSetup' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_page_setup import DrawingPageSetup')
    if 'DrawingPicture' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_picture import DrawingPicture')
    if 'DrawingPictures' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_pictures import DrawingPictures')
    if 'DrawingRoot' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_root import DrawingRoot')
    if 'DrawingSheet' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_sheet import DrawingSheet')
    if 'DrawingSheets' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_sheets import DrawingSheets')
    if 'DrawingTable' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_table import DrawingTable')
    if 'DrawingTables' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_tables import DrawingTables')
    if 'DrawingText' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_text import DrawingText')
    if 'DrawingTextProperties' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_text_properties import DrawingTextProperties')
    if 'DrawingTextRange' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_text_range import DrawingTextRange')
    if 'DrawingTexts' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_texts import DrawingTexts')
    if 'DrawingThread' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_thread import DrawingThread')
    if 'DrawingThreads' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_threads import DrawingThreads')
    if 'DrawingView' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_view import DrawingView')
    if 'DrawingViewGenerativeBehavior' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_view_generative_behavior import DrawingViewGenerativeBehavior')
    if 'DrawingViewGenerativeLinks' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_view_generative_links import DrawingViewGenerativeLinks')
    if 'DrawingViews' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_views import DrawingViews')
    if 'DrawingWelding' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_welding import DrawingWelding')
    if 'DrawingWeldings' in returns:
        imports.append(f'from pycatia.drafting_interfaces.drawing_weldings import DrawingWeldings')
    if 'PrintArea' in returns:
        imports.append(f'from pycatia.drafting_interfaces.print_area import PrintArea')

    # in interfaces
    if 'Application' in returns:
        imports.append(f'from pycatia.in_interfaces.application import Application')
    if 'Camera' in returns:
        imports.append(f'from pycatia.in_interfaces.camera import Camera')
    if 'Camera2D' in returns:
        imports.append(f'from pycatia.in_interfaces.camera2_d import Camera2D')
    if 'Camera3D' in returns:
        imports.append(f'from pycatia.in_interfaces.camera3_d import Camera3D')
    if 'Cameras' in returns:
        imports.append(f'from pycatia.in_interfaces.cameras import Cameras')
    if 'CgrAdhesionSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.cgr_adhesion_setting_att import CgrAdhesionSettingAtt')
    if 'Document' in returns:
        imports.append(f'from pycatia.in_interfaces.document import Document')
    if 'DocumentationSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.documentation_setting_att import DocumentationSettingAtt')
    if 'Documents' in returns:
        imports.append(f'from pycatia.in_interfaces.documents import Documents')
    if 'DraftingPageSetup' in returns:
        imports.append(f'from pycatia.in_interfaces.drafting_page_setup import DraftingPageSetup')
    if 'File' in returns:
        imports.append(f'from pycatia.in_interfaces.file import File')
    if 'FileComponent' in returns:
        imports.append(f'from pycatia.in_interfaces.file_component import FileComponent')
    if 'FileSystem' in returns:
        imports.append(f'from pycatia.in_interfaces.file_system import FileSystem')
    if 'Files' in returns:
        imports.append(f'from pycatia.in_interfaces.files import Files')
    if 'Folder' in returns:
        imports.append(f'from pycatia.in_interfaces.folder import Folder')
    if 'Folders' in returns:
        imports.append(f'from pycatia.in_interfaces.folders import Folders')
    if 'GeneralSessionSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.general_session_setting_att import GeneralSessionSettingAtt')
    if 'LightSource' in returns:
        imports.append(f'from pycatia.in_interfaces.light_source import LightSource')
    if 'LightSources' in returns:
        imports.append(f'from pycatia.in_interfaces.light_sources import LightSources')
    if 'MacrosSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.macros_setting_att import MacrosSettingAtt')
    if 'Move' in returns:
        imports.append(f'from pycatia.in_interfaces.move import Move')
    if 'PageSetup' in returns:
        imports.append(f'from pycatia.in_interfaces.page_setup import PageSetup')
    if 'Position' in returns:
        imports.append(f'from pycatia.in_interfaces.position import Position')
    if 'Printer' in returns:
        imports.append(f'from pycatia.in_interfaces.printer import Printer')
    if 'Printers' in returns:
        imports.append(f'from pycatia.in_interfaces.printers import Printers')
    if 'PrintersSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.printers_setting_att import PrintersSettingAtt')
    if 'Reference' in returns:
        imports.append(f'from pycatia.in_interfaces.reference import Reference')
    if 'References' in returns:
        imports.append(f'from pycatia.in_interfaces.references import References')
    if 'SearchSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.search_setting_att import SearchSettingAtt')
    if 'SelectedElement' in returns:
        imports.append(f'from pycatia.in_interfaces.selected_element import SelectedElement')
    if 'Selection' in returns:
        imports.append(f'from pycatia.in_interfaces.selection import Selection')
    if 'SelectionSets' in returns:
        imports.append(f'from pycatia.in_interfaces.selection_sets import SelectionSets')
    if 'SendToService' in returns:
        imports.append(f'from pycatia.in_interfaces.send_to_service import SendToService')
    if 'SettingControllers' in returns:
        imports.append(f'from pycatia.in_interfaces.setting_controllers import SettingControllers')
    if 'SpecsAndGeomWindow' in returns:
        imports.append(f'from pycatia.in_interfaces.specs_and_geom_window import SpecsAndGeomWindow')
    if 'SpecsViewer' in returns:
        imports.append(f'from pycatia.in_interfaces.specs_viewer import SpecsViewer')
    if 'SystemConfiguration' in returns:
        imports.append(f'from pycatia.in_interfaces.system_configuration import SystemConfiguration')
    if 'TextStream' in returns:
        imports.append(f'from pycatia.in_interfaces.text_stream import TextStream')
    if 'TreeVizManipSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.tree_viz_manip_setting_att import TreeVizManipSettingAtt')
    if 'Viewer' in returns:
        imports.append(f'from pycatia.in_interfaces.viewer import Viewer')
    if 'Viewer2D' in returns:
        imports.append(f'from pycatia.in_interfaces.viewer2_d import Viewer2D')
    if 'Viewer3D' in returns:
        imports.append(f'from pycatia.in_interfaces.viewer3_d import Viewer3D')
    if 'Viewers' in returns:
        imports.append(f'from pycatia.in_interfaces.viewers import Viewers')
    if 'Viewpoint2D' in returns:
        imports.append(f'from pycatia.in_interfaces.viewpoint2_d import Viewpoint2D')
    if 'Viewpoint3D' in returns:
        imports.append(f'from pycatia.in_interfaces.viewpoint3_d import Viewpoint3D')
    if 'VisPropertySet' in returns:
        imports.append(f'from pycatia.in_interfaces.vis_property_set import VisPropertySet')
    if 'VisualizationSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.visualization_setting_att import VisualizationSettingAtt')
    if 'VrmlSettingAtt' in returns:
        imports.append(f'from pycatia.in_interfaces.vrml_setting_att import VrmlSettingAtt')
    if 'Window' in returns:
        imports.append(f'from pycatia.in_interfaces.window import Window')
    if 'Windows' in returns:
        imports.append(f'from pycatia.in_interfaces.windows import Windows')
    if 'Workbench' in returns:
        imports.append(f'from pycatia.in_interfaces.workbench import Workbench')

    # system interfaces
    if 'AccesslogStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.accesslog_statistics_setting_att import AccesslogStatisticsSettingAtt')
    if 'AnyObject' in returns:
        imports.append(f'from pycatia.system_interfaces.any_object import AnyObject')
    if 'CacheSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.cache_setting_att import CacheSettingAtt')
    if 'CatBaseDispatch' in returns:
        imports.append(f'from pycatia.system_interfaces.cat_base_dispatch import CatBaseDispatch')
    if 'CatBaseUnknown' in returns:
        imports.append(f'from pycatia.system_interfaces.cat_base_unknown import CatBaseUnknown')
    if 'Collection' in returns:
        imports.append(f'from pycatia.system_interfaces.collection import Collection')
    if 'CommandStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.command_statistics_setting_att import CommandStatisticsSettingAtt')
    if 'DisconnectionSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.disconnection_setting_att import DisconnectionSettingAtt')
    if 'DlNameSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.dl_name_setting_att import DlNameSettingAtt')
    if 'DynLicenseSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.dyn_license_setting_att import DynLicenseSettingAtt')
    if 'ErrorlogStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.errorlog_statistics_setting_att import ErrorlogStatisticsSettingAtt')
    if 'FileAccessStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.file_access_statistics_setting_att import FileAccessStatisticsSettingAtt')
    if 'GeneralStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.general_statistics_setting_att import GeneralStatisticsSettingAtt')
    if 'GlobalStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.global_statistics_setting_att import GlobalStatisticsSettingAtt')
    if 'IDispatch' in returns:
        imports.append(f'from pycatia.system_interfaces.i_dispatch import IDispatch')
    if 'IUnknown' in returns:
        imports.append(f'from pycatia.system_interfaces.i_unknown import IUnknown')
    if 'LicenseSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.license_setting_att import LicenseSettingAtt')
    if 'MemoryWarningSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.memory_warning_setting_att import MemoryWarningSettingAtt')
    if 'PcsStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.pcs_statistics_setting_att import PcsStatisticsSettingAtt')
    if 'ServerStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.server_statistics_setting_att import ServerStatisticsSettingAtt')
    if 'SessionStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.session_statistics_setting_att import SessionStatisticsSettingAtt')
    if 'SettingController' in returns:
        imports.append(f'from pycatia.system_interfaces.setting_controller import SettingController')
    if 'SettingRepository' in returns:
        imports.append(f'from pycatia.system_interfaces.setting_repository import SettingRepository')
    if 'SystemService' in returns:
        imports.append(f'from pycatia.system_interfaces.system_service import SystemService')
    if 'WorkbenchStatisticsSettingAtt' in returns:
        imports.append(f'from pycatia.system_interfaces.workbench_statistics_setting_att import WorkbenchStatisticsSettingAtt')

    # product structure interfaces
    if 'Analyze' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.analyze import Analyze')
    if 'AssemblyConvertor' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.assembly_convertor import AssemblyConvertor')
    if 'Product' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.product import Product')
    if 'ProductDocument' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.product_document import ProductDocument')
    if 'Products' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.products import Products')
    if 'Publication' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.publication import Publication')
    if 'Publications' in returns:
        imports.append(f'from pycatia.product_structure_interfaces.publications import Publications')

    if 'Add' in returns:
        imports.append(f'from pycatia.part_interfaces.add import Add')
    if 'Affinity' in returns:
        imports.append(f'from pycatia.part_interfaces.affinity import Affinity')
    if 'AngularRepartition' in returns:
        imports.append(f'from pycatia.part_interfaces.angular_repartition import AngularRepartition')
    if 'Assemble' in returns:
        imports.append(f'from pycatia.part_interfaces.assemble import Assemble')
    if 'AutoDraft' in returns:
        imports.append(f'from pycatia.part_interfaces.auto_draft import AutoDraft')
    if 'AutoFillet' in returns:
        imports.append(f'from pycatia.part_interfaces.auto_fillet import AutoFillet')
    if 'AxisToAxis' in returns:
        imports.append(f'from pycatia.part_interfaces.axis_to_axis import AxisToAxis')
    if 'BooleanShape' in returns:
        imports.append(f'from pycatia.part_interfaces.boolean_shape import BooleanShape')
    if 'Chamfer' in returns:
        imports.append(f'from pycatia.part_interfaces.chamfer import Chamfer')
    if 'CircPattern' in returns:
        imports.append(f'from pycatia.part_interfaces.circ_pattern import CircPattern')
    if 'CloseSurface' in returns:
        imports.append(f'from pycatia.part_interfaces.close_surface import CloseSurface')
    if 'ConstRadEdgeFillet' in returns:
        imports.append(f'from pycatia.part_interfaces.const_rad_edge_fillet import ConstRadEdgeFillet')
    if 'Defeaturing' in returns:
        imports.append(f'from pycatia.part_interfaces.defeaturing import Defeaturing')
    if 'DefeaturingFilletFilter' in returns:
        imports.append(f'from pycatia.part_interfaces.defeaturing_fillet_filter import DefeaturingFilletFilter')
    if 'DefeaturingFilter' in returns:
        imports.append(f'from pycatia.part_interfaces.defeaturing_filter import DefeaturingFilter')
    if 'DefeaturingFilterWithRange' in returns:
        imports.append(f'from pycatia.part_interfaces.defeaturing_filter_with_range import DefeaturingFilterWithRange')
    if 'DefeaturingFilters' in returns:
        imports.append(f'from pycatia.part_interfaces.defeaturing_filters import DefeaturingFilters')
    if 'DefeaturingHoleFilter' in returns:
        imports.append(f'from pycatia.part_interfaces.defeaturing_hole_filter import DefeaturingHoleFilter')
    if 'Draft' in returns:
        imports.append(f'from pycatia.part_interfaces.draft import Draft')
    if 'DraftDomain' in returns:
        imports.append(f'from pycatia.part_interfaces.draft_domain import DraftDomain')
    if 'DraftDomains' in returns:
        imports.append(f'from pycatia.part_interfaces.draft_domains import DraftDomains')
    if 'DressUpShape' in returns:
        imports.append(f'from pycatia.part_interfaces.dress_up_shape import DressUpShape')
    if 'EdgeFillet' in returns:
        imports.append(f'from pycatia.part_interfaces.edge_fillet import EdgeFillet')
    if 'FaceFillet' in returns:
        imports.append(f'from pycatia.part_interfaces.face_fillet import FaceFillet')
    if 'Fillet' in returns:
        imports.append(f'from pycatia.part_interfaces.fillet import Fillet')
    if 'Groove' in returns:
        imports.append(f'from pycatia.part_interfaces.groove import Groove')
    if 'Hole' in returns:
        imports.append(f'from pycatia.part_interfaces.hole import Hole')
    if 'Intersect' in returns:
        imports.append(f'from pycatia.part_interfaces.intersect import Intersect')
    if 'Limit' in returns:
        imports.append(f'from pycatia.part_interfaces.limit import Limit')
    if 'LinearRepartition' in returns:
        imports.append(f'from pycatia.part_interfaces.linear_repartition import LinearRepartition')
    if 'Loft' in returns:
        imports.append(f'from pycatia.part_interfaces.loft import Loft')
    if 'Mirror' in returns:
        imports.append(f'from pycatia.part_interfaces.mirror import Mirror')
    if 'Pad' in returns:
        imports.append(f'from pycatia.part_interfaces.pad import Pad')
    if 'Pattern' in returns:
        imports.append(f'from pycatia.part_interfaces.pattern import Pattern')
    if 'Pocket' in returns:
        imports.append(f'from pycatia.part_interfaces.pocket import Pocket')
    if 'Prism' in returns:
        imports.append(f'from pycatia.part_interfaces.prism import Prism')
    if 'RectPattern' in returns:
        imports.append(f'from pycatia.part_interfaces.rect_pattern import RectPattern')
    if 'Remove' in returns:
        imports.append(f'from pycatia.part_interfaces.remove import Remove')
    if 'RemoveFace' in returns:
        imports.append(f'from pycatia.part_interfaces.remove_face import RemoveFace')
    if 'Repartition' in returns:
        imports.append(f'from pycatia.part_interfaces.repartition import Repartition')
    if 'ReplaceFace' in returns:
        imports.append(f'from pycatia.part_interfaces.replace_face import ReplaceFace')
    if 'Revolution' in returns:
        imports.append(f'from pycatia.part_interfaces.revolution import Revolution')
    if 'Rib' in returns:
        imports.append(f'from pycatia.part_interfaces.rib import Rib')
    if 'Rotate' in returns:
        imports.append(f'from pycatia.part_interfaces.rotate import Rotate')
    if 'Scaling' in returns:
        imports.append(f'from pycatia.part_interfaces.scaling import Scaling')
    if 'Scaling2' in returns:
        imports.append(f'from pycatia.part_interfaces.scaling2 import Scaling2')
    if 'SewSurface' in returns:
        imports.append(f'from pycatia.part_interfaces.sew_surface import SewSurface')
    if 'Shaft' in returns:
        imports.append(f'from pycatia.part_interfaces.shaft import Shaft')
    if 'ShapeFactory' in returns:
        imports.append(f'from pycatia.part_interfaces.shape_factory import ShapeFactory')
    if 'Shell' in returns:
        imports.append(f'from pycatia.part_interfaces.shell import Shell')
    if 'SketchBasedShape' in returns:
        imports.append(f'from pycatia.part_interfaces.sketch_based_shape import SketchBasedShape')
    if 'Slot' in returns:
        imports.append(f'from pycatia.part_interfaces.slot import Slot')
    if 'SolidCombine' in returns:
        imports.append(f'from pycatia.part_interfaces.solid_combine import SolidCombine')
    if 'Split' in returns:
        imports.append(f'from pycatia.part_interfaces.split import Split')
    if 'Stiffener' in returns:
        imports.append(f'from pycatia.part_interfaces.stiffener import Stiffener')
    if 'SurfaceBasedShape' in returns:
        imports.append(f'from pycatia.part_interfaces.surface_based_shape import SurfaceBasedShape')
    if 'Sweep' in returns:
        imports.append(f'from pycatia.part_interfaces.sweep import Sweep')
    if 'Symmetry' in returns:
        imports.append(f'from pycatia.part_interfaces.symmetry import Symmetry')
    if 'ThickSurface' in returns:
        imports.append(f'from pycatia.part_interfaces.thick_surface import ThickSurface')
    if 'Thickness' in returns:
        imports.append(f'from pycatia.part_interfaces.thickness import Thickness')
    if 'Thread' in returns:
        imports.append(f'from pycatia.part_interfaces.thread import Thread')
    if 'TransformationShape' in returns:
        imports.append(f'from pycatia.part_interfaces.transformation_shape import TransformationShape')
    if 'Translate' in returns:
        imports.append(f'from pycatia.part_interfaces.translate import Translate')
    if 'Trim' in returns:
        imports.append(f'from pycatia.part_interfaces.trim import Trim')
    if 'TritangentFillet' in returns:
        imports.append(f'from pycatia.part_interfaces.tritangent_fillet import TritangentFillet')
    if 'UserPattern' in returns:
        imports.append(f'from pycatia.part_interfaces.user_pattern import UserPattern')
    if 'UserRepartition' in returns:
        imports.append(f'from pycatia.part_interfaces.user_repartition import UserRepartition')
    if 'VarRadEdgeFillet' in returns:
        imports.append(f'from pycatia.part_interfaces.var_rad_edge_fillet import VarRadEdgeFillet')

    imports.sort()

    return '\n'.join(imports)
