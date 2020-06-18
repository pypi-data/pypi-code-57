import moviepy.editor
from PIL import Image, ImageStat
import argparse
import numpy as np

def main():
  ##### ARGPARSE SETUP #####
  parser = argparse.ArgumentParser(description="Takes a video File and creates an image with the average colors in stripes")
  parser.add_argument('input',help="String - Input filepath")
  parser.add_argument('--output', help="String - Output filename")
  parser.add_argument('--stripes', type=int ,help="Int - Number of stripes in Image")
  parser.add_argument('--dimensions', type=int ,nargs=2,help="Int Int - Width and height of final image")
  args = parser.parse_args()

  ##### FORMAT ARGUMENTS #####
  inputFile = args.input
  stripes = args.stripes if args.stripes else 100
  dimensions = args.dimensions if args.dimensions else (1920,1080)
  output = args.output if args.output else "output.png"

  ##### VARIABLE SETUP #####
  averageColors = []
  video = moviepy.editor.VideoFileClip(inputFile)
  interval = video.duration/stripes

  ##### FIND AVERAGE COLOR FOR ALL FRAMES #####
  for position in np.arange(interval, video.duration, interval):
    frame = video.get_frame(position)
    img = Image.fromarray(frame)
    stat = ImageStat.Stat(img)
    averageColors.append(stat.mean)

  stripeWidth = dimensions[0] / stripes

  ##### COMPOSE FINAL IMAGE #####
  final = Image.new('RGB',dimensions,0)
  for i,color in enumerate(averageColors):
    for x in np.arange(i*stripeWidth,(i+1)*stripeWidth):
      for y in np.arange(dimensions[1]):
        final.putpixel(tuple(map(int, [x,y])), tuple(map(int, color)))

  final.save(output)