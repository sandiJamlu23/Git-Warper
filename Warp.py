import sys
import subprocess
import json

class Translate(object):
    def user_input(self, prompt):
        '''
        # bahasa_to_eng = {'komit':'commit',
                          'menarik':'pull',
                          'mendorong': 'push',
                          'status':'status'}
        '''
        bahasa_to_english = None
        path = 'E:/Github Indo Wrapper/cmd.json'
        with open(path, 'r', encoding='utf-8') as f:
            translation = json.load(f)

        # Do a case-insensitive lookup so user can type any case
        for key, val in translation.items():
            if key.lower() == prompt.lower():
                bahasa_to_english = val
                break

        if bahasa_to_english is None:
            print("Perintah git tidak ditemukan")

        return bahasa_to_english
    
    def run_git_command(self, command):
        '''Basic idea
            To run a command like: git pull
            subprocess.run(['git', 'pull'])             
        '''
        res = None

        if isinstance(command, str) and command.lower() in ('komit', 'commit'):
            subprocess.run(['git', 'add', '.'], capture_output=True, text=True, check=True)

            comment = input('Masukkan pesan komit: ').strip()
            if not comment:
                print("Pesan komit tidak boleh kosong.")
                return

            commit_res = subprocess.run(['git', 'commit', '-m', comment], capture_output=True, text=True)
            print(commit_res.stdout or commit_res.stderr)

            res = subprocess.run(['git', 'push'], capture_output=True, text=True)
            print(res.stdout or res.stderr)

        else: 
            cmd = ['git',command]
            res = subprocess.run(cmd,capture_output=False, text=True)

        return res
        
    def handle_git_err(self, res):
        stderr = ''
        if res and res.stderr:
            stderr = res.stderr.lower()

        # 1️⃣ Missing remote repo
        if "no configured push destination" in stderr:
            url = input('Paste remote URL: ')
            subprocess.run(['git', 'remote', 'add', 'origin', url],
                        capture_output=True, text=True)
            res = subprocess.run(['git', 'push', '-u', 'origin', 'main'],
                                capture_output=True, text=True)
            return res

        # 2️⃣ No upstream branch
        if 'current branch main has no upstream branch' in stderr:
            res = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'],
                                capture_output=True, text=True)
            return res

        # 3️⃣ Author identity missing
        if 'author identity unknown' in stderr:
            email = input('Enter github email (you@example.com): ')
            name = input('Your Name: ')

            subprocess.run(['git', 'config', '--global', 'user.email', email],
                        check=True, text=True)
            subprocess.run(['git', 'config', '--global', 'user.name', name],
                        check=True, text=True)
            
            # Try the previous command again (optional, but cleaner)
            print("✅ Git identity set. Retrying your last command...")
            retry = subprocess.run(res.args, capture_output=True, text=True)
            
            return retry

        # If nothing matched, just return the original result
        return res

if __name__ == '__main__':
    translate = Translate()
    command = sys.argv[1]
    bahasa_to_english = translate.user_input(command)
    if not bahasa_to_english:
        sys.exit(1)
    # print(bahasa_to_english)
    # run_cmd = Translate.run_git_command(bahasa_to_english)
    run_cmd = translate.run_git_command(bahasa_to_english)
    run_cmd_err = translate.handle_git_err(run_cmd)
    print(run_cmd_err)
