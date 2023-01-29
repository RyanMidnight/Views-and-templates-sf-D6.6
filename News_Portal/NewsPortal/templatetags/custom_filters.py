from django import template
from string import punctuation

register = template.Library()

SWEAR_WORDS = [
    'fuck',
    'Fuck',
    'fucking',
    'Fucking',
    'shit',
    'Shit',
    'Bitch',
    'bitch',
    'dick',
    'Dick',
    'tits',
    'Tits',
    'boobs',
    'Boobs',
    'faggot',
    'Faggot',
    'nigger',
    'Nigger',
    'radish',
    'Radish',
    'damn',
    'Damn',
    'Goddamn',
    'goddamn',
    'freak',
    'Freak',
    'slave',
    'Slave',
]


def punc(word):
    for symbol in punctuation:
        if symbol in word:
            return True
    else:
        return False


def substring(user_word):
    for swear_word in SWEAR_WORDS:
        if swear_word in user_word.lower():
            return True
    else:
        return False


@register.filter()
def censor(value):
    values_list = value.split(' ')
    new_word_list = []
    for word in values_list:
        if substring(word):
            if punc(word):
                new_word = word[0] + ((len(word) - 2) * '*') + word[-1]
                new_word_list.append(new_word)
            else:
                new_word = word[0] + ((len(word) - 1) * '*')
                new_word_list.append(new_word)
        else:
            new_word_list.append(word)
    new_value = ' '.join(new_word_list)
    return new_value
