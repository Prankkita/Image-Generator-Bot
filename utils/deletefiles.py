import os

def delete_images_in_folder(folder_path):
    """
    Deletes all files in the specified folder.
    """
    try:
        # List all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Check if it's a file and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")
