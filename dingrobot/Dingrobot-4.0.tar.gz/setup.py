from setuptools import setup, find_packages
setup(
    name = "Dingrobot",
    version = "4.0",
    description = "Dingrobot control",
    long_description = "This packet is Ding Talk(https://www.dingtalk.com/) custom robot control,can be very conveniently controlled the Ding Talk's custom robot,but only support endorsement.\n"
                       "Several basic methods are provided in the package to control the Ding Talk's custom robot,create a robot class, and enter the robot's token (in the robot's url), then you can start manipulating the robot!\n"
                       "For example, robot.send_text(content, @ Who (default is False)) you can let the robot send the basic text!\n"
                       "There is still a lot of content left for you to explore!",
    author = "WangZiPeng",
    author_email = "3357223099@qq.com",
    packages = find_packages(),
    platforms = "any",
    install_requires = ["requests"],
)