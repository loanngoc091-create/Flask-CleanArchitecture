import os
import uuid

class FileStorageService:

    def __init__(self, storage_path="uploads"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def save_file(self, file):
        filename = f"{uuid.uuid4()}_{file.filename}"
        path = os.path.join(self.storage_path, filename)
        file.save(path)
        return path

    def delete_file(self, path):
        if os.path.exists(path):
            os.remove(path)
