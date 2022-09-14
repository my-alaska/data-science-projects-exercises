import os
import string

import zipfile
from collections import defaultdict
import pandas as pd

input_dir = 'berg_input'
output_dir = 'berg_output'


def unzip_read(f_name):
    with zipfile.ZipFile(input_dir + '\\' + f_name, 'r') as zip_ref:
        text_ = zip_ref.read(f_name[:-4] + '.txt', )
    return text_


translator = str.maketrans('', '', string.punctuation + '0123456789')


def text_to_words(text):
    text = text.translate(translator).lower().split()

    unique_words = defaultdict(lambda: 0)
    for word in text:
        unique_words[word] += 1

    sorted_words = sorted(list(unique_words.items()), key=lambda x: x[1], reverse=True)

    words_df = pd.DataFrame(sorted_words, columns=['Words', 'Occurences'])
    words_df['Words'] = words_df['Words'].astype('string')

    words_df['Length'] = words_df['Words'].str.len()

    return words_df


def words_to_params(words_df):
    no_words = words_df.shape[0]

    text_length = words_df['Occurences'].sum()

    repetition_tendency = words_df['Occurences'].mean() / words_df['Occurences'].sum()

    max_word_length = words_df['Length'].max()

    instances = words_df['Length']
    occurences = words_df['Length'].loc[words_df.index.repeat(words_df['Occurences'])].reset_index(drop=True)

    inst_mean, inst_var = instances.mean(), instances.var()
    occur_mean, occur_var = occurences.mean(), occurences.var()

    return no_words, text_length, repetition_tendency, max_word_length, inst_mean, inst_var, occur_mean, occur_var


month_dict = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}


def get_book_info(text, title, author, release_date):
    params = words_to_params(text_to_words(text))
    # no_words = params[0]  # number of distinct words
    # text_length = params[1]  # number of all words in the text
    # repetition_tendency = params[2]  # average word length divided by the length of text in number of words
    # max_word_length = params[3]  # self explanatory
    # inst_mean = params[4]  # average length of a word that appear at least once in the text
    # inst_var = params[5]  # length variance like above
    # occur_mean = params[6]  # average word length of the text
    # occur_var = params[7]  # length variance like above
    split = release_date.find("[")
    release_date = release_date[:split]
    split = release_date.find(" ")
    month = month_dict[release_date[:split].lower()]
    release_date = release_date[split+1:]
    split = release_date.find(",")
    day = str(release_date[:split])
    year = int(release_date[split+1:])
    book_info = [title,author,day,month,year]
    book_info.extend(params)

    return book_info


df = []

for file_name in os.listdir('berg_input'):
    print(len('Character set encoding: '))
    text = unzip_read(file_name)
    title, author, release_date, encoding = None, None, None, None
    for line in text.splitlines():
        if line[:7] == b'Title: ':
            title = str(line[7:], 'UTF-8')
            print(title)
        elif line[:8] == b'Author: ':
            author = str(line[8:], 'UTF-8')
            print(author)
        elif line[:14] == b'Release Date: ':
            release_date = str(line[14:], 'UTF-8')
            print(release_date)
        elif line[:24] == b'Character set encoding: ':
            encoding = str(line[24:], 'UTF-8')
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

    text = text[start:end + 1]

    df_entry = get_book_info(text, title, author, release_date)

    df.append(df_entry)

df = pd.DataFrame(df,columns=['title','author','day','month','year','no_words_distinct', 'no_words', 'repeat_tend',
                              'max_w_len', 'sing_mean', 'sing_var', 'multi_mean', 'multi_var'])

df.to_csv('book_info.csv')
