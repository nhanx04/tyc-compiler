# Dự án Trình biên dịch TyC

Một triển khai trình biên dịch toàn diện cho **TyC**, một ngôn ngữ lập trình đơn giản kiểu C với **suy luận kiểu hoàn chỉnh**, sử dụng trình sinh parser ANTLR4.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![ANTLR](https://img.shields.io/badge/ANTLR-4.13.2-orange.svg)](https://www.antlr.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

## Tổng quan

Đây là một mini project cho môn học **Nguyên lý Ngôn ngữ Lập trình** (Principles of Programming Languages) nhằm xây dựng một trình biên dịch cho **TyC**, một ngôn ngữ lập trình tùy biến kiểu C được thiết kế cho mục đích giáo dục.

📋 **Để xem đặc tả ngôn ngữ chi tiết, xem [Đặc tả TyC](tyc_specification.md)**

Dự án minh họa các khái niệm nền tảng của việc xây dựng trình biên dịch, bao gồm:

- **Phân tích từ vựng (Lexical Analysis)**: Tách token và xử lý lỗi cho ký tự không hợp lệ, chuỗi chưa đóng, và chuỗi escape không hợp lệ
- **Phân tích cú pháp (Syntax Analysis)**: Phân tích dựa trên ngữ pháp bằng ANTLR4 (ANother Tool for Language Recognition)
- **Sinh AST (AST Generation)**: Xây dựng cây cú pháp trừu tượng từ cây phân tích (parse tree)
- **Phân tích ngữ nghĩa (Semantic Analysis)**: Hệ suy luận kiểu hoàn chỉnh kèm kiểm tra kiểu tĩnh
- **Sinh mã (Code Generation)**: Sinh mã đích từ AST đã được kiểm tra hợp lệ
- **Xử lý lỗi (Error Handling)**: Báo lỗi đầy đủ cho mọi giai đoạn biên dịch
- **Khung kiểm thử (Testing Framework)**: Kiểm thử tự động kèm sinh báo cáo HTML

---

## Bài tập 1 - Phân tích từ vựng và Phân tích cú pháp

### Các yêu cầu cần hoàn thành

1. **Đọc kỹ đặc tả ngôn ngữ**
   - Nghiên cứu tài liệu [Đặc tả TyC](tyc_specification.md)
   - Hiểu cú pháp và ngữ nghĩa của ngôn ngữ TyC
   - Nắm vững các quy tắc từ vựng và cú pháp

2. **Cài đặt file TyC.g4**
   - Hoàn thiện file ngữ pháp ANTLR4 tại `src/grammar/TyC.g4`
   - Định nghĩa các luật từ vựng (token)
   - Định nghĩa các luật parser (luật ngữ pháp)
   - Xử lý độ ưu tiên và tính kết hợp (associativity)

3. **Viết 100 bài test lexer và 100 bài test parser**
   - **100 test case cho lexer** trong `tests/test_lexer.py`
     - Kiểm thử token hợp lệ và không hợp lệ
     - Kiểm thử xử lý lỗi (chuỗi chưa đóng, chuỗi escape không hợp lệ, ...)
     - Kiểm thử các trường hợp biên và edge case
   - **100 test case cho parser** trong `tests/test_parser.py`
     - Kiểm thử các cấu trúc ngữ pháp hợp lệ
     - Kiểm thử lỗi cú pháp và phục hồi lỗi
     - Kiểm thử cấu trúc lồng nhau và biểu thức phức tạp

### Yêu cầu xử lý lỗi từ vựng

Với các lỗi từ vựng, lexer phải trả về các token sau với lexeme cụ thể:

- **ERROR_TOKEN** với lexeme `<unrecognized char>`: khi lexer phát hiện ký tự không nhận diện được.

- **UNCLOSE_STRING** với lexeme `<unclosed string>`: khi lexer phát hiện chuỗi chưa được kết thúc. Lexeme `<unclosed string>` không bao gồm dấu ngoặc kép mở.

- **ILLEGAL_ESCAPE** với lexeme `<wrong string>`: khi lexer phát hiện escape không hợp lệ trong chuỗi. “Wrong string” tính từ đầu chuỗi (không bao gồm dấu ngoặc kép mở) cho đến escape không hợp lệ.

### Tiêu chí đánh giá

- **Cài đặt ngữ pháp**: Độ chính xác và mức độ đầy đủ của file `TyC.g4`
- **Độ phủ kiểm thử**: Số lượng và chất lượng test case (tổng 200 test)
- **Xử lý lỗi**: Khả năng xử lý lỗi từ vựng và cú pháp

---

## Bài tập 2 - Sinh AST

### Các yêu cầu cần hoàn thành

1. **Nghiên cứu cấu trúc node AST**
   - Đọc kỹ toàn bộ các lớp node trong `src/utils/nodes.py`
   - Hiểu hệ phân cấp node AST và các thuộc tính
   - Nắm được cách các cấu trúc ngôn ngữ ánh xạ sang node AST

2. **Cài đặt lớp ASTGeneration**
   - Tạo lớp `ASTGeneration` trong `src/astgen/ast_generation.py`
   - Kế thừa từ `TyCVisitor` (được sinh từ ANTLR4)
   - Override các phương thức visitor để tạo ra node AST phù hợp
   - Xử lý tất cả cấu trúc ngôn ngữ được định nghĩa trong đặc tả TyC

3. **Viết test case cho sinh AST**
   - Cài đặt test trong `tests/test_ast_gen.py`
   - Kiểm thử sinh AST cho tất cả tính năng ngôn ngữ
   - Xác minh đúng loại node và cấu trúc
   - Kiểm thử edge case và cấu trúc lồng nhau phức tạp

### Yêu cầu đối với sinh AST

Lớp `ASTGeneration` phải:

- **Kế thừa từ TyCVisitor**: Dùng visitor pattern để duyệt parse tree
- **Trả về node AST**: Mỗi phương thức `visit...` phải trả về đối tượng node tương ứng từ `nodes.py`
- **Hỗ trợ toàn bộ cấu trúc**: Hỗ trợ tất cả tính năng ngôn ngữ định nghĩa trong grammar
- **Giữ đúng cấu trúc**: Bảo toàn cấu trúc logic và quan hệ giữa các thành phần ngôn ngữ

### Tiêu chí đánh giá

- **Cài đặt AST**: Đúng và đầy đủ của lớp `ASTGeneration`
- **Sử dụng node**: Dùng đúng các lớp node trong `nodes.py`
- **Độ phủ kiểm thử**: Chất lượng và mức độ bao phủ của test case sinh AST
- **Độ chính xác cấu trúc**: AST phải biểu diễn đúng cấu trúc chương trình nguồn

---

## Cấu trúc dự án

```
.
├── Makefile              # Tự động hóa build đa nền tảng
├── run.py                # Điểm vào chính của dự án
├── README.md             # Tài liệu dự án
├── requirements.txt      # Phụ thuộc Python
├── tyc_specification.md  # Đặc tả ngôn ngữ
├── external/             # Phụ thuộc bên ngoài
│   └── antlr-4.13.2-complete.jar
├── src/                  # Mã nguồn
│   ├── astgen/           # Module sinh AST
│   │   ├── __init__.py   # Khởi tạo package
│   │   └── ast_generation.py # Cài đặt lớp ASTGeneration
│   ├── grammar/          # Định nghĩa ngữ pháp
│   │   ├── TyC.g4        # Đặc tả ngữ pháp ANTLR4
│   │   └── lexererr.py   # Các lớp lỗi lexer tùy biến
│   └── utils/            # Module tiện ích
│       ├── error_listener.py
│       ├── nodes.py      # Định nghĩa lớp node AST
│       └── visitor.py    # Các lớp visitor cơ sở
└── tests/                # Bộ kiểm thử
    ├── test_lexer.py     # Test lexer
    ├── test_parser.py    # Test parser
    ├── test_ast_gen.py   # Test sinh AST
    └── utils.py          # Tiện ích kiểm thử
```

## Bắt đầu nhanh

### Yêu cầu trước

- **Python 3.12+** (khuyến nghị) hoặc Python 3.8+
- **Java Runtime Environment (JRE) 8+** (cần cho ANTLR4)

### Cài đặt

1. **Clone repository:**

   ```bash
   cd TyC-compiler
   ```

2. **Kiểm tra yêu cầu hệ thống:**

   ```bash
   python3 run.py check
   ```

3. **Thiết lập môi trường:**

   ```bash
   python3 run.py setup
   ```

4. **Kích hoạt virtual environment:**

   ```bash
   # Trên macOS/Linux:
   source venv/bin/activate

   # Trên Windows:
   venv\Scripts\activate
   ```

5. **Build trình biên dịch:**

   ```bash
   python3 run.py build
   ```

6. **Chạy test:**
   ```bash
   python3 run.py test-lexer
   python3 run.py test-parser
   python3 run.py test-ast
   ```

## Các lệnh hiện có

- `python3 run.py setup` - Cài dependencies và thiết lập môi trường
- `python3 run.py build` - Biên dịch các file grammar ANTLR
- `python3 run.py check` - Kiểm tra các công cụ cần thiết đã được cài
- `python3 run.py test-lexer` - Chạy test lexer
- `python3 run.py test-parser` - Chạy test parser
- `python3 run.py test-ast` - Chạy test sinh AST
- `python3 run.py clean` - Dọn file build

## Giấy phép

Dự án này được phát triển cho mục đích giáo dục như một phần của môn **Principles of Programming Languages**.

**Tác giả**: MEng. Trần Ngọc Bảo Duy
**Đơn vị**: Khoa Khoa học và Kỹ thuật Máy tính, Trường Đại học Bách Khoa TP.HCM, ĐHQG-HCM
