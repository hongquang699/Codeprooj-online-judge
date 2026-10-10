# Terminal quản trị nội dung và chat

Chạy từ thư mục gốc dự án bằng tài khoản có quyền truy cập máy chủ và cơ sở dữ liệu. `--user` phải là username của một tài khoản Django đang hoạt động và có quyền staff.

Trong PowerShell, cài lệnh ngắn một lần:

```powershell
.\scripts\install-codepro-command.ps1
. $PROFILE
codepro
```

`codepro` chỉ mở khi thư mục hiện tại nằm trong project (kể cả thư mục con). Khi gọi không có `--user`, lệnh hỏi tên tài khoản quản trị. Có thể chạy trực tiếp `codepro --user admin status`. Ngoài project, lệnh báo lỗi và không kết nối cơ sở dữ liệu. Sau khi clone project ở chỗ khác, chạy lại script cài đặt để cập nhật đường dẫn.

```powershell
python manage.py site_terminal --user admin
```

Gõ `help` để xem lệnh. Phiên tương tác hỗ trợ:

```text
status
posts
show-post 12
edit-post 12 content C:\temp\new-body.txt
edit-post 12 title C:\temp\new-title.txt
chats
read 4
send username "Xin chào, chúng tôi đã nhận yêu cầu của bạn."
quit
```

Có thể chạy một lệnh rồi thoát, ví dụ `python manage.py site_terminal --user admin status`. Nội dung sửa bài viết được đọc từ tệp UTF-8 tối đa 1 MB. Việc sửa bài viết được ghi vào Django admin log. Tin nhắn lưu trong hệ thống chat hiện có và tạo thông báo cho người nhận. Lệnh `read` chỉ cho xem hội thoại có tài khoản staff đã chọn tham gia. Công cụ không chạy lệnh shell và không mở terminal qua web.
