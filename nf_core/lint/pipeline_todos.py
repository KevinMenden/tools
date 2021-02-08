#!/usr/bin/env python

import os
import io
import fnmatch


def pipeline_todos(self):
    """Check for nf-core *TODO* lines.

    The nf-core workflow template contains a number of comment lines to help developers
    of new pipelines know where they need to edit files and add content.
    They typically have the following format:

    .. code-block:: groovy

        // TODO nf-core: Make some kind of change to the workflow here

    ..or in markdown:

    .. code-block:: html

        <!-- TODO nf-core: Add some detail to the docs here -->

    This lint test runs through all files in the pipeline and searches for these lines.
    If any are found they will throw a warning.

    .. tip:: Note that many GUI code editors have plugins to list all instances of *TODO*
              in a given project directory. This is a very quick and convenient way to get
              started on your pipeline!
    """
    passed = []
    warned = []
    failed = []

    ignore = [".git"]
    if os.path.isfile(os.path.join(self.wf_path, ".gitignore")):
        with io.open(os.path.join(self.wf_path, ".gitignore"), "rt", encoding="latin1") as fh:
            for l in fh:
                ignore.append(os.path.basename(l.strip().rstrip("/")))
    for root, dirs, files in os.walk(self.wf_path):
        # Ignore files
        for i in ignore:
            dirs = [d for d in dirs if not fnmatch.fnmatch(os.path.join(root, d), i)]
            files = [f for f in files if not fnmatch.fnmatch(os.path.join(root, f), i)]
        for fname in files:
            with io.open(os.path.join(root, fname), "rt", encoding="latin1") as fh:
                for l in fh:
                    if "TODO nf-core" in l:
                        l = (
                            l.replace("<!--", "")
                            .replace("-->", "")
                            .replace("# TODO nf-core: ", "")
                            .replace("// TODO nf-core: ", "")
                            .replace("TODO nf-core: ", "")
                            .strip()
                        )
                        warned.append("TODO string in `{}`: _{}_".format(fname, l))

    return {"passed": passed, "warned": warned, "failed": failed}
