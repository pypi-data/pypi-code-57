import pathlib
import shutil
import tempfile

import numpy as np
from PySide2.QtGui import QColor

import vmi
import vtk


def LeftButtonPressRelease(**kwargs):
    if kwargs['picked'] is color_box:
        color = QColor.fromRgbF(*property.GetColor(), 1)
        rgb = vmi.askInts([0, 0, 0], [color.red(), color.green(), color.blue()], [255, 255, 255], title='主色')
        if rgb is not None:
            color = QColor.fromRgb(*rgb)
            property.SetColor(color.redF(), color.greenF(), color.blueF())
            color_box.draw_text('主色: {:.0f}, {:.0f}, {:.0f}'.format(color.red(), color.green(), color.blue()),
                                back_color=color)


def NoButtonWheel(**kwargs):
    if kwargs['picked'] is ambient_box:
        r = property.GetAmbient() + 0.01 * kwargs['delta']
        r = min(max(r, property.GetAmbientMinValue()), property.GetAmbientMaxValue())
        property.SetAmbient(r)
        ambient_box.draw_text('环境: {:.2f}'.format(property.GetAmbient()))
    elif kwargs['picked'] is diffuse_box:
        r = property.GetDiffuse() + 0.01 * kwargs['delta']
        r = min(max(r, property.GetDiffuseMinValue()), property.GetDiffuseMaxValue())
        property.SetDiffuse(r)
        diffuse_box.draw_text('扩散: {:.2f}'.format(property.GetDiffuse()))
    elif kwargs['picked'] is specular_box:
        r = property.GetSpecular() + 0.01 * kwargs['delta']
        r = min(max(r, property.GetSpecularMinValue()), property.GetSpecularMaxValue())
        property.SetSpecular(r)
        specular_box.draw_text('反光系数: {:.2f}'.format(property.GetSpecular()))
    elif kwargs['picked'] is specular_power_box:
        r = property.GetSpecularPower() + kwargs['delta']
        r = min(max(r, property.GetSpecularPowerMinValue()), property.GetSpecularPowerMaxValue())
        property.SetSpecularPower(r)
        specular_power_box.draw_text('反光强度: {:.0f}'.format(property.GetSpecularPower()))


if __name__ == '__main__':
    f = vmi.askOpenFile('*.stl', 'STL')
    if f is None:
        vmi.appexit()
    pd = vmi.pdOpenFile_STL(f)

    map_to = vtk.vtkTextureMapToPlane()
    map_to.SetInputData(pd)
    map_to.Update()
    pd = map_to.GetOutput()

    f = vmi.askOpenFile('*.png', 'PNG')
    if f is None:
        vmi.appexit()

    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.png'
        shutil.copy2(f, p)

        reader = vtk.vtkImageReader2Factory().CreateImageReader2(str(p))
        reader.SetFileName(str(p))
        reader.Update()

        texture_data = reader.GetOutput()

    texture = vtk.vtkTexture()
    texture.SetInputData(texture_data)
    texture.SetInterpolate(1)

    view = vmi.View()
    prop = vmi.PolyActor(view)
    prop.setData(pd)
    view.setCamera_Coronal()
    view.setCamera_FitAll()

    # prop._Prop.SetTexture(texture)
    prop._Prop.SetBackfaceProperty(vtk.vtkProperty())

    property = vtk.vtkProperty()
    property.SetAmbient(0.2)
    property.SetDiffuse(0.8)
    property.SetSpecular(0)
    property.SetSpecularPower(0)
    property.SetColor(250 / 255, 246 / 255, 222 / 255)
    prop._Prop.SetProperty(property)

    color = QColor.fromRgbF(*property.GetColor(), 1)
    color_box = vmi.TextBox(view, back_color=color,
                            text='主色: {:.0f}, {:.0f}, {:.0f}'.format(color.red(), color.green(), color.blue()),
                            size=[0.15, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)
    color_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    ambient_box = vmi.TextBox(view, text='环境: {:.2f}'.format(property.GetAmbient()),
                              size=[0.15, 0.04], pos=[0, 0.08], anchor=[0, 0], pickable=True)
    ambient_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    diffuse_box = vmi.TextBox(view, text='扩散: {:.2f}'.format(property.GetDiffuse()),
                              size=[0.15, 0.04], pos=[0, 0.12], anchor=[0, 0], pickable=True)
    diffuse_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    specular_box = vmi.TextBox(view, text='反光系数: {:.2f}'.format(property.GetSpecular()),
                               size=[0.15, 0.04], pos=[0, 0.16], anchor=[0, 0], pickable=True)
    specular_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    specular_power_box = vmi.TextBox(view, text='反光强度: {:.2f}'.format(property.GetSpecularPower()), pickable=True,
                                     size=[0.15, 0.04], pos=[0, 0.20], anchor=[0, 0])
    specular_power_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]


    vmi.appexec(view)
