$(function(){
  const input = $('.input_text'); // inputタグ内のクラス名
  const chatlog = $('.chat-log'); // 結果を追加していくためのdivタグ内のクラス名

  // ユーザーのログを追加する関数
  function createRow_user(text) {
    const row = $(`<p class="chat-text-color1"><span>${text}</span></p>`); // クラス名を追記
    chatlog.append(row);
  }

  // ボットのログを追加する関数
  function createRow_bot(text) {
    const row = $(`<p class="chat-text-color2"><span>${text}</span></p>`); // クラス名を追記
    chatlog.append(row);
  }

  // Ajax
  $('form').submit(function (event) {
    event.preventDefault();
    let form = $(this);

    // HTMLフォームの情報を設定する
    $.ajax({
        url: form.prop('action'), // 非同期通信するURL（/bot_response/）
        type: form.prop('method'), // POST
        data: form.serialize(), // データの情報
        dataType: 'text', // データのタイプ
    })
    .done(function (statement) {
        createRow_user(`あなた : ${input.val()}`); // ユーザーのログを追加
        createRow_bot(statement); // ボットのログを追加
        input.val(''); // input内の要素を空にする

        // ログ枠のスクロールを最後の結果に合わせる
        chatlog[0].scrollTop = chatlog[0].scrollHeight;
    })
    // 送信に失敗した場合
    .fail(function () {
        alert('もう一度やり直してください');
    });
  });
});