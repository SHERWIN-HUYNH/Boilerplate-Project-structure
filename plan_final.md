# Plan Final — Distributed Messaging Delivery Service

## 1) Mục tiêu tổng thể
Xây dựng một MVP cho hệ thống messaging delivery có thể:
- nhận message từ CLI
- validate và chuẩn hóa message
- đưa message vào queue-like storage trong bộ nhớ
- xử lý bất đồng bộ bằng worker pool
- mô phỏng success / temporary failure / permanent failure
- retry tối đa 3 lần với backoff tăng dần
- ghi đúng **1 final row** cho mỗi `message_id` ra file JSONL
- xuất counters/logs cơ bản và chạy benchmark bằng một lệnh

Mục tiêu của kế hoạch này là đủ rõ để dùng làm **đầu vào cho lệnh `specify`** trong quy trình spec-driven development.

## 2) Nguyên tắc triển khai theo spec-driven development
Mỗi epic bên dưới cần được chuyển thành một spec riêng trước khi code:
1. Xác định mục tiêu nghiệp vụ của epic
2. Chốt input/output và ranh giới trách nhiệm
3. Viết acceptance criteria rõ ràng
4. Chỉ implement phần nhỏ nhất để pass spec
5. Verify ngay bằng test hoặc command tương ứng

Không đi vào thiết kế production-grade ngoài phạm vi 2 giờ.

## 3) Chọn công nghệ
### Ngôn ngữ
**Python**

### Lý do chọn
- viết nhanh, phù hợp timebox 2 giờ
- standard library đủ mạnh cho CLI, JSONL, logging, counters, benchmark
- dễ mô phỏng async worker và retry logic
- dễ đọc/giải thích trong bài test

### Stack đề xuất
- `argparse` cho CLI
- `asyncio` hoặc worker pool nhẹ cho xử lý đồng thời
- `dataclasses` cho model dữ liệu
- `logging` cho log runtime
- `json` / JSONL writer tự triển khai
- `collections.Counter` hoặc class counters đơn giản cho metrics

Nếu cần dependency ngoài để tăng tốc validation, có thể dùng `pydantic`, nhưng chỉ nên chọn nếu thực sự giúp giảm thời gian implement.

## 4) Phạm vi khả thi trong 2 giờ
### MVP bắt buộc
- Ingestion CLI
- Validation/normalization
- Queue/storage in-memory
- Worker processing
- Retry/backoff
- Final writer JSONL exactly-once per message
- Basic logging + counters
- Benchmark harness
- Documentation: `README.md`, `BENCHMARK.md`, `AI_USAGE.md`

### Không làm trong 2 giờ
- distributed multi-node thật sự
- persistence kiểu database
- monitoring production-grade
- tối ưu throughput cực sâu vượt yêu cầu benchmark

---

# 5) Epic-based plan

## Epic A — Ingestion
### Ý nghĩa
Epic này định nghĩa cách hệ thống nhận message từ bên ngoài và biến nó thành dữ liệu hợp lệ để đưa vào pipeline. Đây là lớp đầu vào duy nhất cho toàn hệ thống.

### Bao gồm
- Feature 1 — Input contract & entrypoint
- Feature 2 — Validation & normalization

### Context cần có cho `specify`
Hệ thống phải chấp nhận message với schema:
- `message_id`: unique string
- `recipient`: string
- `channel`: một trong `email | sms | push`
- `priority`: một trong `high | normal | low`
- `content`: string
- `created_at`: timestamp

CLI là giao diện chính, vì benchmark cần chạy được bằng một lệnh và input volume lớn.

### Ranh giới
Epic này chỉ xử lý:
- nhận input
- kiểm tra hợp lệ
- chuẩn hóa dữ liệu
- trả lỗi rõ ràng nếu invalid

Epic này không xử lý queue, worker hay output file.

### Acceptance criteria cấp epic
- submit được message hợp lệ qua CLI
- message sai schema bị reject rõ ràng
- message sau validation có format thống nhất để đưa vào queue

### Spec đầu ra mong muốn
Một spec riêng cho Epic A cần mô tả rõ:
- input command name
- schema message
- validation rules
- behavior với input lỗi
- output của bước ingest/validate

---

## Epic B — Delivery pipeline
### Ý nghĩa
Epic này tạo lõi xử lý message: lưu tạm, phân phối cho worker, mô phỏng delivery, và áp dụng retry/backoff khi fail tạm thời. Đây là phần quyết định system có chạy đúng luồng hay không.

### Bao gồm
- Feature 3 — Queue/storage & lifecycle state
- Feature 4 — Worker processing & delivery simulation
- Feature 5 — Retry policy with backoff

### Context cần có cho `specify`
Pipeline phải thể hiện được trạng thái của message theo vòng đời tối thiểu:
- `pending`
- `processing`
- `retrying`
- `delivered`
- `failed`

Queue/storage ở mức MVP có thể là in-memory queue hoặc queue-like structure, miễn là:
- worker có thể lấy việc từ đó
- state không bị mất trong quá trình chạy bình thường
- retry được điều phối có kiểm soát

Worker phải mô phỏng 3 loại outcome:
- success
- temporary failure
- permanent failure

Temporary failure phải được retry tối đa 3 lần, với backoff tăng dần.

### Ranh giới
Epic này không chịu trách nhiệm viết output final file. Nó chỉ tạo final outcome để chuyển sang Epic C.

### Acceptance criteria cấp epic
- message được enqueue thành công
- worker có thể xử lý đồng thời
- temporary failure được retry đúng policy
- permanent failure không retry vượt quy định
- attempts được đếm đúng

### Spec đầu ra mong muốn
Một spec riêng cho Epic B cần mô tả rõ:
- data model queue item
- state machine lifecycle
- worker concurrency model
- failure simulation rules
- retry/backoff rules
- attempt counting rules

---

## Epic C — Finalization & proof
### Ý nghĩa
Epic này đảm bảo hệ thống tạo ra bằng chứng cuối cùng cho bài test: mỗi message có đúng một final row, có counters/log để kiểm chứng, và có benchmark command để chứng minh throughput và correctness.

### Bao gồm
- Feature 6 — Final result writer with exactly-one-row guarantee
- Feature 7 — Logging, counters, and basic observability
- Feature 8 — Benchmark harness

### Context cần có cho `specify`
Mọi message sau khi kết thúc pipeline chỉ được ghi **một lần** vào output file, định dạng ưu tiên là **JSONL** vì append nhanh và dễ verify.

Output final phải có các trường phù hợp với trạng thái:
- thành công: `message_id`, `recipient`, `channel`, `status=delivered`, `attempts`, `delivered_at`
- thất bại: `message_id`, `recipient`, `channel`, `status=failed`, `reason`, `attempts`, `finished_at`

Writer phải chặn duplicate final rows theo `message_id`.

Benchmark phải chạy từ clean start và kiểm tra được:
- tổng số message
- số final rows
- duplicate final rows
- data loss count
- success/fail/retry counts
- duration và throughput

### Ranh giới
Epic này không thay đổi logic nghiệp vụ ingest hay retry. Nó chỉ chuẩn hóa đầu ra và proof.

### Acceptance criteria cấp epic
- mỗi `message_id` sinh đúng 1 final row
- retry không tạo duplicate final rows
- counters tổng hợp cuối job chính xác
- benchmark có thể chạy bằng 1 command và sinh report đủ trường

### Spec đầu ra mong muốn
Một spec riêng cho Epic C cần mô tả rõ:
- output format
- dedup strategy
- write guarantee
- logging/counter names
- benchmark command
- validation rules của benchmark output

---

## Epic D — Delivery package
### Ý nghĩa
Epic này hoàn thiện phần nộp bài: tài liệu design, benchmark report, và AI usage disclosure. Đây là phần giúp người chấm hiểu hệ thống và xác nhận cách dùng AI.

### Bao gồm
- Feature 9 — Documentation and AI usage report

### Context cần có cho `specify`
Cần có 3 file tài liệu tối thiểu:
- `README.md`
- `BENCHMARK.md`
- `AI_USAGE.md`

Tài liệu phải đủ ngắn gọn nhưng rõ:
- mục tiêu hệ thống
- quyết định thiết kế
- cách chạy benchmark
- kết quả benchmark
- AI đã hỗ trợ phần nào, prompt nào, phần nào tự chỉnh sửa thủ công

### Ranh giới
Epic này không thêm logic runtime mới. Nó chỉ đóng gói, giải thích và chứng minh hệ thống đã hoàn thành yêu cầu.

### Acceptance criteria cấp epic
- có đủ 3 file tài liệu
- người đọc hiểu được design và trade-offs
- AI usage được ghi minh bạch

### Spec đầu ra mong muốn
Một spec riêng cho Epic D cần mô tả rõ:
- cấu trúc từng file
- nội dung tối thiểu
- format benchmark report
- format AI usage disclosure

---

# 6) Thứ tự triển khai khuyến nghị
1. **Epic A — Ingestion**
2. **Epic B — Delivery pipeline**
3. **Epic C — Finalization & proof**
4. **Epic D — Delivery package**

Thứ tự này giúp tạo được một đường chạy end-to-end sớm:
- nhận message
- xử lý message
- ghi final result
- chứng minh kết quả bằng benchmark và tài liệu

---

# 7) Timeline 2 giờ
## 0–15 phút
- chốt epic scope
- chuyển Epic A thành spec đầu tiên
- xác định CLI contract và schema message

## 15–35 phút
- implement Epic A
- validation/normalization hoàn chỉnh

## 35–65 phút
- implement Epic B phần queue + worker
- thêm delivery simulation

## 65–85 phút
- implement retry/backoff và lifecycle state

## 85–105 phút
- implement Epic C
- writer JSONL exactly-once
- counters và summary

## 105–120 phút
- benchmark harness
- verify output integrity
- viết README/BENCHMARK/AI_USAGE

---

# 8) Rủi ro chính và cách giảm rủi ro
### Rủi ro 1: scope lan rộng khỏi 2 giờ
Giảm bằng cách giữ mọi spec ở mức MVP, không thêm persistence/database.

### Rủi ro 2: duplicate final rows
Giảm bằng dedup theo `message_id` ở tầng writer/aggregator và chỉ ghi final state một lần.

### Rủi ro 3: benchmark không đạt throughput
Giảm bằng JSONL append nhanh, batch processing, và tránh sleep/backoff quá nặng trong mô phỏng.

### Rủi ro 4: spec không đủ rõ để implement nhanh
Giảm bằng cách mỗi epic phải có rõ:
- mục tiêu
- ranh giới
- input/output
- acceptance criteria
- rules hành vi

---

# 9) Tiêu chí hoàn thành kế hoạch
Kế hoạch này đạt yêu cầu nếu:
- mỗi epic có thể được dùng làm đầu vào để viết spec riêng
- spec mỗi epic đủ rõ để implement mà không phải hỏi lại nhiều
- hệ thống cuối cùng có thể chạy end-to-end
- benchmark chạy bằng 1 lệnh
- output có đúng 1 final row per message
- tài liệu bắt buộc đầy đủ
- toàn bộ phạm vi vẫn khả thi trong 2 giờ
