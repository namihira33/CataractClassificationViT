data_root = '../medicaldata/images/CASIA2_16'

# 先生方によるラベル付与の分割データ
#train_info_list = '../medicaldata/txt/as_oct_train_preprocess.csv'
#test_info_list = '../medicaldata/txt/as_oct_test.csv'

# 12月発表時に使用したデータ
train_info_list = '../medicaldata/txt/casia16_train_list.csv'
test_info_list = '../medicaldata/txt/casia16_test_list.csv'

#pickleの位置
#normal_pkl = '../medicaldata/pkls/OCT_ViT_spin.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_P2_horizontal.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_P2_spin.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_N2_horizontal.pkl'
normal_pkl = '../medicaldata/pkls/OCT_N2_spin.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_ViT_horizontal_N3.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_N3_spin16to1.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_N3_horizontal_3ch.pkl' #N3クラス分類_水平
#normal_pkl = '../medicaldata/pkls/OCT_N3_horizontal_1ch_2.pkl' #N3クラス分類_水平
#normal_pkl = '../medicaldata/pkls/OCT_N3_N3_16to1.pkl' #N3クラス分類_回転
#normal_pkl = '../medicaldata/pkls/OCT_C2_horizontal.pkl'
#normal_pkl = '../medicaldata/pkls/OCT_C2_16to1spin.pkl'

#回転断面画像16枚を1ラベルに対応づけるpickleファイル
#spin16to1_pkl = '../medicaldata/pkls/OCT_P2_spin16.pkl'

MODEL_DIR_PATH = './model/'
LOG_DIR_PATH = './log/'
n_per_unit = 16
image_size = 224
n_class = 2

# train_info_list = '../medicaldata/txt/casia16_train_list.csv'
# test_info_list = '../medicaldata/txt/casia16_test_list.csv'