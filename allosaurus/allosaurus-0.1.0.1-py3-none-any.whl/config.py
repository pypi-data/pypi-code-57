import argparse

def create_allosaurus_parser():

    parser = argparse.ArgumentParser('Phone recognizer')
    parser.add_argument('--device_id', type=int, default=-1, help='specify cuda device id to use, -1 means no cuda and will use cpu for inference')
    parser.add_argument('--model', type=str, default='latest', help='specify which model to use. default is to use the latest model')
    parser.add_argument('--lang_id', type=str, default='ipa',help='specify which language inventory to use for recognition. default is to use all phone inventory')

    return parser

def create_allosaurus_config():
    parser = create_allosaurus_parser()
    args = parser.parse_args()

    return args