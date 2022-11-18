import re


NUMBERS_SEQ = (
    ('dieci', '10'),
    ('undici', '11'),
    ('dodici', '12'),
    ('tredici', '13'),
    ('quattordici', '14'),
    ('quindici', '15'),
    ('sedici', '16'),
    ('diciasette', '17'),
    ('diciotto', '18'),
    ('diciannove', '19'),
    ('venti', '20'),
    ('trenta', '30'),
    ('quaranta', '40'),
    ('cinquanta', '50'),
    ('sessanta', '60'),
    ('settanta', '70'),
    ('ottanta', '80'),
    ('novanta', '90'),
    ('cento', '100'),
    ('mille', '1000'), ('mila', '1000'),
    ('milione', '1000000'), ('milioni', '1000000'),
    ('miliardo', '1000000000'), ('miliardi', '1000000000'),
    ('uno', '1'), ('un', '1'),
    ('due', '2'),
    ('tre', '3'),
    ('quattro', '4'),
    ('cinque', '5'),
    ('sei', '6'),
    ('sette', '7'),
    ('otto', '8'),
    ('nove', '9'),
    )

NUMBERS = dict(NUMBERS_SEQ)

TOKEN_REGEX = re.compile('|'.join('(%s)' % num for num, val in NUMBERS_SEQ))


def normalize_text(num_repr):
    '''Return a normalized version of *num_repr* that can be passed to let2num.'''

    return num_repr.lower().translate(None, ' \t')


def let2num(num_repr):
    '''Yield the numeric representation of *num_repr*.'''

    result = ''

    for token in (tok for tok in TOKEN_REGEX.split(num_repr) if tok):
        try:
            value = NUMBERS[token]
        except KeyError:
            if token not in ('di', 'e'):
                raise ValueError('Invalid number representation: %r' % num_repr)
            continue

        if token == 'miliardi':
            result += '0'*9
        elif token in ('mila','milioni'):
            zeros = '0' * value.count('0')
            piece = result[-3:].lstrip('0')
            result = (result[:-len(piece)-len(zeros)] +
                      piece +
                      zeros)
        elif not result:
            result = value
        else:
            length = len(value)
            non_zero_values = len(value.strip('0'))
            if token in ('cento', 'milione', 'miliardo'):
                if result[-1] != '0':
                    result = (result[:-length] +
                              result[-1] +
                              '0' * value.count('0'))
                    continue
            result = (result[:-length] +
                      value.rstrip('0') +
                      result[len(result) -length + non_zero_values:])
    return add_thousand_separator(result)


def add_thousand_separator(s, sep='.'):
    '''Return the numeric string s with the thousand separator.'''

    rev_s = s[::-1]
    tokens = [rev_s[i:i+3][::-1] for i in range(0, len(s), 3)][::-1]
    return sep.join(tokens)