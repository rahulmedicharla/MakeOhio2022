import os

def deleteAllButMostRecentFiles(filepath):    
    if len(os.listdir(filepath)) < 3:
        return

    skip = True
    for f in os.listdir(filepath):
        if skip:
            skip = False
            continue
        os.remove(os.path.join(filepath, f))

    for f in os.listdir(filepath):
        if f != 'img.jpg':
            os.rename(os.path.join(filepath, f), os.path.join(filepath, 'img.jpg'))
            break

if __name__ == '__main__':
    deleteAllButMostRecentFiles()