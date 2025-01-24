import sys
import collections
import hashlib
import pathlib
import shutil


def main(args=sys.argv[1:]):
    destination_dir_name = args[0] if args else "EXTRA_DUPLICATES"

    destination_root = pathlib.Path(destination_dir_name)

    file_paths_and_mtimes = collections.defaultdict(list)

    file_paths = [path for path in pathlib.Path.cwd().iterdir() if path.is_file()]

    print_every = min(50, len(file_paths) // 10)

    for i, path in enumerate(file_paths, start=1):
        if i % print_every == 0:
            print(f"Hash digest calculated for ({i}/{len(file_paths)}) files. ")
        with path.open("rb") as f:
            digest = hashlib.file_digest(f, "sha256")
        file_paths_and_mtimes[digest.hexdigest()].append((path, path.stat().st_mtime))

    for hex_digest, files_and_mtimes in file_paths_and_mtimes.items():
        files_and_mtimes.sort(lambda tuple_: tuple_[1])

        destination = destination_root / hex_digest
        destination.mkdir(parents=True, exist_ok=True)
        for i, (file_path, mtime) in enumerate(files_and_mtimes[1:-1], start=1):
            shutil.move(file_path, destination)
        print(f"Moved {i} file(s) to {destination}")


if __name__ == "__main__":
    main()
