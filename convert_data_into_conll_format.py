"""Convert data into conll format where each line contains the token and the pos separated by a tab."""
import os
import argparse


def read_lines_from_a_file(file_path):
    """Read lines from a file."""
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return [line.strip() for line in file_read.readlines() if line.strip()]


def read_files_from_folder_convert_into_conll_and_write(input_folder_path, output_folder_path):
    """Read files from a folder, convert the sentences in a file into conll, and write them into a folder."""
    for input_root, input_dirs, input_files in os.walk(input_folder_path):
        input_file_paths = [os.path.join(input_root, fl) for fl in input_files]
        output_file_paths = [os.path.join(output_folder_path, fl) for fl in input_files]
    for index_file, file_path in enumerate(input_file_paths):
        output_path = output_file_paths[index_file]
        read_file_convert_data_into_conll_and_write(file_path, out_path)


def read_file_convert_data_into_conll_and_write(input_file, output_file):
    """Read a file, convert its content into conll format, and write into another file."""
    lines_read = read_lines_from_a_file(input_file)
    conll_sentences = []
    print('File : ' + input_file)
    for index, line in enumerate(lines_read):
        temp_conll = []
        tokens_with_pos = line.split()
        for token_with_pos in tokens_with_pos:
            token_split = token_with_pos.split('\\')
            if len(token_split) != 2:
                print('Error in line number = ' + str(index + 1))
                print(line)
                print('For token : ' + token_with_pos)
                break
            else:
                token, pos = token_split
                temp_conll.append(token + '\t' + pos)
        if len(temp_conll) == len(tokens_with_pos):
            conll_sentence = '\n'.join(temp_conll)
            conll_sentences.append(conll_sentence + '\n')
            temp_conll = []
    write_list_to_file(conll_sentences, output_file)


def write_list_to_file(data_list, out_path):
    """Write list to a file."""
    with open(out_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(data_list) + '\n')


def main():
    """Pass arguments and call functions here."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help='Enter the input folder path')
    parser.add_argument('--output', dest='out', help='Enter the output file where data will be written in conll format')
    args = parser.parse_args()
    if os.path.isdir(args.inp):
        if not os.path.isdir(args.out):
            os.makedirs(args.out)
            read_files_from_folder_convert_into_conll_and_write(args.inp, args.out)
    else:
        read_file_convert_data_into_conll_and_write(args.inp, args.out)


if __name__ == '__main__':
    main()
