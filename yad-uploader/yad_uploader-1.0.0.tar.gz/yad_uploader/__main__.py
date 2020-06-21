from yad_uploader import loggers, yad, arguments


def run():
    options = arguments.parse_args()
    if options.tg_token and options.tg_chats_id:
        loggers.setup(options)
    yad_client = yad.get_yad_client(options.yad_id, options.yad_password, options.yad_token)
    yad.upload_dir(yad_client, options.local_source_dir, options.yad_dest_dir)


if __name__ == '__main__':
    run()
