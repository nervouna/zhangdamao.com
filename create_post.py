import os.path
from argparse import ArgumentParser

import pelicanconf


def parse_slug() -> None:
    parser = ArgumentParser(description="Create a new post.")
    parser.add_argument("slug", help="The slug of the post to create.")
    return parser.parse_args()


def create_empty_file(file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write("")


def assemble_path(slug: str) -> str:
    return os.path.join(
        pelicanconf.PATH,
        pelicanconf.ARTICLE_PATHS[0],
        slug + ".md",
    )


def create_post(slug: str) -> str:
    file_path = assemble_path(slug)
    create_empty_file(file_path)
    return os.path.abspath(file_path)


def main() -> None:
    args = parse_slug()
    created_file = create_post(args.slug)
    print(f"📝 Created {created_file}")


if __name__ == "__main__":
    main()
