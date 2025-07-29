import os
import glob


def clear_txt_files_simple(directory_path):
   for file_path in glob.glob(os.path.join(directory_path, "*.txt")):
      open(file_path, 'w').close()


def main():
   path = 'E:/ShilingTech/Dataset/fishtale/labels/'
   clear_txt_files_simple(path)


if __name__ == '__main__':
    main()