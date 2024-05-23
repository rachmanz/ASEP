from hdfs import InsecureClient


NAMENODE = "localhost"
PORT = "8080"

class HadoopDataUploader:
    def __init__(self, namenode, port, username):
        self.client = InsecureClient(f'http://{NAMENODE}:{PORT}', user="khirtz")

    def upload_file(self, local_file_path, hdfs_file_path):
        self.client.upload(hdfs_file_path, local_file_path)
        print(f"File uploaded to HDFS: {hdfs_file_path}")

# Example usage:
uploader = HadoopDataUploader('<namenode>', '<port>', '<username>')
uploader.upload_file('/path/to/local/file.txt', '/path/to/hdfs/file.txt')