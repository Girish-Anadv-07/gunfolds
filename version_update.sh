python_file1="version.py"

version=$(grep "__version_info__ =" "$python_file1" | sed 's/.*\[\(.*\)\].*/\1/')
echo $version
sed -i -e "1s/s = .*/s = [$version]/" version_update.py
updated_version=$(python version_update.py)
echo $updated_version
sed -i -e "1s/__version_info__ = .*/__version_info__ = $updated_version/" version.py
