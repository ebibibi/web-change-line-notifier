# web-change-line-notifier

Webサイトの変更を検知してLINEに通知するPythonスクリプトです。

## 機能

- 指定したWebサイトのHTMLを取得し、ハッシュ値で変更を検知
- 変更があった場合、LINE Messaging APIで通知
- 個人またはグループへの通知に対応

## セットアップ

### 1. LINE Messaging APIの準備

LINE Notifyは2025年3月31日でサービス終了したため、LINE Messaging APIを使用します。

#### 1.1 LINE Developersでチャネル作成

1. [LINE Developers](https://developers.line.biz/)にログイン
2. プロバイダーを作成（または既存のものを選択）
3. 「新規チャネル作成」→「Messaging API」を選択
4. チャネル情報を入力して作成

#### 1.2 チャネルアクセストークンの取得

1. 作成したチャネルを開く
2. 「Messaging API設定」タブをクリック
3. ページ下部の「チャネルアクセストークン（長期）」で「発行」をクリック
4. 表示されたトークンをコピー

#### 1.3 ユーザーID / グループIDの取得

**個人に通知する場合:**
- 「チャネル基本設定」タブの下部にある「あなたのユーザーID」を使用
- ※ビジネスIDでログインしている場合は表示されません（下記のWebhook方式で取得）

**グループに通知する場合:**
1. [webhook.site](https://webhook.site)にアクセスし、表示されたURLをコピー
2. LINE Developersの「Messaging API設定」タブで「Webhook URL」にペースト
3. 「Webhookの利用」をONにする
4. LINE公式アカウント（Bot）をグループに招待
5. グループ内でメッセージを送信
6. webhook.siteに届いたJSONの `events[0].source.groupId` がグループID

### 2. 環境構築

```bash
# リポジトリをクローン
git clone https://github.com/ebibibi/web-change-line-notifier.git
cd web-change-line-notifier

# 依存関係をインストール
pip install -r requirements.txt

# .envファイルを作成
cp .env.example .env
```

### 3. .envファイルの設定

```bash
# LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_USER_ID=your_user_id_or_group_id

# 監視対象のURL
TARGET_URL=https://example.com

# 通知メッセージ
NOTIFICATION_MESSAGE=Webサイトが更新されました！

# 状態保存ファイル（オプション）
STATE_FILE=state.json
```

| 変数名 | 説明 |
|--------|------|
| `LINE_CHANNEL_ACCESS_TOKEN` | チャネルアクセストークン（長期） |
| `LINE_USER_ID` | 通知先のユーザーID（`U`で始まる）またはグループID（`C`で始まる） |
| `TARGET_URL` | 監視対象のWebサイトURL |
| `NOTIFICATION_MESSAGE` | 変更検知時に送信するメッセージ |
| `STATE_FILE` | 前回のハッシュを保存するファイル（デフォルト: `state.json`） |

## 使い方

```bash
python main.py
```

- 初回実行時は状態を保存するだけで通知はスキップされます
- 2回目以降、前回と比較して変更があれば通知されます

### 定期実行

cronやsystemdタイマーで定期実行することを想定しています。

```bash
# 例: 1時間ごとに実行（cron）
0 * * * * cd /path/to/web-change-line-notifier && /usr/bin/python3 main.py
```

## 参考URL

### LINE Messaging API

- [LINE Developers](https://developers.line.biz/) - 公式コンソール
- [Messaging API | LINE Developers](https://developers.line.biz/ja/services/messaging-api/) - 概要
- [チャネルアクセストークン | LINE Developers](https://developers.line.biz/ja/docs/basics/channel-access-token/) - トークンの種類と発行方法
- [プッシュメッセージを送る | LINE Developers](https://developers.line.biz/ja/docs/messaging-api/sending-messages/#send-push-messages) - APIリファレンス
- [ユーザーIDを取得する | LINE Developers](https://developers.line.biz/ja/docs/messaging-api/getting-user-ids/) - ユーザーID/グループIDの取得方法

### 料金

- [LINE公式アカウントの料金プラン](https://www.linebiz.com/jp/service/line-official-account/plan/)
- コミュニケーションプラン: 月200通まで無料

## ライセンス

Apache-2.0 License
