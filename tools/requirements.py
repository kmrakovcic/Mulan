def create_requrements_file():
    # Create requirements.txt file
    import os
    old_path = os.getcwd()
    os.chdir('..')
    new_path = os.getcwd()
    os.chdir(old_path)
    os.system('pip install pipreqs --upgrade')
    #os.mkdirs(new_path + '/requirements.txt', exist_ok=True)
    os.system('pipreqs ' + new_path+' --force')


def install_requrements():
    # Install requirements.txt file
    import os
    old_path = os.getcwd()
    os.chdir('..')
    new_path = os.getcwd()
    os.chdir(old_path)
    os.system('pip install -r ' + new_path + '/requirements.txt')


if __name__ == '__main__':
    create_requrements_file()