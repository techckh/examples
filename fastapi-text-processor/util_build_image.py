from dotenv import load_dotenv
import os
import shutil


if __name__ == '__main__':

    load_dotenv()
    library_dir = os.getenv('LIBRARY_DIR', None)
    assert library_dir
    dst = 'temp/jp_tokenizer'
    print('src, %s' % library_dir)
    print('dst, %s' % dst)

    shutil.copytree(library_dir, dst)
    print('okay')
