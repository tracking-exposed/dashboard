import os
script_dir = os.path.dirname(__file__)

def add():
    name = input('Please, select a name for your new profile:\n_ ')
    print('\nThank you, this will be the name of your new configuration file: ' + name)
    rel_path = "../config/" + name
    file = os.path.join(script_dir, rel_path)

    with open(file, 'w+') as f:
        while True:
            try:
                id = input('\nPlease paste the unique id for your user: _ ')
                int(id, 16)
                if len(id) == 40:
                    break
                else:
                    print('Id should be 40 characters long. Please enter it again.\n')
            except ValueError:
                print('Id should contain only numbers and lowercase letters from a to f. Please enter it again.')
                continue
        f.write('# see README.md for more infos\n')
        f.write('--name ' + name + '\n')
        f.write('--id ' + id + '\n')
        print('\n                       Done! saving to \'' + file + '\'')
        print('\nRemember you can call scripts with this configuration file by using:')
        print('                     python3 script.py -c ' + file+'\n\n')

def main():
    print('Welcome to the fbtrex dashboard configuration setup script.')
    while True:
        c = input('Please pick one:\n1. Add a new profile\n\n_')
        if c == '1':
            add()
            break
        # elif c == '2':
        #     print('Pick one of the configurations to edit:\n')
        #     dr = script_dir+'config/'
        #     print(os.listdir(dr))
        #     break
        else:
            print('Invalid input, please try again.')
            continue


if __name__ == '__main__':
    main()
