#!/usr/bin/env python3
"""Entry program for the make.fun bounty "Sum up 24 November's world
news in one image" (news-image-20261124).

The image itself lives in this repository as news.png. This program
does one small, exact job: it copies that file byte for byte to the
grader's output location and checks the copy with SHA-256, so the two
runs the grader performs always produce identical bytes.

Standard library only. No network, no extra files read, no randomness.
"""

import hashlib
import os
import shutil
import sys

# SHA-256 of news.png as shipped in this repository. The program refuses
# to run if the file on disk does not match, so a damaged or swapped
# image can never be submitted silently.
EXPECTED_SHA256 = "6733b2296b239dc6270933f91b8c84de166ddd82e71829f85b8acf680047605b"

SOURCE_NAME = "news.png"
OUTPUT_NAME = "entry.png"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)

    before = sha256_file(source)
    if before != EXPECTED_SHA256:
        print("error: news.png fingerprint mismatch", file=sys.stderr)
        print("  expected: %s" % EXPECTED_SHA256, file=sys.stderr)
        print("  found:    %s" % before, file=sys.stderr)
        return 1

    shutil.copyfile(source, target)

    # Byte-for-byte means size as well as hash: check both before we
    # call the copy good. The run is deterministic by construction —
    # the same input file always yields the same output bytes.
    if os.path.getsize(source) != os.path.getsize(target):
        print("error: copied file size differs from news.png",
              file=sys.stderr)
        return 1

    after = sha256_file(target)
    if after != EXPECTED_SHA256:
        print("error: copied file fingerprint mismatch", file=sys.stderr)
        print("  expected: %s" % EXPECTED_SHA256, file=sys.stderr)
        print("  found:    %s" % after, file=sys.stderr)
        return 1

    print("wrote %s (%s)" % (target, after))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
