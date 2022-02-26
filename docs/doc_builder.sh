#!/usr/bin/env sh

make html

shopt -s dotglob

support_language=('en' 'de')
for language in ${support_language[@]}
do
    make -e SPHINXOPTS="-D language='${language}'" -e BUILDDIR="./_build/html/${language}" html
    cp -r ./_build/html/${language}/html/* ./_build/html/${language}/
done

