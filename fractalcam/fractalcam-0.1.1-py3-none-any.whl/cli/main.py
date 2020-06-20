"""
Main CLI Entry Point
"""
import click
import fractalcam

@click.command()
@click.option('-m','--mapper',
              help='Conformal map name.', default='mandelbrot', type=str)
@click.option('-d','--device',
              help='Camera device number, defaults to 0.', default=0, type=int)
def run(mapper, device):
    """
    Script to start webcam, at device, and apply named mapping function.
    """
    with fractalcam.Camera(mapper, device) as fcam:
        while fcam.rval:
            fcam.iterate()