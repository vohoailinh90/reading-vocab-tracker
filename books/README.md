# Ghi chú sách

Mỗi cuốn một file `books/<ten-sach>.md`, tạo từ `_template.md`.

Phần **theo dõi tiến độ** (trạng thái, số trang, ngày bắt đầu/kết thúc) nằm ở
`data/books.csv` và sheet `Books` trong `data/vocabulary.xlsx`, cập nhật bằng tool:

```bash
python3 tools/vocab_tool.py book \
  --title "Never Split the Difference" \
  --author "Chris Voss" \
  --language "tiếng Anh" \
  --status "đang đọc" \
  --progress "120/320" \
  --started 2026-09-18 \
  --notes-path books/never-split-the-difference.md
```

File markdown giữ phần dài: tóm tắt chương, đoạn trích, cảm nhận. Đừng chép nội dung
này vào CSV — CSV chỉ để lọc và thống kê.

Từ vựng học được từ một cuốn sách thì lưu bằng `vocab_tool.py add` với
`--source "<tên sách>"` và `--page <trang>`, để sau này lọc lại theo sách.
