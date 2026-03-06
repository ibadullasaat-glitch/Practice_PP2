import os
os.makedirs("folder1/folder2/folder3", exist_ok=True)


files1 = os.listdir("folder1")
print(files1)
files2 = os.listdir("folder1/folder2")
print(files2)
files3 = os.listdir("folder1/folder2/folder3")
print(files3)


from pathlib import Path
for file in Path("Practice_PP2\\folder1").rglob("*.txt"):
    print(file)