from PIL import Image
import click

class Im:

    def __init__(self,image):
        self.image = image

    def format_image(self):
        '''Formatting the image'''
        click.echo(click.style("Converting the image to 2:3 aspect ratio", fg="green"))
        image_obj = Image.open(self.image)
        width = image_obj.width
        formatted_height = (image_obj.width/2)*3
        if formatted_height > image_obj.height:
            click.echo(click.style("Cannot convert to 2:3 aspect ration for the {self.image}", fg="red"))
            return
        img = image_obj.resize((width,int(formatted_height)), Image.ANTIALIAS)
        img.save(self.image)