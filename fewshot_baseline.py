# @Author: JY HUA
# @Date: 20220923
# @Description: 小样本数据分类任务
# @比赛链接: https://www.datafountain.cn/competitions/582
import torch
from transformers import Trainer, TrainingArguments, DefaultFlowCallback, AdamW, get_constant_schedule
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pandas as pd
from tqdm import tqdm
import json
def read_json(input_file):
    """Reads a json list file."""
    with open(input_file, "r") as f:
        reader = f.readlines()
    return [json.loads(line.strip()) for line in reader]
# 1、加载模型 & tokenizer
from transformers import BertTokenizerFast, BertForSequenceClassification
model = BertForSequenceClassification.from_pretrained('Langboat/mengzi-bert-base', num_labels=36)
tokenizer = BertTokenizerFast.from_pretrained('Langboat/mengzi-bert-base')
# 2、加载训练数据
df = pd.DataFrame.from_records(read_json('data/train.json'))
df = df.sample(frac=1,random_state=42)
# 3、构建输入输出文本
# 参考了社区里其他同学构建input的形式
df['input_string'] = df.apply(lambda x: f"这份专利的标题为：《{x.title}》，由“{x.assignee}”公司申请，详细说明如下：{x.abstract}",axis=1)
df = df[['input_string','label_id']]
# 4、划分 train dev 数据集
df_train, df_dev = train_test_split(df, test_size=0.2, random_state=42)
df_train = df_train.reset_index()
df_dev = df_dev.reset_index()
# 5、构建数据集
from torch.utils.data import Dataset
class BertDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.input_encodings = tokenizer([data.loc[i,'input_string'] for i in range(len(data))],
                                         max_length=512,
                                         truncation=True,
                                         padding=True)
        self.targets = data['label_id'].astype(int)
    def __len__(self):
        return len(self.targets)
    def __getitem__(self, index):
        return {
            'input_ids': torch.tensor(self.input_encodings['input_ids'][index]),
            'token_type_ids': torch.tensor(self.input_encodings['token_type_ids'][index]),
            'attention_mask': torch.tensor(self.input_encodings['attention_mask'][index]),
            'labels': torch.tensor(self.targets[index])
        }
train_dataset = BertDataset(df_train, tokenizer)
dev_dataset = BertDataset(df_dev, tokenizer)
# 6、模型训练
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    f1 = f1_score(labels, preds, average='macro')
    print('f1: ', f1)
    return {'f1': f1}
training_args = TrainingArguments(
    output_dir=f'./ckpts',
    num_train_epochs=25,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    per_device_eval_batch_size=32,   # 2*per_device_train_batch_size
    dataloader_num_workers=8,
    logging_dir=f'./logs',
    logging_steps=50,
    evaluation_strategy="steps",
    eval_steps=50,
    save_steps=50,
    fp16=False,
    save_total_limit=10,
    load_best_model_at_end=True,
    metric_for_best_model='f1',
    report_to=[],
)
optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=True)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset,
    optimizers= (optimizer, get_constant_schedule(optimizer, last_epoch=-1)),
    compute_metrics=compute_metrics
)
trainer.train()
trainer.save_model(f'./best_ckpt/')
# 7、inference
model = BertForSequenceClassification.from_pretrained('./best_ckpt/', num_labels=36)
model = model.to('cuda')
tokenizer = BertTokenizerFast.from_pretrained('Langboat/mengzi-bert-base')
df_test = pd.DataFrame.from_records(read_json('data/testA.json'))
df_test['input_string'] = df_test.apply(lambda x: f"这份专利的标题为：《{x.title}》，由“{x.assignee}”公司申请，详细说明如下：{x.abstract}",axis=1)
BATCH_SIZE = 6
total_batch_num = int(len(df_test)/BATCH_SIZE) + 1
outputs_list = []
for batch_num in tqdm(range(total_batch_num)):
    batch_input = df_test[batch_num*BATCH_SIZE:(batch_num+1)*BATCH_SIZE].reset_index(drop=True)
    if len(batch_input)==0:
        break
    tokens = tokenizer([batch_input.loc[i,'input_string'] for i in range(len(batch_input))],
                         return_tensors="pt",
                         max_length=512,
                         truncation=True,
                         padding=True).to('cuda')
    outputs = model(input_ids=tokens.input_ids,
                    attention_mask=tokens.attention_mask,
                    token_type_ids=tokens.token_type_ids)
    res_tmp = outputs['logits'].argmax(1).tolist()
    outputs_list.extend(res_tmp)
    del tokens, res_tmp
assert len(df_test) == len(outputs_list)
df_test['label'] = outputs_list
df_test['label'] = df_test['label'].apply(int)
df_test[['id','label']].to_csv('submit.csv',index=False)