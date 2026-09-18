# Chia sẻ repo cho nhiều tài khoản Claude

Repo này để **private**. Mỗi tài khoản Claude muốn dùng chung cần hai thứ: quyền trên
GitHub, và Claude được kết nối tới GitHub.

## 1. Mời tài khoản GitHub của người đó

GitHub → repo `reading-vocab-tracker` → **Settings → Collaborators → Add people** →
nhập username hoặc email → chọn quyền **Write** (cần Write thì tool mới `push` được).

Người được mời phải bấm nhận lời mời trong email hoặc tại
`https://github.com/vohoailinh90/reading-vocab-tracker/invitations`.

## 2. Kết nối Claude với GitHub

Trên tài khoản Claude của người đó:

1. Vào `https://claude.ai/connect-github` và kết nối tài khoản GitHub.
2. Cài Claude GitHub App cho repo này tại
   `https://github.com/apps/claude/installations/select_target` — chọn repo
   `reading-vocab-tracker` (hoặc *All repositories*).
3. Mở `https://claude.ai/code`, chọn repo `reading-vocab-tracker`.

Từ lúc đó `CLAUDE.md` tự được nạp, nên mọi tài khoản đều dùng chung một bộ quy tắc
dịch/giải thích và cùng một định dạng dữ liệu từ vựng.

## 3. Dùng trên máy cá nhân (Claude Code CLI)

```bash
git clone https://github.com/vohoailinh90/reading-vocab-tracker.git
cd reading-vocab-tracker
python3 -m pip install -r requirements.txt
claude
```

## 4. Quy tắc phối hợp để tránh xung đột

- **Luôn `git pull` trước khi thêm từ**, và `sync` ngay sau khi thêm — đừng để dồn nhiều ngày.
- Không sửa tay `data/vocabulary.xlsx`. Nếu file này xung đột khi merge:

  ```bash
  git checkout --ours data/vocabulary.xlsx   # lấy bản nào cũng được
  python3 tools/vocab_tool.py build-xlsx     # dựng lại từ CSV
  git add data/vocabulary.xlsx && git commit
  ```

- File CSV xung đột thì sửa như văn bản thường: giữ cả hai dòng, rồi đảm bảo cột `id`
  không trùng nhau (`python3 -m pytest tests/ -q` sẽ báo nếu trùng).

## 5. Dùng chung trên claude.ai (không qua GitHub)

Nếu chỉ cần chia sẻ *cách trả lời* chứ không cần dữ liệu, copy **Phần A** của
`CLAUDE.md` vào phần hướng dẫn của một Project trên claude.ai rồi mời người khác vào
Project đó. Cách này không đồng bộ file Excel.
