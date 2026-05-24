import subprocess
import json
import os
import sys

# 新しいプレイグラウンドプロジェクトのID
PROJECT_ID = "PVT_kwHOBKn2EM4BYn8Z"
# 自分自身があるディレクトリをスコープの出力先にする
SCOPE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_graphql_query(query, variables=None):
    try:
        # 環境変数に GH_TOKEN がある場合はそれを使用し、ない場合は通常の gh CLI の認証を使う
        token = os.environ.get("GH_TOKEN")
        
        cmd = ["gh", "api", "graphql"]
        if variables:
            for key, val in variables.items():
                cmd.extend(["-F", f"{key}={val}"])
        cmd.extend(["-f", f"query={query}"])
        
        env = os.environ.copy()
        if token:
            env["GH_TOKEN"] = token
            
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        
        res_data = json.loads(result.stdout)
        if "errors" in res_data:
            raise Exception(f"GraphQL Errors: {json.dumps(res_data['errors'], indent=2)}")
        
        return res_data["data"]
    except subprocess.CalledProcessError as e:
        print(f"❌ gh api コマンドの実行に失敗しました:\n{e.stderr}", file=sys.stderr)
        sys.exit(1)

def generate_markdown_cache(item):
    content = item.get("content")
    if not content:
        return
    
    issue_number = content.get("number")
    if not issue_number:
        return
    
    title = content.get("title", "Untitled")
    body = content.get("body", "") or "（本文なし）"
    state = content.get("state", "OPEN")
    repo = content.get("repository", {}).get("nameWithOwner", "unknown")
    item_id = item.get("id")
    
    status = "Todo"
    field_values = item.get("fieldValues", {}).get("nodes", [])
    for val in field_values:
        if "field" in val and val["field"].get("name") == "Status":
            status = val.get("name", "Todo")
            
    doc_id = f"TASK-{issue_number:03d}"
    file_name = f"{doc_id}.md"
    file_path = os.path.join(SCOPE_DIR, file_name)
    
    markdown_content = f"""---
scope: synapse-task-playground
version: 1.0.0
id: {doc_id}
title: "{title}"
status: "{status}"
github_state: "{state}"
repository: "{repo}"
github_url: "https://github.com/{repo}/issues/{issue_number}"
project_item_id: "{item_id}"
---

# {doc_id}: {title}

## 📋 概要
{body}

---

## 🛠️ メタデータ
* **同期ステータス**: 同期済み (読み取り専用レプリカ)
* **GitHub状態**: {state} (Status: {status})
* **リポジトリ**: `{repo}`
* **GitHubリンク**: [GitHub Issueはこちら](https://github.com/{repo}/issues/{issue_number})
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"✅ ローカルキャッシュ生成完了: {file_name} (Status: {status})")

def main():
    print(f"🔄 GitHub Projects ID: {PROJECT_ID} からタスク同期中...")
    
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          title
          items(first: 50) {
            nodes {
              id
              type
              fieldValues(first: 15) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                }
              }
              content {
                ... on Issue {
                  title
                  number
                  body
                  state
                  repository {
                    nameWithOwner
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"projectId": PROJECT_ID}
    
    data = run_graphql_query(query, variables)
    project = data.get("node")
    if not project:
        print("❌ プロジェクトが見つかりません。")
        return
        
    items = project["items"]["nodes"]
    if not items:
        print("💡 同期対象のアイテムはありません。")
        return
        
    for item in items:
        generate_markdown_cache(item)
        
    print("✨ 同期プロセスが正常に完了しました！")

if __name__ == "__main__":
    main()
