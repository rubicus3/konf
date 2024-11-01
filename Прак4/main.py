import os


def get_git_objects(repository_path):
    # Получаем список всех объектов в репозитории
    raw_log = os.popen(f"git -C {repository_path} --no-pager log --pretty=format:\"%h\"").read()
    objects = raw_log.splitlines()
    return objects


def print_info(repository_path: str, objects: list):
    for object in objects:
        raw = os.popen(f"git -C {repository_path} cat-file -p {object}")
        print(raw.read())

def main():
    objects = get_git_objects("~/Проекты/Mini-chem")
    print_info("~/Проекты/Mini-chem", objects)


if __name__ == "__main__":
    main()
