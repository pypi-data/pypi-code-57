import copy,math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


class PacingAndLeading:

    def __init__(self,
                 unit,
                 experiment,
                 dpi,
                 hard_target_display=False,
                 soft_target_display=False,
                 mediator_display=True,
                 vertical_targets_display=True,
                 arrows_display=4):

        self._unit = unit
        
        # creating the main figure
        figsize = (experiment.width/dpi ,
                   experiment.height/dpi)
        self._figure = plt.figure(figsize=figsize,
                                  dpi=dpi)

        # setting the cursor motion callback
        self._figure.canvas.mpl_connect("motion_notify_event",
                                        self.mouse_move)
        
        self._axis = plt.axes(xlim=(0,experiment.width),
                              ylim=(0,experiment.height))
        plt.gca().set_aspect('equal',adjustable='box')
        
        # middle of main figure
        self._center = [experiment.width/2,
                        experiment.height/2]

        # will return for each iteration the
        # position of each circle to draw
        self._experiment = experiment

        # initial cursor position
        self._cursor_position = self._center

        # remove axes
        plt.axis('off')

        # creating the matplotlib circles to draw.
        # if display is False, no circle is drawn
        def _gen_circle(display):
            if display:
                circle = plt.Circle(self._center,0,fc="white")
                self._axis.add_patch(circle)
                return circle
            else :
                return None
            
        def _gen_vertical_bar(display):
            if not display:
                return None
            rectangle = plt.Rectangle((0,experiment.height),
                                      3,
                                      experiment.height,
                                      angle=0.0,
                                      fill=True)
            self._axis.add_patch(rectangle)
            return rectangle

        def _gen_arrow():
            # could not display FancyArrow on Mac, replacing
            # by a line (thin Rectangle) with a circle at its tip
            class Arrow:
                def __init__(self,center,axis):
                    self.tip = plt.Circle(center,0,fc="white")
                    self.rectangle = plt.Rectangle((0,experiment.height),
                                                   3,
                                                   experiment.height,
                                                   angle=0.0,
                                                   fill=True)
                    axis.add_patch(self.rectangle)
                    # ignoring the tip for now
                    #axis.add_patch(self.tip)
            arrow = Arrow(self._center,self._axis)
            return arrow
            
        self._hard_target = _gen_circle(hard_target_display)
        self._soft_target = _gen_circle(soft_target_display)
        self._mediator = _gen_circle(mediator_display)
        self._cursor = _gen_circle(True)
        self._vertical_target1 = _gen_vertical_bar(vertical_targets_display)
        self._vertical_target2 = _gen_vertical_bar(vertical_targets_display)
        if arrows_display:
            self._draw_arrows = [ _gen_arrow()
                                  for _ in range(arrows_display) ]
        
        
        # note that the order is the same as of
        # Experiment._circles
        self._draw_circles = [self._hard_target,
                              self._soft_target,
                              self._mediator,
                              self._cursor]

        self._draw_vertical_targets = [self._vertical_target1,
                                       self._vertical_target2]
        
        # management of the animation by matplotlib
        self._animation = animation.FuncAnimation(self._figure,
                                                  self.animate,
                                                  interval=1000.0/experiment.frequency,
                                                  blit=True)

    def run(self):

        plt.show()
        
    def mouse_move(self,event):

        if not event.inaxes:
            return
        
        self._cursor_position = [event.xdata,
                                 event.ydata]
        
        
    def animate(self,args):

        circles,vertical_targets,arrows = self._experiment.update(self._cursor_position)

        def circle_draw(circle,draw_circle):
            if draw_circle is None:
                return
            display_position = copy.deepcopy(circle.position)
            display_position[0] += circle.x_shift
            draw_circle.center = display_position
            draw_circle.set_radius(circle.size)
            draw_circle.fill=True
            draw_circle.set_color(circle.color)
            return

        list ( map (lambda c,dc: circle_draw(c,dc),
                    circles, self._draw_circles) )
        
        def vertical_target_draw(vertical_target,
                                 draw_vertical_target):
            if draw_vertical_target is None:
                return
            xy = (vertical_target.position[0],vertical_target.position[1])
            draw_vertical_target.set_xy(xy)
            draw_vertical_target.set_width(vertical_target.size)
            draw_vertical_target.fill=True
            draw_vertical_target.set_color(vertical_target.color)
            return

        list( map (lambda vt,dvt : vertical_target_draw(vt,dvt),
                   vertical_targets, self._draw_vertical_targets) )

        def arrow_draw(arrow,
                       display_arrow):

            # could not get matplotlib to draw
            # dynamic arrows on mac, replacing by
            # a line (Rectangle) with a circle at the tip

            x = [arrow.position[0],arrow.position[1]]
            y = [p+d for p,d
                 in zip(arrow.position,arrow.delta)]

            display_arrow.rectangle.set_xy(x)
            display_arrow.rectangle.set_height(arrow.length)
            display_arrow.rectangle.set_width(arrow.width)
            display_arrow.rectangle.fill=True
            display_arrow.rectangle.set_color(arrow.color)

            rotated = [+arrow.delta[1],-arrow.delta[0]]
            
            display_arrow.rectangle.angle = 57.2958*math.atan2(rotated[1],
                                                               rotated[0])

            display_arrow.tip.center = y
            display_arrow.tip.set_radius(arrow.tip_size)
            display_arrow.tip.fill = True
            display_arrow.tip.set_color(arrow.color)

            return display_arrow.rectangle,display_arrow.tip
        
        draw_arrows = []
        for arrow,display_arrow in zip(arrows,self._draw_arrows):
            #draw_arrows.extend(arrow_draw(arrow,display_arrow))
            # ignoring the tip for now
            draw_arrows.extend([arrow_draw(arrow,display_arrow)[0]])
            
        r  = [c for c in  self._draw_circles
              if c is not None] + [vt for vt in self._draw_vertical_targets
                                   if vt is not None] +draw_arrows

        return r
        
        

