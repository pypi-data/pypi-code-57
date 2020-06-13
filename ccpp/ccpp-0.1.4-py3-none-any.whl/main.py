import fire

from .generate import generate_tmpl


class Commands:

    def new(self, repo):
        generate_tmpl(repo)


def main():
    fire.Fire(Commands)


if __name__ == "__main__":
    main()
