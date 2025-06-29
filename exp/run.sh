#!/bin/bash

python defense.py --model_name vicuna --attacker GCG --defender PPL --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender PPL --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender PPL --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender PPL --disable_GPT_judge

python defense.py --model_name vicuna --attacker GCG --defender  Self-Exam --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender  Self-Exam --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender  Self-Exam --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender  Self-Exam --disable_GPT_judge

python defense.py --model_name vicuna --attacker GCG --defender Paraphrase --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender Paraphrase --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender Paraphrase --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender Paraphrase --disable_GPT_judge

python defense.py --model_name vicuna --attacker GCG --defender Retokenization --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender Retokenization --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender Retokenization --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender Retokenization --disable_GPT_judge

python defense.py --model_name vicuna --attacker GCG --defender Self-Reminder --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender Self-Reminder --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender Self-Reminder --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender Self-Reminder --disable_GPT_judge


python defense.py --model_name vicuna --attacker GCG --defender ICD --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender ICD --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender ICD --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender ICD --disable_GPT_judge

python defense.py --model_name vicuna --attacker GCG --defender SafeDecoding --disable_GPT_judge
python defense.py --model_name vicuna --attacker  AutoDAN --defender SafeDecoding --disable_GPT_judge
python defense.py --model_name vicuna --attacker  PAIR --defender SafeDecoding --disable_GPT_judge
python defense.py --model_name vicuna --attacker  DeepInception --defender SafeDecoding  --disable_GPT_judge



