Tổng quan chiến lược
Mục tiêu hệ thống
Xây dựng một Distributed Messaging Delivery Service có thể:

nhận 1,000,000 messages
xử lý async
retry khi fail tạm thời
ghi kết quả cuối cùng ra file
không duplicate final rows
chạy benchmark trong 10 phút
Nguyên tắc chia feature
Mỗi feature nên:

có spec riêng
có acceptance criteria riêng
có thể test độc lập
không phụ thuộc quá nhiều vào feature sau
Danh sách feature đề xuất
Feature 1 — Input contract & submission entrypoint
Mục tiêu: Có điểm vào hệ thống để submit message.

Phạm vi
CLI hoặc API nhận message
hỗ trợ import input từ file / generate test data
nhận đúng schema cơ bản của message
trả về xác nhận đã nhận message
Vì sao là feature đầu tiên
Không có entrypoint thì không có cách nào đưa messages vào hệ thống để test các phần sau.

Acceptance criteria
Người dùng submit được message hợp lệ
Message không hợp lệ bị từ chối rõ ràng
Có thể chạy từ command line
Có thể dùng làm nguồn dữ liệu cho benchmark
Spec cần mô tả
input format
fields bắt buộc
cách truyền dữ liệu
expected response / exit code
Feature 2 — Message schema validation & normalization
Mục tiêu: Mọi message vào hệ thống đều được chuẩn hóa và kiểm tra hợp lệ.

Phạm vi
validate message_id, recipient, channel, priority, content, created_at
chuẩn hóa dữ liệu đầu vào
xử lý thiếu field / sai kiểu / giá trị không hợp lệ
đảm bảo message có thể đi tiếp vào pipeline
Vì sao tách riêng
Validation là lớp bảo vệ đầu tiên. Nếu trộn với queue/worker thì spec sẽ khó rõ.

Acceptance criteria
Message hợp lệ đi tiếp
Message sai schema bị reject
Có lỗi rõ ràng cho từng loại invalid case
Spec cần mô tả
schema chuẩn
rule validation
normalization rule
behavior khi field thiếu hoặc sai format
Feature 3 — Queue/storage layer & message lifecycle state
Mục tiêu: Có nơi giữ message và theo dõi trạng thái lifecycle.

Phạm vi
queue hoặc queue-like mechanism
trạng thái message: pending / processing / retrying / delivered / failed
lưu trạng thái đủ để tránh mất message
hỗ trợ crash recovery ở mức cơ bản
Vì sao quan trọng
Đây là nền tảng để chứng minh “messages are not lost”.

Acceptance criteria
message được enqueue thành công
state chuyển đúng thứ tự
có thể query/tracking trạng thái hiện tại
restart không làm mất toàn bộ trạng thái nếu có persistence
Spec cần mô tả
data model của queue item
state machine
durability assumptions
recovery behavior
Feature 4 — Worker processing & delivery simulation
Mục tiêu: Xử lý message bất đồng bộ và mô phỏng delivery.

Phạm vi
worker pool
logic delivery giả lập success / temporary failure / permanent failure
xử lý song song
worker lấy message từ queue
Vì sao là feature riêng
Đây là lõi xử lý business, cần tách khỏi retry và output để dễ kiểm soát behavior.

Acceptance criteria
nhiều worker có thể chạy đồng thời
message được xử lý đúng
result trạng thái phản ánh đúng outcome giả lập
Spec cần mô tả
worker concurrency model
cách mô phỏng failure
rules chọn success/fail
giới hạn throughput target
Feature 5 — Retry policy with backoff and max-attempt tracking
Mục tiêu: Xử lý fail tạm thời bằng retry có kiểm soát.

Phạm vi
retry tối đa 3 lần
backoff tăng dần
đếm attempts
chuyển sang failed khi vượt ngưỡng
không ghi duplicate final result trong quá trình retry
Vì sao là feature riêng
Retry là yêu cầu quan trọng nhất về correctness trong bài này.

Acceptance criteria
temporary failure được retry
backoff tăng dần
max 3 attempts
permanent failed result sau tối đa số lần retry
retry không tạo final output trùng
Spec cần mô tả
retry state machine
backoff rule
attempt counting rule
final failure rule
Feature 6 — Final result writer with exactly-one-row guarantee
Mục tiêu: Ghi final result ra file, đảm bảo đúng một dòng cuối cùng cho mỗi message.

Phạm vi
output file writer
JSONL/CSV/plain text
append-only hoặc buffered write
dedup final write theo message_id
flush/close an toàn
Vì sao là feature riêng
Đây là phần trực tiếp ảnh hưởng đến benchmark và tiêu chí pass/fail.

Acceptance criteria
mỗi message đúng 1 final row
không duplicate final rows
output file có thể kiểm tra được
writer ổn định khi throughput cao
Spec cần mô tả
output format
write guarantee
dedup strategy
flush policy
Feature 7 — Logging, counters, and observability
Mục tiêu: Có đủ thông tin để chứng minh hệ thống hoạt động đúng.

Phạm vi
basic logging
counters: submitted, processed, retry, delivered, failed, duplicate_prevented
progress metrics
benchmark-visible summary
Vì sao cần sớm
Không có metrics thì không chứng minh được benchmark và cũng khó debug.

Acceptance criteria
có log cho lifecycle chính
có counters tổng hợp
benchmark report có thể lấy số liệu từ đây hoặc từ summary file
Spec cần mô tả
metric names
logging granularity
output summary format
what to log / what not to log
Feature 8 — Benchmark harness and proof report
Mục tiêu: Chứng minh hệ thống hoàn thành 1,000,000 messages trong 10 phút.

Phạm vi
command benchmark 1 bước
generate 1M messages
run clean start
collect duration / throughput / retries / duplicates / losses
validate output file
Vì sao là feature quan trọng nhất
Đây là “proof” của bài test. Không có feature này thì chưa thể chứng minh đã hoàn thành yêu cầu.

Acceptance criteria
chạy được bằng 1 command
benchmark reproducible
report đủ thông số
output row count đúng
duration ≤ 10 phút
Spec cần mô tả
benchmark command
input generation
validation checks
required report fields
pass/fail rule
Feature 9 — Documentation and AI usage report
Mục tiêu: Hoàn thiện bài nộp theo đúng đề.

Phạm vi
README.md
BENCHMARK.md
AI_USAGE.md
mô tả kiến trúc, trade-offs, bottleneck
Vì sao là feature riêng
Đề bài yêu cầu rõ phần documentation và AI usage, nên nên coi như feature cuối.

Acceptance criteria
người khác đọc hiểu design
benchmark report đúng format
AI usage ghi rõ tool, prompt, phần nào AI hỗ trợ
Spec cần mô tả
tài liệu nào phải có
nội dung tối thiểu
format report
Thứ tự triển khai đề xuất
Mình khuyên đi theo thứ tự này:

Feature 1 — Input contract & entrypoint
Feature 2 — Validation & normalization
Feature 3 — Queue/storage & lifecycle state
Feature 4 — Worker processing
Feature 5 — Retry & backoff
Feature 6 — Final result writer
Feature 7 — Logging & observability
Feature 8 — Benchmark harness
Feature 9 — Documentation
Feature grouping theo spec-driven development
MVP slice
Nếu muốn có một bản chạy được sớm, MVP nên gồm:

Feature 1
Feature 2
Feature 3
Feature 4
Feature 6
Tức là:

nhận input
validate
enqueue
process
ghi final result
Sau đó mới thêm:

Feature 5 retry
Feature 7 observability
Feature 8 benchmark
Feature 9 docs
