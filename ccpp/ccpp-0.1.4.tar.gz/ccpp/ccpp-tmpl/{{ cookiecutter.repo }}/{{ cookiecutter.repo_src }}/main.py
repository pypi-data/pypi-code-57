import fire


class Commands:

    def hello(self):
        print("Hello, World! I'm {{ cookiecutter.user }}.")


def main():
    fire.Fire(Commands)


if __name__ == "__main__":
    main()