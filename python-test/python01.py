import pandas as pd
import plotly.express as px

# CSVファイルのパス
csv_path = "data.csv"

# 読み込み
df = pd.read_csv(
    csv_path,
    encoding="shift_jis",
    skiprows=[0, 1, 2, 4, 5],
    header=0
)

# 必要な列だけ取り出す
df = df[["年月日", "平均気温(℃)"]]

# 型変換
df["年月日"] = pd.to_datetime(
    df["年月日"],
    format="%Y/%m/%d",
    errors="coerce"
)

df["平均気温(℃)"] = pd.to_numeric(
    df["平均気温(℃)"],
    errors="coerce"
)

# グラフ作成
fig = px.line(
    df,
    x="年月日",
    y="平均気温(℃)",
    title="平均気温の推移",
    labels={
        "年月日": "日付",
        "平均気温(℃)": "気温(℃)"
    }
)

# HTMLファイルとして保存
fig.write_html("temperature.html")

print("temperature.html を生成しました")