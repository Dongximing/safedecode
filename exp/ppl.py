import os
import gc
from math import exp
from typing import List
from tqdm import tqdm
import urllib
import json
import transformers
import torch
os.environ["OMP_NUM_THREADS"] = "1"  # to turn off warning message
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # to turn off warning message
PAD_TOKEN_LABEL_ID = torch.nn.CrossEntropyLoss().ignore_index
FORCE_RESET = bool(int(os.getenv("FORCE_RESET", "0")))

def internet_connection(host: str = 'http://google.com'):
    """ check if internet connection is available """
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
class PPL_Calculator:
    def __init__(self,
                 model: str = 'gpt2',
                 use_auth_token: bool = False,
                 max_length: int = None,
                 num_gpus: int = None,
                 torch_dtype=None,
                 device_map: str = None,
                 low_cpu_mem_usage: bool = False,
                 trust_remote_code: bool = True,
                 offload_folder: str = None,
                 hf_cache_dir: str = None):
        """ Language Model.

        @param model: Model alias or path to local model file.
        @param use_auth_token: Huggingface transformers argument of `use_auth_token`
        @param device: Device name to load the models.
        @param num_gpus: Number of gpus to be used.
        """

        # load model
        params = {"local_files_only": not internet_connection(), "use_auth_token": use_auth_token,
                  "trust_remote_code": trust_remote_code}
        if hf_cache_dir is not None:
            params["cache_dir"] = hf_cache_dir
        if offload_folder is not None:
            params["offload_folder"] = offload_folder
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model, **params)
        self.config = transformers.AutoConfig.from_pretrained(model, **params)

        params.update({"config": self.config, "low_cpu_mem_usage": low_cpu_mem_usage})
        if torch_dtype is not None:
            params['torch_dtype'] = torch_dtype
        if device_map is not None:
            params['device_map'] = device_map
        self.model = transformers.AutoModelForCausalLM.from_pretrained(model, **params)

        self.pad_token_initialized = False
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': "<<PAD>>"})
            self.model.resize_token_embeddings(len(self.tokenizer))
            self.pad_token_initialized = True

        if max_length is None:
            self.max_length = None
        else:
            self.max_length = max_length if max_length is not None else self.tokenizer.model_max_length
            assert self.max_length <= self.tokenizer.model_max_length, f"{self.max_length} > {self.tokenizer.model_max_length}"

        # loss function
        self.loss_fct = torch.nn.CrossEntropyLoss(reduction='none')

        # GPU setup
        self.device = self.model.device
        if device_map is None:
            num_gpus = torch.cuda.device_count() if num_gpus is None else num_gpus
            if num_gpus == 1:
                self.model.to('cuda')
                self.device = self.model.device
            elif num_gpus > 1:
                self.model = torch.nn.DataParallel(self.model)
                self.model.to('cuda')
                self.device = self.model.module.device
        self.model.eval()

    def get_perplexity(self, input_texts: str or List, batch: int = None):
        """ Compute the perplexity on recurrent LM.

        :param input_texts: A string or list of input texts for the encoder.
        :param batch: Batch size
        :return: A value or list of perplexity.
        """

        # batch preparation
        single_input = type(input_texts) == str
        input_texts = [input_texts] if single_input else input_texts
        batch = len(input_texts) if batch is None else batch
        batch_id = list(range(0, len(input_texts), batch)) + [len(input_texts)]
        batch_id = list(zip(batch_id[:-1], batch_id[1:]))

        loss_list = []
        with torch.no_grad():
            for s, e in batch_id:

                # run model inference
                if self.max_length is not None:
                    model_inputs = self.tokenizer(input_texts[s:e], max_length=self.max_length, truncation=True, padding='max_length', return_tensors='pt')
                else:
                    model_inputs = self.tokenizer(input_texts[s:e], truncation=True, padding=True, return_tensors='pt')
                if 'token_type_ids' in model_inputs:
                    model_inputs.pop('token_type_ids')

                output = self.model(**{k: v.to(self.device) for k, v in model_inputs.items()})
                logit = output['logits']
                if self.pad_token_initialized:
                    logit = logit[:, :, :-1]

                # shift the label sequence for causal inference
                label = model_inputs['input_ids']
                label[label == self.tokenizer.pad_token_id] = PAD_TOKEN_LABEL_ID

                # Shift so that tokens < n predict n
                shift_logits = logit[..., :-1, :].contiguous()
                shift_label = label[:, 1:].contiguous()

                # compute loss
                valid_length = (shift_label != PAD_TOKEN_LABEL_ID).sum(dim=-1)
                valid_length = valid_length.to(self.device)
                shift_label = shift_label.to(self.device)
                loss = self.loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_label.view(-1))
                loss = loss.view(len(output['logits']), -1)
                loss = torch.sum(loss, -1) / valid_length
                loss_list += loss.cpu().tolist()

                if FORCE_RESET:
                    del model_inputs
                    del loss
                    del output
                    gc.collect()
                    torch.cuda.empty_cache()

        # conversion to perplexity
        ppl = [exp(i) for i in loss_list]
        return ppl[0] if single_input else ppl
import os
import gc
from math import exp
from typing import List
from tqdm import tqdm
import urllib
import json
import transformers
import torch
os.environ["OMP_NUM_THREADS"] = "1"  # to turn off warning message
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # to turn off warning message
PAD_TOKEN_LABEL_ID = torch.nn.CrossEntropyLoss().ignore_index
FORCE_RESET = bool(int(os.getenv("FORCE_RESET", "0")))

def internet_connection(host: str = 'http://google.com'):
    """ check if internet connection is available """
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
class PPL_Calculator:
    def __init__(self,
                 model: str = 'gpt2',
                 use_auth_token: bool = False,
                 max_length: int = None,
                 num_gpus: int = None,
                 torch_dtype=None,
                 device_map: str = None,
                 low_cpu_mem_usage: bool = False,
                 trust_remote_code: bool = True,
                 offload_folder: str = None,
                 hf_cache_dir: str = None):
        """ Language Model.

        @param model: Model alias or path to local model file.
        @param use_auth_token: Huggingface transformers argument of `use_auth_token`
        @param device: Device name to load the models.
        @param num_gpus: Number of gpus to be used.
        """

        # load model
        params = {"local_files_only": not internet_connection(), "use_auth_token": use_auth_token,
                  "trust_remote_code": trust_remote_code}
        if hf_cache_dir is not None:
            params["cache_dir"] = hf_cache_dir
        if offload_folder is not None:
            params["offload_folder"] = offload_folder
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model, **params)
        self.config = transformers.AutoConfig.from_pretrained(model, **params)

        params.update({"config": self.config, "low_cpu_mem_usage": low_cpu_mem_usage})
        if torch_dtype is not None:
            params['torch_dtype'] = torch_dtype
        if device_map is not None:
            params['device_map'] = device_map
        self.model = transformers.AutoModelForCausalLM.from_pretrained(model, **params)

        self.pad_token_initialized = False
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': "<<PAD>>"})
            self.model.resize_token_embeddings(len(self.tokenizer))
            self.pad_token_initialized = True

        if max_length is None:
            self.max_length = None
        else:
            self.max_length = max_length if max_length is not None else self.tokenizer.model_max_length
            assert self.max_length <= self.tokenizer.model_max_length, f"{self.max_length} > {self.tokenizer.model_max_length}"

        # loss function
        self.loss_fct = torch.nn.CrossEntropyLoss(reduction='none')

        # GPU setup
        self.device = self.model.device
        if device_map is None:
            num_gpus = torch.cuda.device_count() if num_gpus is None else num_gpus
            if num_gpus == 1:
                self.model.to('cuda')
                self.device = self.model.device
            elif num_gpus > 1:
                self.model = torch.nn.DataParallel(self.model)
                self.model.to('cuda')
                self.device = self.model.module.device
        self.model.eval()

    def get_perplexity(self, input_texts: str or List, batch: int = None):
        """ Compute the perplexity on recurrent LM.

        :param input_texts: A string or list of input texts for the encoder.
        :param batch: Batch size
        :return: A value or list of perplexity.
        """

        # batch preparation
        single_input = type(input_texts) == str
        input_texts = [input_texts] if single_input else input_texts
        batch = len(input_texts) if batch is None else batch
        batch_id = list(range(0, len(input_texts), batch)) + [len(input_texts)]
        batch_id = list(zip(batch_id[:-1], batch_id[1:]))

        loss_list = []
        with torch.no_grad():
            for s, e in batch_id:

                # run model inference
                if self.max_length is not None:
                    model_inputs = self.tokenizer(input_texts[s:e], max_length=self.max_length, truncation=True, padding='max_length', return_tensors='pt')
                else:
                    model_inputs = self.tokenizer(input_texts[s:e], truncation=True, padding=True, return_tensors='pt')
                if 'token_type_ids' in model_inputs:
                    model_inputs.pop('token_type_ids')

                output = self.model(**{k: v.to(self.device) for k, v in model_inputs.items()})
                logit = output['logits']
                if self.pad_token_initialized:
                    logit = logit[:, :, :-1]

                # shift the label sequence for causal inference
                label = model_inputs['input_ids']
                label[label == self.tokenizer.pad_token_id] = PAD_TOKEN_LABEL_ID

                # Shift so that tokens < n predict n
                shift_logits = logit[..., :-1, :].contiguous()
                shift_label = label[:, 1:].contiguous()

                # compute loss
                valid_length = (shift_label != PAD_TOKEN_LABEL_ID).sum(dim=-1)
                valid_length = valid_length.to(self.device)
                shift_label = shift_label.to(self.device)
                loss = self.loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_label.view(-1))
                loss = loss.view(len(output['logits']), -1)
                loss = torch.sum(loss, -1) / valid_length
                loss_list += loss.cpu().tolist()

                if FORCE_RESET:
                    del model_inputs
                    del loss
                    del output
                    gc.collect()
                    torch.cuda.empty_cache()

        # conversion to perplexity
        ppl = [exp(i) for i in loss_list]
        return ppl[0] if single_input else ppl
def process_safe_eval_json(file_path, ppl_calculator, batch_size=8):
    # 读取文件
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 提取所有output
    outputs = [x.get("output", "") for x in data if x.get("output", "").strip() != ""]
    if not outputs:
        return 0, 0
    # 批量算PPL
    all_ppl = []
    for i in range(0, len(outputs), batch_size):
        batch = outputs[i:i+batch_size]
        ppls = ppl_calculator.get_perplexity(batch)
        if isinstance(ppls, float):  # 单条也可能返回float
            ppls = [ppls]
        all_ppl.extend(ppls)
    avg_ppl = sum(all_ppl) / len(all_ppl)
    return avg_ppl, len(all_ppl)

def main(root_dir, model="gpt2"):
    ppl_calculator = PPL_Calculator(model)
    results = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith("_safe_eval.json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    avg_ppl, count = process_safe_eval_json(file_path, ppl_calculator)
                    print(f"{file_path}\tavg_ppl={avg_ppl:.2f}\tcount={count}")
                    results.append((file_path, avg_ppl, count))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    # 可选：保存到文件
    # with open("ppl_results.txt", "w") as f:
    #     for path, avg, count in results:
    #         f.write(f"{path}\t{avg:.2f}\t{count}\n")

if __name__ == "__main__":
    import sys

    root_dir = '/data/safedecode/exp_outputs'
    main(root_dir)