from Controller_GCN import Trainer, Evaluator
import torch
import os
import joblib

info_dict = dict()
info_dict['numb_sample'] = None # training sample for 1 epoch
info_dict['numb_epoch'] = 100 # number of epoch
info_dict['numb_gcn_layers'] = 1 # number of gin layers to be stacked
info_dict['gcn_hidden_dim'] = [] # hidden layer in each gin layer
info_dict['gcn_output_dim'] = 1024
info_dict['gcn_input_dim'] = 2048
info_dict['batchnorm'] = True
info_dict['batch_size'] = 128
info_dict['dropout'] = 0.5
info_dict['visual_backbone'] = 'b5' # 'b0' or 'b4'
info_dict['visual_ft_dim'] = 2048
#info_dict['save_dir'] = '/home/hong01/Research/GraSim/Report'
info_dict['save_dir'] = '/home/nmduy/Graphs/GraSim/Report'
info_dict['optimizer'] = 'Adam' # or Adam
info_dict['learning_rate'] = 3e-4
info_dict['activate_fn'] = 'swish' # swish, relu, leakyrelu
info_dict['grad_clip'] = 2 # Gradient clipping
# info_dict['use_residual'] = False # always set it to false
# Embedder for each objects and predicates, embed graph only base on objects
info_dict['model_name'] = 'GCN_ObjAndPredShare_NoFtExModule_LSTM_i2t' 
info_dict['checkpoint'] = None #'/home/nmduy/Graphs/GraSim/Report/GCN_ObjAndPredShare_NoFtExModule_LSTM-15022021-014523.pth.tar'
info_dict['margin_matrix_loss'] = 0.35
info_dict['rnn_numb_layers'] = 2
info_dict['rnn_bidirectional'] = True
info_dict['rnn_structure'] = 'LSTM'
info_dict['graph_emb_dim'] = info_dict['gcn_output_dim']*2
info_dict['include_pred_ft'] = True # include visual predicate features or not
info_dict['freeze'] = False

def run_train(info_dict):
    if not os.path.exists(info_dict['save_dir']):
        print(f"Creating {info_dict['save_dir']} folder")
        os.makedirs(info_dict['save_dir'])
        
    trainer = Trainer(info_dict)
    trainer.train()

    subset = 'test'
    DATA_DIR = '/home/nmduy/Graphs/GraSim/OriginalData'
    DATA_IMG_DIR = '/home/nmduy/Graphs/GraSim/OriginalData'
    images_data = joblib.load(f"{DATA_IMG_DIR}/flickr30k_{subset}_lowered_images_data.joblib")
    caps_data = joblib.load(f"{DATA_DIR}/flickr30k_{subset}_lowered_caps_data.joblib")
    
    lossVal, ar_val, ari_val = trainer.validate_retrieval(images_data, caps_data, False)
    info_txt = f"\n----- SUMMARY (Matrix)-----\nLoss Val: {6-lossVal}"   
    info_txt = info_txt + f"\n[i2t] {round(ar_val[0], 4)} {round(ar_val[1], 4)} {round(ar_val[2], 4)}"
    info_txt = info_txt + f"\n[t2i] {round(ari_val[0], 4)} {round(ari_val[1], 4)} {round(ari_val[2], 4)}"
    print(info_txt)
    
    lossVal, ar_val, ari_val = trainer.validate_retrieval(images_data, caps_data, True)
    info_txt = f"\n----- SUMMARY (Combine)-----\nLoss Val: {6-lossVal}"   
    info_txt = info_txt + f"\n[i2t] {round(ar_val[0], 4)} {round(ar_val[1], 4)} {round(ar_val[2], 4)}"
    info_txt = info_txt + f"\n[t2i] {round(ari_val[0], 4)} {round(ari_val[1], 4)} {round(ari_val[2], 4)}"
    print(info_txt)
    
def run_evaluate(info_dict):
    info_dict['checkpoint'] = '/home/nmduy/Graphs/GraSim/Report/GCN_ObjAndPredShare_NoFtExModule_LSTM_Freeze-16022021-030527.pth.tar'

    evaluator = Evaluator(info_dict)
    evaluator.load_trained_model()
    
    subset = 'test'
    DATA_DIR = '/home/nmduy/Graphs/GraSim/OriginalData'
    DATA_IMG_DIR = '/home/nmduy/Graphs/GraSim/OriginalData'
    images_data = joblib.load(f"{DATA_IMG_DIR}/flickr30k_{subset}_lowered_images_data.joblib")
    caps_data = joblib.load(f"{DATA_DIR}/flickr30k_{subset}_lowered_caps_data.joblib")
    
#     lossVal, ar_val, ari_val = evaluator.validate_retrieval(images_data, caps_data, False)
#     info_txt = f"\n----- SUMMARY (Matrix)-----\nLoss Val: {6-lossVal}"   
#     info_txt = info_txt + f"\n[i2t] {round(ar_val[0], 4)} {round(ar_val[1], 4)} {round(ar_val[2], 4)}"
#     info_txt = info_txt + f"\n[t2i] {round(ari_val[0], 4)} {round(ari_val[1], 4)} {round(ari_val[2], 4)}"
#     print(info_txt)
    
    lossVal, ar_val, ari_val = evaluator.validate_retrieval(images_data, caps_data, True)
    info_txt = f"\n----- SUMMARY (Combine)-----\nLoss Val: {6-lossVal}"   
    info_txt = info_txt + f"\n[i2t] {round(ar_val[0], 4)} {round(ar_val[1], 4)} {round(ar_val[2], 4)}"
    info_txt = info_txt + f"\n[t2i] {round(ari_val[0], 4)} {round(ari_val[1], 4)} {round(ari_val[2], 4)}"
    print(info_txt)
    
#run_train(info_dict)
run_evaluate(info_dict)