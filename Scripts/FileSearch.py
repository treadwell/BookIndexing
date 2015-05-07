import os
import json

# files = []
# for f in os.listdir(working_dir):
#     if f.endswith(".pdf"):
#         files.append(f)

def locate_files(extension, path_to_library):
	'''Finds all files with specified extension in a defined path 
	and returns a list of tuples with paths and filenames'''

	search_list = []

	for root, dirs, files in os.walk(path_to_library):
	    for file in files:
	        if file.endswith(".pdf"):
				print root
				print file
				print(os.path.join(root, file))
				search_list.append((root, file))
	return search_list

if __name__ == "__main__":
	
	path_to_library = "/Users/kbrooks/Documents/Book indexing project/Test Library"
	extension = ".pdf"

	print locate_files(extension,path_to_library)
