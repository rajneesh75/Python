import os
import pkg_resources

packages = {pkg.key: pkg.location for pkg in pkg_resources.working_set}

for pkg, path in packages.items():
    size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(path) for file in files)
    print(f"{pkg}: {size / (1024*1024):.2f} MB")