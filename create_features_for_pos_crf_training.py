"""Create features for training POS CRF model from CoNLL or SSF annotated data."""
from argparse import ArgumentParser
import os
from re import findall
from re import DOTALL

# input is the folder containing the CONLL or SSF files


def read_text_from_file(file_path):
    '''
    Read text from a file using a file path.

    :param file_path: File path of an input file

    :return text: Returns text read from file
    '''
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.read().strip()


def find_sentences_from_ssf_text(text):
    '''
    Find all the sentences from text annotated in SSF format.

    :param text: Text with SSF annotations

    :return sentences: Returns sentences extracted from SSF text
    '''
    sentence_pattern = '<Sentence id=.*?>\n(.*?)\n</Sentence>'
    return findall(sentence_pattern, text, DOTALL)


def read_lines_from_file(file_path):
    '''
    Read lines from a file.
    
    :param file_path: Path of the input file

    :return lines: Returns lines read from the file
    '''
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.readlines()


def find_sentences_from_conll_text(lines):
    '''
    Find sentences in conll text.

    :param lines: Lines in conll format
    
    :return sentences: Sentences in conll format
    '''
    temp_tokens, sentences = [], []
    for line in lines:
        line = line.strip()
        if line:
            temp_tokens.append(line)
        else:
            if temp_tokens:
                temp_sentence = '\n'.join(temp_tokens)
                sentences.append(temp_sentence)
            temp_tokens = []
            temp_sentence = ''
    if temp_tokens:
        temp_sentence = '\n'.join(temp_tokens)
        sentences.append(temp_sentence)
        temp_tokens = []
        temp_sentence = ''
    print(len(sentences))
    return sentences


def read_file_and_find_features_from_sentences(file_path, data_type='conll'):
    '''
    Read a file and find features from sentences.
    
    :param file_path: File path of an input file

    :return features_string: Features for POS to train a CRF model.
    '''
    features_string = ''
    if data_type == 'conll':
        lines = read_lines_from_file(file_path)
        sentences_found = find_sentences_from_conll_text(lines)
    else:
        text = read_text_from_file(file_path)
        sentences_found = find_sentences_from_ssf_text(text)
    features_string = find_features_from_sentences(sentences_found, data_type)
    return features_string


def find_features_from_sentences(sentences, data_type='conll'):
    '''
    Find features from sentences.

    :param sentences: Sentences read from file

    :return features: Features of all tokens for each sentence combined for all the sentences
    '''
    prefix_len = 4
    suffix_len = 7
    features = ''
    for sentence in sentences:
        sentence_features = ''
        for line in sentence.split('\n'):
            if line:
                line_split = line.split('\t')
                if data_type == 'conll':
                    token = line_split[0]
                    tag = line_split[-1]
                else:
                    token = line_split[1]
                    tag = line_split[2]
                sentence_features += token + '\t'
                for i in range(1, prefix_len + 1):
                    sentence_features += affix_feats(token, i, 0) + '\t'
                for i in range(1, suffix_len + 1):
                    sentence_features += affix_feats(token, i, 1) + '\t'
                sentence_features = sentence_features + 'LESS\t' if len(token) <= 4 else sentence_features + 'MORE\t'
                sentence_features += tag.replace('__', '_').replace('-', '_') + '\n'
        if sentence_features.strip():
            features += sentence_features + '\n'
    return features


def affix_feats(token, length, type_aff):
    '''
    Find features with affixes.

    :param line: extract the token and its corresponding suffix list depending on its length
    :param token: the token in the line
    :param length: length of affix
    :param type: 0 for prefix and 1 for suffix

    :return affix_features: returns the affix features
    '''
    if len(token) < length:
        return 'NULL'
    else:
        if type_aff == 0:
            return token[:length]
        else:
            return token[len(token) - length:]


def write_text_to_file(text, file_path):
    '''
    Write text to file.

    :param text: Text to be written
    :param file_path: File path of the output file
    :return: None
    '''
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write(text + '\n')


def main():
    '''
    Pass arguments and call functions here.

    :param: None
    :return: None
    '''
    parser = ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--output', dest='out', help="Add the output file where the features will be saved")
    parser.add_argument('--type', dest='type', help="Add the type of the data either ssf or conll")
    args = parser.parse_args()
    print(args.type)
    if not os.path.isdir(args.inp):
        features_extracted = read_file_and_find_features_from_sentences(args.inp, args.type)
        write_text_to_file(features_extracted, args.out)
    else:
        all_features = ''
        for root, dirs, files in os.walk(args.inp):
            for fl in files:
                input_path = os.path.join(root, fl)
                features_extracted = read_file_and_find_features_from_sentences(input_path, args.type)
                all_features += features_extracted
            write_text_to_file(all_features, args.out)


if __name__ == '__main__':
    main()
