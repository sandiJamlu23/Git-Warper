import subprocess

subprocess.run(['git','add','.'])
comment = input('masukkan  pesan...')
print(f'Pesan anda {comment}')