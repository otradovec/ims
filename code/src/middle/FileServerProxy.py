import random, os


class FileServerProxy:
    def save(self, contents: bytes, filename: str, comment_id: int):
        pseudo_rand_num = hash(hash(filename) + random.randint(-1000000000, 1000000000))
        path = os.path.join(os.getcwd(), "data_storage")
        if not os.path.exists(path):
            os.makedirs(path)
        name = "c" + str(comment_id) + "a" + str(pseudo_rand_num) + "_ims.data"
        path = os.path.join(path, name)
        with open(path, "wb") as file_destined:
            file_destined.write(contents)
        return path


    def delete(self, attachment_path):
        os.remove(attachment_path)

