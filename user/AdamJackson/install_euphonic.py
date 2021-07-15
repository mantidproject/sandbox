from packaging import version
import scipy
import subprocess
import sys

# Update pip, the version that ships with Ubuntu will insist on updating numpy
# to a version that may not be binary-compatible with Mantid
print("Updating Pip")
process = subprocess.run([sys.executable, "-m", "pip", "install",
                          "--user",
                          "pip"],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
print(process.stdout.decode('utf-8'))

if version.parse(scipy.version.version) < version.parse('1.0.0'):
    print(f"Scipy version is {scipy.version.version}, updating to 1.0.0")
    process = subprocess.run([sys.executable, "-m", "pip", "install",
                              "--user",
                              "scipy==1.0.0"],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    print(process.stdout.decode('utf-8'))

process = subprocess.run([sys.executable, "-m", "pip", "install",
                          "--user",
                          "euphonic"],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
print(process.stdout.decode('utf-8'))

print("Please restart Mantid in order to use the installed Euphonic library")
