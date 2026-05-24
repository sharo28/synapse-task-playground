---
scope: synapse-task-playground
version: 1.0.0
id: TASK-006
title: "TASK-004: 本番環境VMの週次フルバックアップ取得"
status: "Todo"
github_state: "OPEN"
repository: "sharo28/synapse-task-playground"
github_url: "https://github.com/sharo28/synapse-task-playground/issues/6"
project_item_id: "PVTI_lAHOBKn2EM4BYn8Zzgto_Xk"
---

# TASK-006: TASK-004: 本番環境VMの週次フルバックアップ取得

## 📋 概要
スケジュール: 毎週日曜日 2:00-6:00 JST
チェックリスト:
- バックアップ対象VMの明確化
- バックアップ手法の選定（Snapshot / Cold Backup / 第三方ツール）
- スケジューリング設定（cron/VMware Scheduler）
- バックアップ先ストレージの確保（ローカル + S3遠隔地）
- スクリプト化と自動化（PowerCLI等）
- ドキュメント化と定期訓練

既存の ADR-010（WAL-G DBバックアップ）と DOC-006（DR運用マニュアル）と関連付けています。VMバックアップとDBバックアップを補完関係として位置づけています。


---

## 🛠️ メタデータ
* **同期ステータス**: 同期済み (読み取り専用レプリカ)
* **GitHub状態**: OPEN (Status: Todo)
* **リポジトリ**: `sharo28/synapse-task-playground`
* **GitHubリンク**: [GitHub Issueはこちら](https://github.com/sharo28/synapse-task-playground/issues/6)
