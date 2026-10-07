# CODING_OJ - Hệ Thống Chấm Bài & Luyện Lập Trình Thi Đấu Trực Tuyến
> Nền tảng luyện thi Olympic Tin học, HSG Quốc Gia và ICPC thế hệ mới theo chuẩn VNOI, Codeforces và DMOJ.

---

## 📁 Cấu Trúc Thư Mục Chuẩn Hóa Của Dự Án

```text
HQ/
├── apps/                         # Các ứng dụng và tiến trình dịch vụ Node.js
│   ├── web/                      # Web Gateway, định tuyến URL sạch và bảo mật WAF
│   │   ├── server.js             # HTTP Reverse Proxy & Static File Server (Port 8888)
│   │   └── security.js           # Bộ lọc WAF, chống DDoS, Rate Limit, Anti-Bot & Threat Jail
│   ├── admin/                    # Tiến trình nền quản trị và giám sát cụm
│   └── worker/                   # Background Task Daemon (xử lý queue, dọn dẹp)
│
├── backend/                      # Mã nguồn trung tâm Django 5 REST Framework
│   ├── core/                     # Cấu hình chính (settings.py, urls.py, wsgi.py)
│   ├── api/                      # REST API Endpoints v1 & v2 (/api/v2/*)
│   ├── judge/                    # Core Database Models (Problem, Submission, Contest, Profile)
│   ├── auth/                     # Phân hệ xác thực đa lớp (Session, Token, 2FA TOTP, Crypto Hash)
│   ├── community/                # Diễn đàn, bình luận và thảo luận
│   ├── ranking/                  # Thuật toán tính toán Rating Elo & Bảng xếp hạng
│   ├── users/                    # Quản lý người dùng, phân quyền và profile
│   └── moderation/               # Hệ thống báo cáo vi phạm và kỷ luật tài khoản
│
├── frontend/                     # Toàn bộ giao diện người dùng (UI / UX)
│   ├── html/                     # Các trang web HTML theo từng phân hệ chức năng
│   │   ├── home/                 # Trang chủ giới thiệu và thống kê nền tảng
│   │   ├── problem/              # Danh sách bài tập, chi tiết đề bài và nộp bài
│   │   ├── contest/              # Phòng thi đấu, bảng điểm trực tiếp và thông báo
│   │   ├── submission/           # Danh sách bài nộp, mã nguồn và kết quả testcase
│   │   ├── ranking/              # Bảng xếp hạng toàn cầu, trường học và rating
│   │   ├── learning/             # Thư viện thuật toán VNOI Wiki (DP, Graph, Cây, STL,...)
│   │   ├── community/            # Diễn đàn thảo luận và nhóm học tập
│   │   ├── blog/                 # Blog chia sẻ giải thuật và Studio soạn thảo Markdown
│   │   ├── teacher/              # Cổng giáo viên: quản lý lớp, giao bài tập, xuất điểm
│   │   ├── admin/                # Bảng điều khiển quản trị toàn diện (VNOI Standard)
│   │   └── auth/                 # Đăng nhập, đăng ký, xác thực 2FA và kích hoạt email
│   ├── css/                      # Hệ thống CSS module hóa, Dark Mode và Responsive
│   └── js/                       # Core API Client, Auth State, Components và Utilities
│
├── judge-system/                 # Cụm máy chấm phân tán (Distributed Judge Cluster)
│   ├── judge-server/             # Judge Coordinator & Heartbeat Manager (Port 9999)
│   ├── judging/                  # Bộ biên dịch (Compiler) & thực thi (Executor)
│   ├── sandbox/                  # Cơ chế cách ly tài nguyên, SecurityScanner chặn mã độc
│   ├── checker/                  # Bộ so khớp đáp án chuẩn và Custom Testlib
│   └── validator/                # Bộ thẩm định dữ liệu đầu vào testcase
│
├── security/                     # Lớp phòng thủ an ninh mạng tích hợp
│   ├── middleware.py             # FullSecurityMiddleware (WAF, Anti-Spoofing, CORS, Rate Limit)
│   ├── api_security/             # Bảo vệ API, Input Sanitizer (chống SQLi, XSS, CSRF)
│   └── incident_response/        # Quản lý IP blacklist, khóa khẩn cấp
│
├── scripts/                      # Bộ công cụ vận hành & bảo vệ mã nguồn
│   ├── protect_frontend.js       # Script làm rối (obfuscate), nén & bảo vệ mã JavaScript
│   └── protect_backend.py        # Script biên dịch bytecode (.pyc) & kiểm toán rò rỉ mã nguồn
│
├── database/                     # Cơ sở dữ liệu và kịch bản khởi tạo
│   ├── vnoi_db.sqlite3           # CSDL SQLite mặc định cho môi trường phát triển cục bộ
│   ├── schemas/                  # Bản vẽ cấu trúc bảng SQL chuẩn cho PostgreSQL / MySQL
│   └── seeds/                    # Dữ liệu bài tập mẫu và tài khoản ban đầu
│
├── problems/ & problem-data/     # Kho bài toán và bộ testcase chuẩn hóa Polygon
├── storage/                      # Dữ liệu upload, mã nguồn thí sinh nộp và log chấm
│
├── tests/                        # Hệ thống kiểm thử tự động (Unit, API, Integration, Security)
│   ├── security/                 # Kiểm thử SQLi, XSS, CSRF, RCE, Anti-Spoofing & Leak Prevention
│   └── integration/              # Kiểm thử luồng thi đấu và bảng điểm
│
├── docker-compose.yml            # Cấu hình Docker Compose; cần rà soát trước khi triển khai
├── HUONG_DAN_DEPLOY_VPS.txt      # Hướng dẫn chi tiết triển khai lên máy chủ VPS từ A-Z
├── manage.py                     # CLI điều hành Django
├── package.json                  # Cấu hình dự án Node.js & các scripts vận hành
└── requirements.txt              # Danh sách thư viện Python cần thiết
```

### Bộ test và chấm điểm theo nhóm

Gói bài trong `problem-data/problems/{CODE}/` có thể khai báo thứ tự, trọng số, nhóm subtask và test ví dụ trong `testcases.json`:

```json
{
  "cases": [
    {"id": "01", "points": 10, "subtask": 1, "sample": true},
    {"id": "02", "points": 20, "subtask": 1},
    {"id": "s2_01", "points": 30, "subtask": 2}
  ],
  "subtasks": [
    {"id": 1, "points": 30, "scoring_method": "all_or_nothing", "depends_on": []},
    {"id": 2, "points": 70, "scoring_method": "all_or_nothing", "depends_on": [1]}
  ]
}
```

Mỗi `id` khớp tên file `.in`/`.out` trong `cases/`. API soạn đề tự ghi manifest khi thêm/xóa test; ZIP cũ vẫn được nhập với điểm mặc định 10 cho mỗi testcase. Bài cũ không có manifest tiếp tục được đọc theo tên file và trọng số mặc định. `scoring_method` hỗ trợ `all_or_nothing`, `sum` và `min`; `depends_on` liệt kê các nhóm phải đạt điểm trước.

Lời giải mẫu được đưa vào queue của Judge Manager và chạy trên worker/sandbox giống lượt chấm bài. Django chỉ gửi mã nguồn và nhận `job_id`; nó không biên dịch hay thực thi mã lời giải trong web process. Worker phải mount cùng thư mục `problem-data/problems` để đọc testcase và cấu hình mới.

Bài `000` (`A + B - C`) hiện có 15 ca hợp lệ theo giới hạn `-10..10`: hai ví dụ được đánh dấu sample, các ca còn lại tập trung vào dấu âm và giá trị biên; trọng số testcase bí mật cộng thành 100 điểm trong subtask 1.

---

## 🛡️ Bảo mật và phạm vi bảo vệ

Dự án có các lớp kiểm tra quyền, giới hạn request và bảo vệ tài nguyên tĩnh. Các lớp này chưa tương đương với một cuộc kiểm toán bảo mật hoàn chỉnh.

- **Tài nguyên tĩnh:** gateway giới hạn đường dẫn phục vụ trong `frontend/`, cùng một số file gốc được cho phép như favicon; chặn nhiều đuôi file nhạy cảm và source map. JavaScript gửi xuống trình duyệt vẫn có thể đọc được; làm rối mã và chặn DevTools không phải cơ chế bảo mật dữ liệu.
- **Trang quản trị:** gateway xác minh session qua Django và áp dụng `config/admin_ip_whitelist.json`. Whitelist bị tắt, thiếu hoặc không đọc được sẽ từ chối truy cập admin tại gateway. Cookie tự khai báo `role=admin` không thay thế session hợp lệ.
- **Judge Admin:** Django kiểm tra quyền staff/superuser, nhóm `judge_admin` / `judge_manager` hoặc profile role tương ứng. API ghi dữ liệu bằng cookie `cp_session` yêu cầu CSRF token. API quản trị Judge cũng hỗ trợ DRF token.
- **API quản trị v2:** các API quản lý quyền người dùng, cấu hình hệ thống và quản lý kỳ thi đã bổ sung kiểm tra tài khoản active có quyền staff/superuser.
- **Hồ sơ người dùng v2:** danh sách và trang hồ sơ công khai không trả email, trạng thái tài khoản hoặc cờ quyền nội bộ; chủ tài khoản và staff/superuser vẫn xem được thông tin đầy đủ. Tìm người dùng bằng email chỉ dành cho staff/superuser. Đăng nhập bằng email hoặc tên không phân biệt chữ hoa chữ thường từ chối tài khoản đã bị vô hiệu hóa.
- **Đăng ký và đăng nhập:** API đăng ký v1/v2 cùng dùng quy trình OTP email, chỉ cấp tài khoản sau khi xác minh. API đăng nhập v2 dùng kiểm soát đăng nhập chung; tài khoản quản trị hoặc bật 2FA phải hoàn tất đăng nhập tại `/api/v1/auth/login`. Bước 2FA yêu cầu cookie thử thách ký số có hạn 5 phút sau khi nhập đúng mật khẩu và giới hạn lần nhập mã sai. Quyền admin dựa trên cờ staff/superuser đang hoạt động, không dựa vào tên tài khoản; session của tài khoản bị vô hiệu hóa cũng bị thu hồi.
- **Phản hồi gateway:** đường dẫn và IP được thoát ký tự trước khi đưa vào trang lỗi HTML; URL sai mã hóa nhận phản hồi 400.
- **API v2:** thao tác tạo/sửa bài, testcase, kỳ thi và blog yêu cầu staff/superuser. Nộp bài, đăng ký thi, bình luận và gửi câu hỏi dùng danh tính đã xác thực thay vì trường `user` do trình duyệt gửi. Endpoint heartbeat yêu cầu `JUDGE_AUTH_TOKEN`; worker cần nhận cùng biến môi trường. File ZIP testcase chỉ nhận file `.in`/`.out` ở thư mục gốc, tối đa 1.000 file và 100 MiB sau giải nén.
- **Cài đặt tài khoản:** đổi mật khẩu cần nhập mật khẩu hiện tại; quản trị viên vẫn có thể đặt lại mật khẩu qua trang quản trị. API hỗ trợ `Token`, `Bearer` và cookie `cp_session`; yêu cầu CSRF khi ghi bằng cookie.
- **API soạn đề và thi đấu v1:** thao tác soạn đề, quản lý testcase và lời giải yêu cầu staff/superuser; dữ liệu testcase và lời giải chỉ trả về cho quản trị viên. Danh tính thí sinh lấy từ phiên/token đã xác thực. Khi chấm lỗi, bài thi nhận trạng thái lỗi hệ thống để chấm lại, không tạo kết quả AC giả. Tên file trong gói đề và ZIP testcase được giới hạn để tránh ghi ra ngoài thư mục bài.
- **Nộp bài và chấm lại:** các API nộp bài yêu cầu tài khoản đang hoạt động, giới hạn mã nguồn 64 KiB và chỉ dùng ngôn ngữ đang bật. Bài trong kỳ thi phải thuộc kỳ thi đang mở, thí sinh phải đăng ký và không bị loại; kỳ thi nội bộ chỉ nhận thành viên tổ chức. API chấm lại v1/v2 chỉ dành cho Judge Admin/Manager và ghi audit log.
- **Chi tiết bài nộp:** người lạ vẫn xem được kết quả tổng hợp; mã nguồn, log biên dịch và chi tiết testcase chỉ trả về cho tác giả hoặc staff. Giao diện chạy thử với input tùy chỉnh hiện chưa hỗ trợ và không gửi bài nộp thật.
- **Thanh điều hướng trang nộp bài:** các đường dẫn nộp bài dùng chung navbar theo phiên đăng nhập, nên khi chuyển từ trang bài tập sang trang nộp bài vẫn hiển thị tài khoản hiện tại.
- **Nút hồ sơ trên thanh điều hướng:** avatar màu thương hiệu và tên tài khoản có độ tương phản rõ ở giao diện sáng/tối; nút được thu gọn, có trạng thái hover/focus và giới hạn tên dài trên màn hình nhỏ. Màu xếp hạng vẫn hiển thị ở trang hồ sơ, không dùng để tô chữ tên trên thanh điều hướng.
- **Chiều rộng thanh điều hướng:** nội dung navbar trải theo toàn bộ chiều rộng màn hình, với khoảng đệm hai bên linh hoạt thay cho giới hạn 1440px.
- **Trang danh sách dữ liệu:** lịch sử nộp bài, bảng xếp hạng và kho bài tập dùng chiều rộng màn hình với khoảng đệm linh hoạt; bảng cuộn ngang trên màn hình hẹp để các cột không bị bóp méo.
- **Cộng đồng:** thao tác đăng bài, bình luận, nhắn tin, theo dõi và kiểm duyệt dùng tài khoản đã xác thực; danh sách tin nhắn và thông báo chỉ dành cho chủ tài khoản. Gửi tin nhắn yêu cầu người gửi thuộc cuộc trò chuyện. Feed, tìm kiếm và hồ sơ công khai không trả email hoặc cờ quyền nội bộ.
- **Quản trị cuộc thi và tổ chức:** API không nhận `X-Username` hoặc `user` trong query để xác định người thao tác. Quyền quản lý cuộc thi dựa trên staff, chủ tổ chức hoặc vai trò được gán cho cuộc thi; danh sách quản trị chỉ hiển thị cuộc thi người dùng có quyền xem. Tên tài khoản không tự cấp quyền admin; chỉ staff có thể xác minh tổ chức mới tạo.
- **Quyền trên giao diện tổ chức:** API chi tiết tổ chức trả `can_manage` theo quyền `organization.edit` của tài khoản đã xác thực. Trang công khai, tổng quan và các trang quản trị dùng cờ này, không dùng vai trò hoặc tên lưu trong `localStorage`. Quyền tạo tổ chức vẫn dành cho staff/superuser hoặc giáo viên, không dựa vào nhãn profile `admin` đơn lẻ.
- **Menu tổ chức:** Menu Admin tải các tổ chức có thể quản trị từ API để chọn, thay cho đường dẫn gắn cứng tới `vnoi` (có thể không tồn tại trong cơ sở dữ liệu). Trang tổng quan phân biệt tổ chức không tồn tại, lỗi tải và thiếu quyền. API đọc thử lại bằng phiên cookie khi token lưu trong trình duyệt hết hạn. Khi mở file HTML quản trị trực tiếp bằng `file://`, trang chuyển sang gateway `localhost:8888` để CSS, JavaScript và API hoạt động đúng.
- **Quyền quản trị hệ thống:** staff/superuser đang hoạt động có quyền quản lý mọi tổ chức, cuộc thi và Judge Admin. Các trang admin xác nhận quyền bằng phiên hiện tại từ `/api/v1/auth/me` thay cho vai trò cũ trong `localStorage`; khi đổi tài khoản, token lưu của tài khoản trước được bỏ và navbar đồng bộ theo phiên mới. Trang tổ chức hiển thị vai trò quản trị hệ thống ngay cả khi admin chưa là thành viên; nút tạo tổ chức dùng quyền từ phiên hiện tại. Các API đọc của tổ chức/Menu Admin ưu tiên phiên cookie trước token lưu. API `/auth/me` cấp CSRF cookie để thao tác ghi bằng phiên hiện tại hoạt động sau khi bỏ token cũ.
- **Trạng thái Judge trong Menu Admin:** lấy từ API sức khỏe Judge cùng origin và token đăng nhập; trước khi có phản hồi hiển thị “Đang kiểm tra”, không mặc định báo ONLINE.
- **Khi phát triển cục bộ:** nếu chạy Django bằng `runserver --noreload`, phải khởi động lại backend sau khi cập nhật code; nếu không API vẫn dùng phiên bản cũ dù HTML/CSS mới đã hiện trên cổng 8888.
- **Các trang nộp bài cũ:** nút chạy thử với input riêng từng tạo bài nộp thật dù không dùng input đó; các trang này nay thông báo chưa hỗ trợ. API cộng đồng và tổ chức mặc định dùng cùng origin với website.
- **IP và proxy:** gateway mặc định chỉ tin header IP từ loopback và chuyển IP đã xác minh tới Django. Django chỉ nhận `X-Real-IP` từ địa chỉ proxy được liệt kê trong `TRUSTED_PROXY_IPS`, mặc định là loopback; không dùng header chuyển tiếp do client tự khai báo để quyết định quyền admin.
- **Chấm bài:** Django gửi bài tới Judge Manager và không biên dịch/thực thi mã thí sinh trong web process. Khi manager không phản hồi, bài được ghi lỗi hệ thống để chấm lại. Bộ quét mã tĩnh chỉ là một lớp hỗ trợ, không thay thế sandbox và cách ly worker.

**Trước khi triển khai công khai:** Docker Compose chạy với `DEBUG=False` và yêu cầu các secret riêng trong `.env`; không dùng `.env.example` làm cấu hình thật. Cấu hình Compose hiện publish cổng PostgreSQL, Redis và backend ra host, vì vậy cần giới hạn firewall hoặc bỏ publish các cổng nội bộ. Tiếp tục rà soát phân quyền và CSRF của các API còn lại. Không coi các bộ test hiện có là xác nhận toàn bộ hệ thống an toàn.

---

## 🧰 Các Lệnh Vận Hành & Bảo Vệ Mã Nguồn

### 1. Làm rối & Bảo vệ mã nguồn Frontend JavaScript
```bash
# Xem trạng thái bảo vệ hiện tại của 107 file JS frontend
npm run status:protection

# Thực hiện nén, xóa chú thích/console.log và làm rối mã nguồn (tự động tạo backup an toàn)
npm run build:obfuscate

# Khôi phục lại toàn bộ mã nguồn JS gốc từ bản backup khi cần phát triển tiếp
npm run restore:frontend
```

### 2. Kiểm toán & Đóng gói Bytecode Backend Python
```bash
# Biên dịch mã nguồn Python trong dự án thành bytecode (.pyc)
npm run protect:backend
# hoặc:
python scripts/protect_backend.py --compile

# Rà soát an ninh file tĩnh và nguy cơ lộ tệp nhạy cảm
python scripts/protect_backend.py --audit

# Kiểm tra tính toàn vẹn cú pháp của toàn bộ file Python
python scripts/protect_backend.py --check
```

### 3. Chạy Kiểm Thử An Ninh Mạng & Tính Năng Hệ Thống
```bash
# Chạy bộ test chuyên dụng kiểm tra chống RCE, bảo vệ bài nộp & chống IP Spoofing
python manage.py test tests.security.test_source_protection_and_hardening

# Chạy test kiểm tra cô lập tài nguyên tĩnh & chống lộ file trên Web Gateway
node tests/security/test_web_server_security.js

# Kiểm tra quyền riêng tư API v2, đăng nhập tài khoản bị vô hiệu hóa và phản hồi gateway
python manage.py test backend.judge.tests_security_v2 backend.judge.tests_admin
npx jest tests/security/test_gateway_response_security.test.js --runInBand

# Chạy các test trong thư mục tests
python manage.py test tests
```

---

## 🚀 Khởi động trên máy cục bộ

Chạy các lệnh từ thư mục gốc `HQ/`. Cần Python, Node.js và compiler/runtime tương ứng với ngôn ngữ chấm bài. Cài thư viện Python trong môi trường ảo và chuẩn bị database trước:

```bash
python -m pip install -r requirements.txt
# Sao chép .env.example thành .env rồi điền các secret ngẫu nhiên (xem bên dưới).
python manage.py migrate
# Chỉ tạo tài khoản quản trị khi chưa có:
python manage.py createsuperuser
```

Sao chép `.env.example` thành `.env` và điền secret ngẫu nhiên riêng cho `SECRET_KEY`, `JUDGE_AUTH_TOKEN`, `JUDGE_SECRET_TOKEN`, `DJANGO_SECRET_KEY`, `JWT_SECRET`, cùng mật khẩu `DB_PASSWORD`. Có thể tạo từng giá trị bằng `python -c "import secrets; print(secrets.token_urlsafe(48))"`. Không dùng lại token từ README, YAML hoặc ví dụ trên mạng.

Sao chép `config/admin_ip_whitelist.example.json` thành `config/admin_ip_whitelist.json` trước khi mở trang quản trị. File thật chứa IP vận hành và được loại khỏi Git; mẫu chỉ cho phép loopback.

Mở ba terminal riêng, chạy lần lượt:

| Dịch vụ | Lệnh | Cổng mặc định |
| --- | --- | --- |
| Django API | `python manage.py runserver 127.0.0.1:8000` | 8000 |
| Judge Manager và embedded workers | `python judge-system/judge-server/main.py` | 9999 |
| Web gateway | `node apps/web/server.js` | 8888 |

`npm start` hiện trỏ tới backend Node cũ (`backend/server.js`), không phải gateway của luồng Django ở trên.

- Trang chính: [localhost:8888](http://localhost:8888).
- Quản trị chung: [localhost:8888/admin](http://localhost:8888/admin).
- Máy chấm: [localhost:8888/admin/judge](http://localhost:8888/admin/judge).
- API bài tập: [localhost:8000/api/v2/problems](http://localhost:8000/api/v2/problems).
- Health của Judge Manager: [127.0.0.1:9999/api/v1/health](http://127.0.0.1:9999/api/v1/health).

Gateway dùng `DJANGO_BACKEND_HOST`, `DJANGO_BACKEND_PORT` và `PORT` để đổi địa chỉ/cổng. Django dùng `JUDGE_SERVER_URL` và `JUDGE_AUTH_TOKEN` để kết nối Judge Manager; token phải khớp cấu hình manager. Khai báo biến môi trường trong terminal hoặc service launcher, không giả định mọi tiến trình đều tự nạp `.env`.

## ⚙️ Judge Admin và cập nhật dịch vụ

Luồng dữ liệu: trình duyệt → API Django `/api/v1/admin/judge/*` → Judge Manager `/api/v1/*` → hàng đợi → worker → sandbox.

Portal có dashboard, workers, queue, submissions, languages, monitoring, logs và công cụ gửi bài thử. Gateway chuyển `/admin/judge` và các trang con tới Django để kiểm tra quyền rồi trả về `portal.html`. Danh sách worker đến từ heartbeat; entrypoint hiện khởi chạy các embedded worker theo `judge-system/config/workers.yml`. Xem thêm [hướng dẫn Judge Admin](docs/judge-admin.md).

Sau khi thay đổi mã:

1. Với `apps/web/*.js`, khởi động lại tiến trình gateway bằng lệnh ở bảng trên.
2. Với `judge-system/`, kiểm tra hàng đợi và các job đang chạy; chờ xử lý xong rồi khởi động lại Judge Manager. Queue và result cache hiện nằm trong bộ nhớ, nên khởi động lại có thể mất trạng thái chưa được lưu.
3. Django `runserver` thường tự nạp lại mã; nếu dùng service production, cần khởi động lại service đó. Chạy migrations khi có thay đổi schema.
4. Tải lại trang bằng Ctrl+F5 sau khi dịch vụ đã lên.

| Hiện tượng | Kiểm tra và cách xử lý |
| --- | --- |
| Chỉ thấy “Mở Judge Admin”, trang liên tục chuyển hướng | Gateway có thể còn chạy mã cũ và phục vụ file redirect. Khởi động lại gateway để nạp route tới portal. |
| `Endpoint not found: GET /api/v1/admin/queue` | Judge Manager có thể chưa nạp router mới. Kiểm tra queue/job trước khi khởi động lại manager. Đây là endpoint nội bộ mà Django gọi. |
| Chuyển về trang đăng nhập hoặc báo 403 | Kiểm tra session, quyền Judge Admin/Judge Manager và IP whitelist của gateway. |
| `Judge Manager is unavailable` | Kiểm tra manager cổng 9999, `JUDGE_SERVER_URL` và log dịch vụ. |
| Manager báo 401 | Kiểm tra `JUDGE_AUTH_TOKEN` giữa Django và manager; không đưa token dịch vụ vào frontend. |

Các kiểm tra tập trung cho Judge Admin:

```bash
python manage.py test backend.judge.tests_admin
python -m unittest discover -s judge-system/tests -p test_admin_control.py
```

## 🌐 Triển khai VPS / server

Xem [hướng dẫn triển khai](HUONG_DAN_DEPLOY_VPS.txt). Cấu hình Docker/Nginx cần được đối chiếu với các cổng thực tế ở trên và các điểm bảo mật còn tồn tại trước khi đưa ra Internet.
