Python・R業務データトレンド分析ツール

概要

このプロジェクトは、業務データをもとに売上トレンドを分析するための学習用プロジェクトです。

同じCSVデータを使用し、Python版とR版の両方で月別売上推移、前月比成長率、3か月移動平均、異常値検出、カテゴリ別売上集計を実装しています。

Pythonでは pandas、matplotlib、openpyxl を使用し、Rでは tidyverse、openxlsx、zoo を使用しています。

使用技術

* Python
* pandas
* matplotlib
* openpyxl
* R
* tidyverse
* openxlsx
* zoo
* CSV
* Excel
* Git / GitHub

主な機能

* サンプル業務データの自動生成
* CSVデータの読み込み
* 日付データの変換
* 月別売上推移の分析
* 前月比成長率の計算
* 3か月移動平均の計算
* 異常値の検出
* カテゴリ別売上集計
* 月別・カテゴリ別売上集計
* グラフ画像の自動出力
* Excel分析レポートの自動出力
* Python版とR版による同一分析の実装

Python版とR版について

このプロジェクトでは、同じ業務データを使用して、PythonとRの両方で同じ分析処理を実装しています。

Python版では、主に pandas を用いてデータ加工・集計を行い、matplotlib でグラフを作成し、openpyxl を利用してExcelレポートを出力しています。

R版では、tidyverse を用いてデータ加工・集計を行い、zoo で移動平均を計算し、openxlsx でExcelレポートを出力しています。

同じ分析テーマを複数の言語で実装することで、データ分析処理の理解を深めることを目的としています。

ディレクトリ構成

business-trend-analysis/
├── data/
│   └── sample_sales_data.csv
├── output/
│   ├── trend_analysis_report.xlsx
│   ├── monthly_sales_trend.png
│   ├── trend_analysis_report_r.xlsx
│   └── monthly_sales_trend_r.png
├── python/
│   ├── generate_sample_data.py
│   └── trend_analysis.py
├── r/
│   └── trend_analysis.R
├── README.md
├── requirements.txt
└── .gitignore

実行方法

1. Python仮想環境の作成

python3 -m venv .venv
source .venv/bin/activate

2. Pythonライブラリのインストール

pip install -r requirements.txt

3. サンプルデータの生成

python python/generate_sample_data.py

実行後、data/sample_sales_data.csv が作成されます。

4. Python版の分析実行

python python/trend_analysis.py

実行後、以下のファイルが output/ フォルダに作成されます。

trend_analysis_report.xlsx
monthly_sales_trend.png

5. R版の分析実行

Rの必要パッケージをインストールします。

install.packages("tidyverse")
install.packages("openxlsx")
install.packages("zoo")

その後、以下を実行します。

Rscript r/trend_analysis.R

実行後、以下のファイルが output/ フォルダに作成されます。

trend_analysis_report_r.xlsx
monthly_sales_trend_r.png

出力されるExcelシート

Python版・R版ともに、主に以下の内容を出力します。

* Cleaned Data
* Monthly Trend
* Category Sales
* Monthly Category

分析内容

月別売上推移

注文日から年月を抽出し、月別の売上合計を計算します。

前月比成長率

月別売上をもとに、前月と比較した成長率を計算します。

3か月移動平均

短期的な変動をならし、売上の傾向を見やすくするために3か月移動平均を計算します。

異常値検出

月別売上が平均値から大きく離れている月を異常値として判定します。

カテゴリ別売上集計

カテゴリごとの売上合計を集計し、売上貢献度の高いカテゴリを確認します。

学習・開発目的

このプロジェクトでは、業務データの集計・分析を通じて、データ分析の基本的な流れを学習することを目的としています。

特に、Excelで確認するような月別集計やカテゴリ別集計を、PythonとRの両方で自動化することで、データ加工、集計、可視化、レポート作成の基礎を確認しています。

また、同じ処理をPythonとRで実装することで、それぞれの言語におけるデータ分析手法の違いを確認しています。

今後の改善予定

* 線形回帰による簡易売上予測
* カテゴリ別の成長率分析
* 顧客別購買傾向の分析
* 異常値検出ロジックの改善
* Python版とR版の結果比較シート作成
* Streamlitを使用した簡易ダッシュボード化
