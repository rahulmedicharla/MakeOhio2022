import os
PATH = 'assets'

def deleteAllButMostRecentFiles():
    os.chdir("c:/Users/rmedi/OneDrive/Documents/Make Ohio/python")
    
    if len(os.listdir(PATH)) < 3:
        return

    skip = True
    for f in os.listdir(PATH):
        if skip:
            skip = False
            continue
        os.remove(os.path.join(PATH, f))

    for f in os.listdir(PATH):
        if f != 'img.jpg':
            os.rename(os.path.join(PATH, f), os.path.join(PATH, 'img.jpg'))
            break

if __name__ == '__main__':
    deleteAllButMostRecentFiles()