import pandas as pd
import numpy as np

# ===== 設定 =====
csv_path = "df_random_7_1.csv"     # 入力CSV
x_col = "valence"                # x値の列名
y_col = "arousal"                # y値の列名
output_csv = "output.csv"  # 出力CSV（上書き可）

# ===== CSV読み込み =====
df = pd.read_csv(csv_path)

# ===== 最大値の取得 =====
x_max = df[x_col].max()
y_max = df[y_col].max()

# ===== 距離スカラーの計算 =====
# max点 (x_max, y_max) からのユークリッド距離
df["distance_from_max"] = np.sqrt(
    (df[x_col] - x_max) ** 2 +
    (df[y_col] - y_max) ** 2
)

# ===== CSV出力 =====
df.to_csv(output_csv, index=False)
