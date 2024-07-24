import os

if not os.path.isfile('.env'):
    print('Creating .env file...')
    with open('.env', 'w') as f:
        f.write('MONGODB_URI=mongodb+srv://user:password@server/\n')