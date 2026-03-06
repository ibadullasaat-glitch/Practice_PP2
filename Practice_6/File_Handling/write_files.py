with open("Practice_6/File_Handling/PP2.txt", "a") as f:
  f.write("Now the file has more content!")

with open("Practice_6/File_Handling/PP2.txt") as f:
  print(f.read())