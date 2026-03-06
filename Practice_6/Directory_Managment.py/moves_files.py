import shutil

shutil.move("folder1/folder2/folder3/file3.txt", "folder1")
shutil.move("folder1/folder2/file2.txt", "folder1/folder2/folder3")
shutil.move("folder1/file1.txt", "folder1/folder2")

files1 = os.listdir("folder1")
print(files1)
