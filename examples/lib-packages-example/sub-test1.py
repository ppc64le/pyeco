import lame, pkg_resources
def get_version(module_name, module=None):
    # Try to get version from common attributes if module is provided
    if module:
        for attr in ('__version__', 'version', 'VERSION'):
            version = getattr(module, attr, None)
            if version:
                if callable(version):
                    try:
                        return version()
                    except Exception:
                        continue
                return version

    # Fallback: try pkg_resources by module_name
    try:
        return pkg_resources.get_distribution(module_name).version
    except Exception:
        return "unknown"

def test_lame_package_basic():
    print("lame module:", lame)

    # Check for common metadata
    version = get_version("lame", lame)
    if version:
        print(f"lame.__version__: {version}")
    else:
        print("lame.__version__ not found")

    # List attributes
    attrs = dir(lame)
    print(f"Attributes in lame module ({len(attrs)}):")
    print(attrs)

    # Try calling anything callable without arguments (risky, just test)
    for attr_name in attrs:
        attr = getattr(lame, attr_name)
        if callable(attr):
            print(f"Trying to call callable: lame.{attr_name}()")
            try:
                result = attr()
                print(f"  Success, returned: {result}")
            except Exception as e:
                print(f"  Failed with exception: {e}")
            break  # Just test first callable

if __name__ == "__main__":
    test_lame_package_basic()
