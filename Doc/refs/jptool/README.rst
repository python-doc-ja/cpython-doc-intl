converter
   Python 2.5 の日本語ドキュメントを reStructuredText に変換するのに
   利用した converter.

   元のバージョンに比べて、

   * 入力の tex ファイルのエンコーディングを euc-jp として扱う。
   * reST 出力時に、文字幅を docutils と同じ方法で考慮する。

   という違いがある。


looseconv
   Python 2.5 のドキュメント原文を reST に変換するのに利用した converter 。
   ``methoddesc`` や ``memberdesc`` の所属クラスが不明な場合も、エラーと
   せずに ``XXX Class`` と出力するようにした。

makepatch.py
   diff を取るスクリプト。
   
   差分がないファイルに対してもパッチを作ってしまうという問題がある。
   今回は ``find -type f -size 0 | rm`` で消してしまったけど、今後使うとき
   には後2,3行足して同じファイルはdiffファイルを作らない用にする。
