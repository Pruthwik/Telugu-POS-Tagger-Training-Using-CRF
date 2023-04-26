# Telugu-POS-Tagger-Training-Using-CRF
Telugu-POS-Tagger-Training-Using-CRF with Non-CoNLL Data
# For this task, you need to run 2 python programs
## Step 1: To convert non CONLL (non column format) data into CONLL format
python convert_data_into_conll_format.py --input sample_telugu_pos_tagged_data_non_conll.txt --output sample_telugu_pos_tagged_data_conll.txt
## Step 2: Create features from CONLL data.
python create_features_for_pos_crf_training.py --input sample_telugu_pos_tagged_data_conll.txt --output sample_telugu_features_for_pos.txt --type conll
# Then, install CRF++ toolkit and train a CRF model
## How to train a crf using CRF++ toolkit (https://taku910.github.io/crfpp/), requires a template for reading features
crf_learn template_pos_4pre_7suff_5window sample_telugu_features_for_pos.txt model_sample_telugu.m
