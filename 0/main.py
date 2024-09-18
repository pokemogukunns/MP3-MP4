import subprocess

def run_node_script(url, zip_file_name='downloaded_page'):
    try:
        # Node.jsスクリプトを実行する
        subprocess.run(['node', 'savePageToZip.js', url, zip_file_name], check=True)
        print(f'Successfully saved page and resources to {zip_file_name}.zip')
    except subprocess.CalledProcessError as e:
        print(f'Error executing Node.js script: {e}')

# 使用例
url = 'https://example.com'
zip_file_name = 'my_page'
run_node_script(url, zip_file_name)
