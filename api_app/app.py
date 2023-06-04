from flask import Flask, request, jsonify

app = Flask(__name__)


def get_character_count(word, character):
    """
    This function gets the count of character in the given word 
    Parameters:
    word (str): word which contains characters.
    character (str): character count to be calculated.

    Returns:
    int: count of the character in given word.
    """
    count = 0
    for char in word:
        if char == character:
            count += 1
    return count


def get_character_indices(text, character):
    """
    This function gets the index postions of the character in given word
    Parameters:
    text (str): Description of the first argument.
    character (str): Description of the second argument.

    Returns:
    list: gives count and index positions of the character in the word. 
    count at list[0] position and other are index postions of the characters
    """
    indices = []
    indices.append(get_character_count(text, character))
    for i in range(len(text)):
        if text[i] == character:
            indices.append(i+1)
    return indices


def encode_word(text):
    """
    This function encodes the word with the given encoding pattern
    Parameters:
    text (str): text which is to be encoded.

    Returns:
    str: encoded string will be returned.
    """
    dict_char = {}
    string = ""
    for char in text:
        dict_char[char] = get_character_indices(text, char)
    for char, indices in dict_char.items():
        for value in indices:
            if value == 10:
                string += '+'
            elif 20 > value > 10:
                val = value - 10
                string += '+' + str(val)
            elif 30 > value > 20:
                val = value - 20
                string += '-' + str(val)
            elif 40 > value > 30:
                val = value - 30
                string += '*' + str(val)
            elif 50 > value > 40:
                val = value - 40
                string += '/' + str(val)
            else:
                string += str(value)
        string += char
    return string


def encode_text(input_text):
    """
    This function encodes the text.

    Parameters:
    input_text (str): Text is provided to encode.

    Returns:
    str: encoded text will be returned .
    """
    encoded_word_lst = []
    for word in input_text.split():
        encoded_word = encode_word(word)
        encoded_word_lst.append(encoded_word)
    encoded_text = '?'.join(encoded_word_lst)
    return encoded_text


def seperate_integer_index(encoded_word_index):
    """
    This function gets the indexes of the character from encoded integer string.

    Parameters:
    encoded_word_index (str): Encoded integer string of index positions.

    Returns:
    list: list of index positions of characters.
    """
    index_position_of_char = []
    ind = 0
    flag = False
    values_dict = {'+':10,'-':20,'*':30, '/':40}
    values_list = ['+','-','*','/']
    for count in range(len(encoded_word_index[:])):
        char = encoded_word_index[count]
        if char in values_list:
            try:
                encoded_word_index[count+1]
            except IndexError:
                ind += values_dict[char]
                index_position_of_char.append(ind)
                ind = 0
                flag = False
            if flag:
                index_position_of_char.append(ind)
                ind = values_dict[char]
                flag = False
                continue
            else:
                ind += values_dict[char]
                flag = True
            continue
        ind += int(char)
        index_position_of_char.append(ind)
        ind = 0
        flag = False
    return index_position_of_char


def separate_integer_characters(text):
    """
    This function seperates the characters and encoded index position text and return in the form of dictionary.

    Parameters:
    encoded_word (str): The encoded text word.

    Returns:
    dict: returns dict with character as key and list of index positions as values.

    """
    start_ind = 0
    end_ind = 0
    str_dict = {}

    for count in range(len(text)):
        if text[count].isalpha():
            end_ind = count
            index_position = seperate_integer_index((text[start_ind:end_ind]))
            str_dict[text[count]] = index_position
            start_ind = end_ind + 1
    return str_dict


def get_decoded_word(word_dict):
    """
    This function decodes the provided encoded word in the form of dict.
    Parameters:
    word_dict (dict): dict contains characters as key and list of index positions as values.

    Returns:
    str: returns the decoded word.

    Additional details or examples can be included here.
    """
    word_length = 0
    for char, values in word_dict.items():
        word_length += values[0]
    word = []
    for i in range(word_length):
        word.append('*')
    for char, values in word_dict.items():
        for value in values[1:]:
            word[value-1] = char
    decoded_word = ''.join(word)
    return decoded_word


def decode_text(encoded_text):
    """
    This function decodes the given encoded text and returns it.
    Parameters:
    encoded_text (str): Encoded text.

    Returns:
    str: Decoded text of provided encoded text.
    """
    decoded_word_list = []
    encoded_words_list = encoded_text.split('?')
    for word in encoded_words_list:
        decoded_word_dict = separate_integer_characters(word)
        decoded_word = get_decoded_word(decoded_word_dict)
        decoded_word_list.append(decoded_word)
    decoded_text = ' '.join(decoded_word_list)
    return decoded_text


@app.route('/encode/', methods=['POST'])
def encode_endpoint():
    data = request.get_json()
    text = data['text']

    encoded_text = encode_text(text)

    return jsonify({'encoded_text': encoded_text})


@app.route('/decode/', methods=['POST'])
def decode_endpoint():
    data = request.get_json()
    encoded_text = data['encoded_text']

    decoded_text = decode_text(encoded_text)

    return jsonify({'decoded_text': decoded_text})


if __name__ == '__main__':
    app.run()
