# reading-vocab-tracker

Theo dõi việc **đọc sách** và tích luỹ **từ vựng tiếng Anh / tiếng Nhật**, dùng chung
cho nhiều tài khoản Claude.

- `CLAUDE.md` — hướng dẫn agent dịch/giải thích Anh–Nhật sang tiếng Việt. Mọi phiên
  Claude mở repo này đều tự nạp nó, nên các tài khoản trả lời theo cùng một chuẩn.
- `tools/vocab_tool.py` — thêm từ vựng, cập nhật tiến độ sách, dựng file Excel, và
  đẩy lên repo.

## Cài đặt

```bash
git clone https://github.com/vohoailinh90/reading-vocab-tracker.git
cd reading-vocab-tracker
python3 -m pip install -r requirements.txt
python3 tools/vocab_tool.py init          # chỉ cần khi thiếu file dữ liệu
```

## Dùng nhanh

```bash
# Thêm một từ — tự nhận diện tiếng Anh hay tiếng Nhật theo ký tự
python3 tools/vocab_tool.py add \
  --term "escalate" \
  --reading "/ˈeskəleɪt/" \
  --meaning "đẩy vấn đề lên cấp cao hơn" \
  --register "trung tính" \
  --example "We need to escalate this to the DNOx team lead." \
  --example-vi "Chúng ta cần đẩy việc này lên trưởng nhóm DNOx." \
  --source "Never Split the Difference" --page 42 --tags "công việc,họp"

# Từ tiếng Nhật vào đúng sheet JA mà không cần khai báo --lang
python3 tools/vocab_tool.py add --term "納期" --reading "のうき" --meaning "kỳ hạn giao hàng"

# Cập nhật tiến độ đọc
python3 tools/vocab_tool.py book --title "Never Split the Difference" \
  --author "Chris Voss" --status "đang đọc" --progress "120/320"

# Xem lại và đẩy lên GitHub
python3 tools/vocab_tool.py list --lang en --limit 20
python3 tools/vocab_tool.py sync -m "vocab: từ mới chương 3"
```

Các lệnh khác: `add-batch <file.json>`, `build-xlsx`, `import`, `init`.
Xem đầy đủ tham số bằng `python3 tools/vocab_tool.py <lệnh> --help`.

## Dữ liệu nằm ở đâu

| File | Vai trò |
|---|---|
| `data/vocabulary.en.csv` | **Nguồn sự thật** — từ vựng tiếng Anh |
| `data/vocabulary.ja.csv` | **Nguồn sự thật** — từ vựng tiếng Nhật |
| `data/books.csv` | **Nguồn sự thật** — sách và tiến độ đọc |
| `data/vocabulary.xlsx` | **Bản sinh ra** từ ba file trên — 3 sheet `EN`, `JA`, `Books` |
| `books/*.md` | Ghi chú dài cho từng cuốn sách |

**Vì sao không lấy thẳng Excel làm nguồn sự thật:** repo dùng chung cho nhiều tài khoản.
`.xlsx` là binary nên git không merge được theo dòng — hai người cùng thêm từ trong một
ngày sẽ tạo xung đột không giải được bằng tay. CSV merge bình thường, còn Excel chỉ cần
dựng lại bằng `build-xlsx`. Vì vậy **đừng sửa trực tiếp `data/vocabulary.xlsx`** — nội
dung sửa tay sẽ bị ghi đè ở lần dựng kế tiếp.

Cột của sheet từ vựng: `id`, `ngày thêm`, `từ vựng`, `cách đọc`, `nghĩa tiếng Việt`,
`văn nói/văn viết`, `cụm văn nói tương đương`, `ví dụ`, `nghĩa ví dụ`, `nguồn`, `trang`,
`nhãn`, `ghi chú` — khớp đúng những mục mà `CLAUDE.md` yêu cầu agent giải thích.

## Thêm trùng từ thì sao

Mặc định tool **cập nhật đè** vào dòng cũ thay vì tạo dòng mới, và chỉ đè những trường
được truyền vào lần này — ô cũ không bị xoá trắng. Dùng `--strict` nếu muốn báo lỗi.

Hai điểm dễ bất ngờ:

- **Cột `từ vựng` là ngoại lệ của quy tắc trên.** Vì `--term` luôn phải truyền, nên thêm
  lại `"  Root Cause "` lên từ `"root cause"` đã có sẽ đổi luôn cách viết hoa đã lưu
  thành `Root Cause`. Đây là cách để sửa chính tả/viết hoa; nếu không muốn đổi thì gõ
  đúng như đã lưu.
- **Tiếng Nhật viết bằng romaji không tự nhận diện được.** Tool phân loại Anh/Nhật theo
  ký tự kana/kanji, nên `shimekiri` sẽ rơi vào sheet EN. Với romaji hãy chỉ định rõ:
  `--lang ja`.

## Nạp file Excel từ vựng cũ

File Excel từ vựng có sẵn từ trước **chưa xác định được đường dẫn**; khi tìm ra:

```bash
python3 tools/vocab_tool.py import --path "<đường-dẫn-file.xlsx>" --dry-run
python3 tools/vocab_tool.py import --path "<đường-dẫn-file.xlsx>"
```

`--dry-run` in ra tool nhận diện được cột nào mà không ghi gì. Tool tự hiểu nhiều kiểu
tên cột tiếng Việt/Anh/Nhật (`Từ vựng`, `Nghĩa tiếng Việt`, `Cách đọc`, `Ví dụ`, `単語`,
`意味`, `Word`, `Meaning`...).

File Excel làm tay thường không phải một bảng phẳng, nên tool xử lý sẵn:

- **Dòng tựa đề phía trên bảng** (kiểu `TỪ VỰNG BOSCH DNOx - 2024` gộp ô ngang): tự dò
  10 dòng đầu để tìm đúng hàng tiêu đề. Tựa đề dài hơn 10 dòng thì chỉ rõ bằng
  `--header-row 13`.
- **Dòng ghi chú gộp ô ngang nằm giữa bảng**: bị bỏ qua kèm cảnh báo, thay vì nạp thành
  một "từ vựng" rác.
- **Hai cột trùng tên**: chỉ lấy cột đầu, và in cảnh báo cho biết cột nào bị bỏ.

Tên cột lạ thì chỉ định thủ công:

```bash
python3 tools/vocab_tool.py import --path "cu.xlsx" \
  --map "Cột từ=term" --map "Diễn giải=meaning_vi"
```

Muốn tool ghi thêm một bản Excel ra thư mục ngoài repo thì điền `external_excel_path`
trong `config/vocab.config.json`.

## Chia sẻ cho nhiều tài khoản Claude

Xem `docs/chia-se-nhieu-tai-khoan.md`.

## Kiểm thử

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests/ -q
```

`tests/test_vocab_tool.py` kiểm tra hành vi của tool trên thư mục tạm.
`tests/test_repo_data.py` kiểm tra tính toàn vẹn của dữ liệu thật trong `data/`
(đúng cột, `id` không trùng, từ không trùng) — nó sẽ báo nếu một lần merge git để lại
dữ liệu hỏng.
