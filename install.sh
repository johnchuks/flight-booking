#!/bin/bash

set -e
set -o pipefail
set -x

#install packages and write to requirements.txt

for pkg in $@; do
    pip install "$pkg" && {
        name="$(pip show "$pkg" | grep Name: | awk '{print $2}')";
        version="$(pip show "$pkg" | grep Version: | awk '{print $2}')";
        echo "${name}==${version}" >> requirements.txt;
    }
done

exit 0
