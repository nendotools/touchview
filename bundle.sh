bundle ()
{
    local dest dir
    dest="bin"
    dir="bin/touchview"
    mkdir -p "$dir"
    cp "__init__.py" "$dir"
    cp "preferences.py" "$dir"
    cp -r "source" "$dir"
    cd "$dest"
    zip -r "touchview.zip" "touchview"
    cd ".."
    rm -rf "$dir"
}

bundle
