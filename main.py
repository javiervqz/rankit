

def _print_welcome():
    print ('*'*50)
    print ('[C]rawl a Website\n') 
    print ('*'*50)

if __name__ == '__main__':
    _print_welcome()

    command = input().upper()

    if command == 'C':
        pass
    else:
        print('Invalid Command')
