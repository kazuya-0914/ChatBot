import torch
from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from transformers import AutoModelForQuestionAnswering, BertJapaneseTokenizer

model_name = 'KoichiYasuoka/bert-base-japanese-wikipedia-ud-head'
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

class TopView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    title = 'チャットボットアプリ'

    # データ出力
    context = super().get_context_data(**kwargs)
    params = {
        'title': title,
    }
    context.update(params)
    return context

# replayメソッド
def reply(question):
  tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
  context = "私の名前は山田です。趣味は動画鑑賞とショッピングです。年齢は30歳です。出身は大阪府です。仕事は医者です。"
  inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
  input_ids = inputs["input_ids"].tolist()[0]
  output = model(**inputs)
  answer_start = torch.argmax(output.start_logits)
  answer_end = torch.argmax(output.end_logits) + 1
  answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
  answer = answer.replace(' ', '')
  return answer

# bot_responseビュー
def bot_response(request):
  input_data = request.POST.get('input_text')
  if not input_data:
    return HttpResponse('<h2>空のデータを受け取りました。</h2>', status=400)
  bot_response = reply(input_data)
  http_response = HttpResponse()
  http_response.write(f"BOT: {bot_response}")

  return http_response