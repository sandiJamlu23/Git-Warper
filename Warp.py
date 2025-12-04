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
            try:
                subprocess.run(['git', 'add', '.'], capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                print('Gagal menambahkan perubahan:', e.stderr or e)
                return e

            comment = input('Masukkan pesan komit: ').strip()
            if not comment:
                print("Pesan komit tidak boleh kosong.")
                return

            commit_res = subprocess.run(['git', 'commit', '-m', comment], capture_output=True, text=True)
            print(commit_res.stdout or commit_res.stderr)

            # Try a plain push first
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
            # determine current branch
            br = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            branch = br.stdout.strip() or 'main'
            res = subprocess.run(['git', 'push', '-u', 'origin', branch],
                                capture_output=True, text=True)
            return res

        # 2️⃣ No upstream branch
        if 'no upstream' in stderr or 'has no upstream branch' in stderr:
            br = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            branch = br.stdout.strip() or 'main'
            res = subprocess.run(['git', 'push', '--set-upstream', 'origin', branch],
                                capture_output=True, text=True)
            return res

        # 3️⃣ Author identity missing
        if 'author identity unknown' in stderr or 'please tell me who you are' in stderr:
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

        # 4️⃣ Authentication / remote access issues
        if 'authentication failed' in stderr or 'unable to access' in stderr or 'could not read from remote repository' in stderr:
            print('Push failed due to authentication/remote access. Ensure your credentials or SSH keys are set up, or use a Personal Access Token for HTTPS.')
            return res

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
