import zipfile
from io import BytesIO
import sqlparse


def zipper(root_dir: str, objs_type: str, objs: dict) -> bytes:

    memory_str = BytesIO()
    zip_file = zipfile.ZipFile(memory_str, 'w', zipfile.ZIP_DEFLATED)

    for k, v in objs.items():
        zip_file.writestr('new_dwh/{0}/{1}/{2}.sql'.format(root_dir, objs_type, k), v)

    zip_file.close()

    return memory_str.getvalue()
