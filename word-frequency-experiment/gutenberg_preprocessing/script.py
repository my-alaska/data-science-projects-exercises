import os

import zipfile

input_dir = 'berg_input'
output_dir = 'berg_output'

def unzip_read(f_name):
    with zipfile.ZipFile(input_dir + '\\' + f_name, 'r') as zip_ref:
        text_ = zip_ref.read(f_name[:-4]+'.txt',)
    return text_



for file_name in os.listdir('berg_input'):
    print(len('Character set encoding: '))
    text = unzip_read(file_name)
    title, author, release_date, encoding = None, None, None, None
    for line in text.splitlines():
        if line[:7] == b'Title: ':
            title = str(line[7:],'UTF-8')
            print(title)
        elif line[:8] == b'Author: ':
            author = str(line[8:],'UTF-8')
            print(author)
        elif line[:14] == b'Release Date: ':
            release_date = str(line[14:],'UTF-8')
            print(release_date)
        elif line[:24] == b'Character set encoding: ':
            encoding = str(line[24:],'UTF-8')
            print(encoding)
            break
    if title is None:
        title = "___"
    if author is None:
        author = "___"
    if release_date is None:
        release_date = "___"
    if encoding is None:
        encoding = 'UTF-8'

    text = str(text, encoding)

    start = text.find('START OF THIS PROJECT GUTENBERG EBOOK')
    end = text.find('END OF THIS PROJECT GUTENBERG EBOOK')

    while text[start] != '\n':
        start += 1
    while text[end] != '\n':
        end -= 1

    text = title + '\n' + author + '\n'+ release_date + '\n' + text[start:end+1]

    with open( output_dir + '\\' + file_name[:-4] + '.txt', 'w', encoding='UTF-8') as f:
        f.write(text)