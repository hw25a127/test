import requests            # Webサイトへのリクエスト（アクセス）を行うためのライブラリ
import os                  # ファイルやパスの操作のための標準ライブラリ
import urllib3             # HTTP通信を制御する低レベルライブラリ（requestsの下層で使われる）

# ★自己署名証明書による警告を表示させないようにする設定
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# チェック対象のURL（更新を監視したいWebページ）
url = "https://dench.mklab.osakac.ac.jp/script-pg/"

# 前回取得したページの内容を保存するためのファイル名
cache_file = "last_script_03.txt"

try:
    # ★証明書の検証を無効にしてWebページを取得（自己署名証明書に対応するため）
    response = requests.get(url, verify=False)
    
    # ステータスコードが200番台でない場合はエラーとして扱う
    response.raise_for_status()
    
    # HTMLの内容をテキストとして取得し、前後の空白や改行を取り除く
    current_content = response.text.strip()

except requests.exceptions.RequestException as e:
    # 通信に失敗した場合にエラーメッセージを表示して終了
    print(f"通信エラー: {e}")
    exit(1)

# ===== ここから差分チェックの処理 =====

# 前回の内容を保存したファイルがまだない（初回）場合
if not os.path.exists(cache_file):
    # 現在取得した内容を保存して初回完了のメッセージを表示
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(current_content)
    print("初回取得完了（差分なし）")

else:
    # 前回保存された内容を読み込む
    with open(cache_file, "r", encoding="utf-8") as f:
        previous_content = f.read().strip()

    # 今回取得した内容と前回の内容を比較
    if current_content != previous_content:
        # 差分があれば更新を検出したとして出力
        print("更新が検出されました！")
        print("前回:", previous_content)
        print("今回:", current_content)
        
        # 差分を検出したので、今回の内容で上書き保存する
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(current_content)
    else:
        # 内容が同じなら変更なしとして表示
        print("変更はありません。")