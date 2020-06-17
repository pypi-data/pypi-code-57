import setuptools
extensions = [setuptools.Extension("vk_audio.secondDecoderFunc",
                       ["src/Source.cpp"]
    )
]

setuptools.setup(
    name = "vk_audio",
    version = "1.1",
	packages=setuptools.find_packages(),
    py_modules = ["vk_api",'datetime'],
    author = "Superbespalevniy chel",
    author_email = "imartemy1@gmail.com",
    url = "https://vk.com/fesh_dragoziy",
    description = "Модуль для вызова методов аудио вк.",
    ext_modules = extensions    
)  