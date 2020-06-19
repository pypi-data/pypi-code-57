from distutils.core import setup
setup(
  name = 'piServo',         # How you named your package folder (MyLib)
  packages = ['piServo'],   # Chose the same as "name"
  version = '1.8',      # Start with a small number and increase it with every change you make
  license = 'MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Control Servos with python !',   # Give a short description about your library
  long_description = """ Control servos with python !\n\n
                         Example to run a servo connected to pin 3 at angle 90:\n\n
                            RPI.GPIO as GPIO\n
                           import piServo\n
                           servo = piServo.Servo(3)\n
                           servo.initServo()\n
                           servo.setAngle(90)\n
                           servo.stopServo()\n
                           GPIO.cleanup()\n
                           \n\n
                         Use the stopServo() function at the end of your code or before GPIO.cleanup()""",
  author = 'Rushan SJ',                   # Type in your name
  author_email = 'shanrsjmax@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/rushan7750/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rushan7750/piServo/archive/master.zip',    # I explain this later on
  keywords = ['Raspberry Pi', 'Servo', 'Python'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'RPi.GPIO',
          'pyfiglet',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)