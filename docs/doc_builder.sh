#!/usr/bin/env bash

make html

support_language=('en')
for language in ${support_language[@]}
do
    export BUILDDIR=./_build/html/${language}
    sphinx-intl update -p _build/gettext -l ${language}
    make -e SPHINXOPTS="-D language=\'${language}\'" -b html
    mv ./_build/html/${language}/html/* .[^\.]* ./_build/html/${language}/
done

