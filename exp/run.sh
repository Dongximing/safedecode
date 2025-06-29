#!/bin/bash

python defense.py --model_name llama2 --attacker GCG --defender PPL --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender PPL --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender PPL --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender PPL --disable_GPT_judge

python defense.py --model_name llama2 --attacker GCG --defender  Self-Exam --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender  Self-Exam --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender  Self-Exam --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender  Self-Exam --disable_GPT_judge

python defense.py --model_name llama2 --attacker GCG --defender Paraphrase --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender Paraphrase --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender Paraphrase --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender Paraphrase --disable_GPT_judge

python defense.py --model_name llama2 --attacker GCG --defender Retokenization --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender Retokenization --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender Retokenization --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender Retokenization --disable_GPT_judge

python defense.py --model_name llama2 --attacker GCG --defender Self-Reminder --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender Self-Reminder --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender Self-Reminder --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender Self-Reminder --disable_GPT_judge


python defense.py --model_name llama2 --attacker GCG --defender ICD --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender ICD --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender ICD --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender ICD --disable_GPT_judge

python defense.py --model_name llama2 --attacker GCG --defender SafeDecoding --disable_GPT_judge
python defense.py --model_name llama2 --attacker  AutoDAN --defender SafeDecoding --disable_GPT_judge
python defense.py --model_name llama2 --attacker  PAIR --defender SafeDecoding --disable_GPT_judge
python defense.py --model_name llama2 --attacker  DeepInception --defender SafeDecoding  --disable_GPT_judge



