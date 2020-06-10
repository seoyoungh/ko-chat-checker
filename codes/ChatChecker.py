from . import CustomModel # seq2seq module
from . import Utils # other functions

from .CustomModel import *
from .Utils import *

def model_only(sentence):
  text = spacer(sentence)
  text_list = tokenizer(text)
  id_list, wrong_list = check_error(text_list)
  final_wrong, pceq = clean_w_pceq(id_list, text_list)
  corrected = seq2seq(final_wrong)
  output = correct(text_list, id_list, corrected, pceq)
  output = sum(output)
  return output

def both(sentence):
  text = spacer(sentence)
  text_list = tokenizer(text)
  id_list, wrong_list = check_error(text_list)
  final_wrong, pceq = clean_w_pceq(id_list, text_list)
  corrected = seq2seq(final_wrong)
  corrected2 = edit_distance_04(final_wrong)
  result = compare(final_wrong, corrected, corrected2)
  output = correct(text_list, id_list, result, pceq)
  output = sum(output)
  return output

def model_only_word(word):
  result = seq2seq([word])
  suggestion = result[0]
  # print("Suggestion: ", suggestion)
  return suggestion

def edit_only_word(word):
  result = edit_distance_04([word])
  suggestions = ""

  for i in range(len(result[0])):
    if i == len(result[0]) - 1:
      suggestions += result[0][i][0]
    else:
      suggestions += result[0][i][0] + ", "

  # print("Suggestions: ", suggestions)
  return suggestions

def both_word(word):
  model_prediction = model_only_word(word)
  edit_prediction = edit_only_word(word)
  # print("Model suggestion: ", model_prediction)
  # print("Edit Distance suggestion: ", edit_prediction)
  return model_prediction, edit_prediction
