import os


def list_files_in_folder(folder_path):
    file_list = []
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_list.append(file_name)
    else:
        print("Folder not found.")

    return file_list


folder_path = './Audio_Records'
files_list = list_files_in_folder(folder_path)
print("Files in the folder:", files_list)
