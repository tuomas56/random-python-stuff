#!/usr/bin/env python3

import markdown2
import settings
import argparse
import os

def bootstrap(path):
	pass

def convert(path, file):
	try:
		with open(file, "r") as f:
			file_text = f.read()
	except IOError:
		print("generate.py: error: file does not exist or cannot be opened!")
		return
	
	try:
		file_text = markdown2.markdown(file_text, extras=["tables","fenced-code-blocks","metadata"])
	except:
		print("generate.py: error: invalid markdown in file!")
		return

	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("command", help="command to execute.", choices=["new", "convert"])
	parser.add_argument("-p", "--path", help="path to write to.", default=os.getcwd())
	parser.add_argument("-f", "--file", help="file to convert.")
	args = parser.parse_args()
	if args.command == "new":
		bootstrap(args.path)
	elif args.command == "convert":
		if not args.file:
			parser.print_usage()
			print("generate.py: error: the following arguments are required: -f, --file")
			return
		convert(args.path, args.file)

if __name__ == "__main__":
	main()
