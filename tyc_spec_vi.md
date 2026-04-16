# Đặc tả Ngôn ngữ Lập trình TyC

**Phiên bản 1.0 - Tháng 01/2026**

## Mục lục

1. [Giới thiệu](#giới-thiệu)
2. [Cấu trúc chương trình](#cấu-trúc-chương-trình)
3. [Cấu trúc từ vựng](#cấu-trúc-từ-vựng)
4. [Hệ thống kiểu](#hệ-thống-kiểu)
5. [Biểu thức](#biểu-thức)
6. [Câu lệnh](#câu-lệnh)
7. [Suy luận kiểu](#suy-luận-kiểu)
8. [Quy tắc phạm vi](#quy-tắc-phạm-vi)
9. [Nhập và xuất](#nhập-và-xuất)
10. [Chương trình ví dụ](#chương-trình-ví-dụ)

---

## Giới thiệu

**TyC**, đọc là "type-see", là một ngôn ngữ lập trình đơn giản kiểu C được thiết kế chủ yếu cho sinh viên thực hành xây dựng một trình biên dịch đơn giản. TyC có một hệ suy luận kiểu hoàn chỉnh với kiểm tra kiểu nghiêm ngặt: mỗi toán tử có yêu cầu kiểu rõ ràng, giúp việc kiểm tra kiểu trở nên trực quan trong khi vẫn giữ cú pháp gần giống C.

Dù đơn giản, TyC vẫn bao gồm hầu hết các tính năng quan trọng của một ngôn ngữ lập trình thủ tục như hàm, biến, các cấu trúc điều khiển luồng (if, while, for, switch-case), và suy luận kiểu hoàn chỉnh.

---

## Cấu trúc chương trình

Do tính đơn giản, trình biên dịch TyC không hỗ trợ biên dịch nhiều file, vì vậy một chương trình TyC chỉ được viết trong **một** file duy nhất. Một chương trình TyC bao gồm một dãy các khai báo struct và khai báo hàm.

Điểm vào (entry point) của chương trình TyC là một hàm tên `main` không có tham số và trả về `void`. Mỗi hàm như vậy trong chương trình TyC là một entry point của chương trình.

### Khai báo hàm

Một khai báo hàm có dạng sau:

```tyc
<return_type> <identifier>(<parameter_list>) {
    <statement_list>
}
```

Trong đó:

- `<return_type>` là một kiểu được mô tả ở Mục 4, hoặc có thể được bỏ qua để suy luận kiểu trả về
- `<identifier>` là tên hàm
- `<parameter_list>` là danh sách khai báo tham số, ngăn cách bằng dấu phẩy (hoặc rỗng)
- `<statement_list>` là một dãy các câu lệnh

Một khai báo tham số có dạng:

```tyc
<type> <identifier>
```

trong đó `<identifier>` là tên tham số và `<type>` phải là kiểu tường minh (`int`, `float`, `string`, hoặc tên kiểu struct). **Lưu ý:** Tham số không thể dùng `auto` để suy luận kiểu — kiểu phải được khai báo tường minh.

`<statement_list>` sẽ được mô tả ở phần [Câu lệnh](#câu-lệnh).

**Nạp chồng hàm (Function Overloading):** TyC không hỗ trợ nạp chồng hàm. Trong một chương trình TyC, tên hàm phải là duy nhất — không thể có hai hàm trùng tên, bất kể kiểu tham số hoặc kiểu trả về. Ràng buộc này giúp suy luận kiểu đơn giản hơn, vì kiểu của lời gọi hàm có thể xác định chỉ dựa trên tên hàm mà không cần xét nhiều chữ ký hàm.

#### Ví dụ

```tyc
int add(int x, int y) {
    return x + y;
}

void main() {
    auto result = add(3, 5);
    printInt(result);
}
```

#### Ví dụ với kiểu trả về được suy luận

Khi bỏ qua kiểu trả về, kiểu sẽ được suy luận từ các câu lệnh return trong hàm:

```tyc
// Kiểu trả về suy luận là int
add(int x, int y) {
    return x + y;
}

// Kiểu trả về suy luận là float
multiply(float a, float b) {
    return a * b;
}

// Kiểu trả về suy luận là void (không có return)
greet(string name) {
    printString("Hello, ");
    printString(name);
}

void main() {
    auto sum = add(3, 5);               // sum: int
    auto product = multiply(2.5, 3.0);  // product: float
    greet("World");
}
```

---

## Cấu trúc từ vựng

### Bộ ký tự

Bộ ký tự của TyC là ASCII. Dấu cách (`' '`), tab (`'\t'`), form feed (ASCII FF) (`'\f'`), carriage return (ASCII CR – `'\r'`) và newline (ASCII LF – `'\n'`) là các ký tự khoảng trắng. Trong TyC, `\n` được dùng làm ký tự xuống dòng.

Định nghĩa về dòng này có thể dùng để xác định số dòng mà trình biên dịch TyC tạo ra.

### Chú thích (Comment)

TyC có hai loại chú thích: chú thích khối (block) và chú thích dòng (line). Chú thích khối bắt đầu bằng `"/*"` và bỏ qua mọi ký tự (trừ EOF) cho đến khi gặp `"*/"`. Chú thích dòng bỏ qua mọi ký tự từ `"//"` đến hết dòng hiện tại, tức là khi gặp cuối dòng hoặc cuối file.

Ví dụ:

```tyc
/* This is a block comment, that
may span in many lines*/
auto x = 5; //this is a line comment
```

Các quy tắc sau được áp dụng trong TyC:

- Chú thích không lồng nhau
- `"/*"` và `"*/"` không có ý nghĩa đặc biệt bên trong chú thích dòng
- `"//"` không có ý nghĩa đặc biệt bên trong chú thích khối

Ví dụ:

```tyc
/* This is a block comment so // has no meaning here */
//This is a line comment so /* has no meaning here
```

### Định danh (Identifier)

Định danh được dùng để đặt tên biến, hàm và tham số.
Định danh bắt đầu bằng chữ cái (A-Z hoặc a-z) hoặc dấu gạch dưới (`_`), và có thể chứa chữ cái, dấu gạch dưới và chữ số (0-9). TyC phân biệt hoa/thường, do đó các định danh sau là khác nhau: `MyVar`, `myvar`, và `MYVAR`.

### Từ khóa (Keyword)

Các chuỗi ký tự sau là từ khóa (reserved keywords) và không thể dùng làm định danh:

| **auto**   | **break**   | **case**   | **continue** | **default** | **else**    |
| ---------- | ----------- | ---------- | ------------ | ----------- | ----------- |
| **float**  | **for**     | **if**     | **int**      | **return**  | **string**  |
| ---------- | ----------- | ---------- | ----------   | ----------- | ----------- |
| **struct** | **switch**  | **void**   | **while**    |             |             |

### Toán tử (Operator)

Danh sách các toán tử **hợp lệ** kèm ý nghĩa. Lưu ý kiểu áp dụng cho từng toán tử:

| **Toán tử** | **Ý nghĩa**                 | **Kiểu áp dụng** |
| ----------- | --------------------------- | ---------------- |
| `+`         | Cộng hoặc dấu cộng một ngôi | int hoặc float   |
| `-`         | Trừ hoặc dấu trừ một ngôi   | int hoặc float   |
| `*`         | Nhân                        | int hoặc float   |
| `/`         | Chia                        | int hoặc float   |
| `%`         | Chia lấy dư                 | chỉ int          |
| `==`        | Bằng                        | int hoặc float   |
| `!=`        | Khác                        | int hoặc float   |
| `<`         | Nhỏ hơn                     | int hoặc float   |
| `>`         | Lớn hơn                     | int hoặc float   |
| `<=`        | Nhỏ hơn hoặc bằng           | int hoặc float   |
| `>=`        | Lớn hơn hoặc bằng           | int hoặc float   |
| `\|\|`      | OR logic                    | chỉ int          |
| `&&`        | AND logic                   | chỉ int          |
| `!`         | NOT logic                   | chỉ int          |
| `++`        | Tăng                        | chỉ int          |
| `--`        | Giảm                        | chỉ int          |
| `=`         | Gán                         | mọi kiểu         |
| `.`         | Truy cập thành viên         | struct           |

### Ký hiệu phân tách (Separator)

Các ký tự **phân tách** gồm: ngoặc vuông trái (`[`), ngoặc vuông phải (`]`), ngoặc nhọn trái (`{`), ngoặc nhọn phải (`}`), ngoặc tròn trái (`(`), ngoặc tròn phải (`)`), dấu chấm phẩy (`;`), và dấu phẩy (`,`).

### Literal

Literal là biểu diễn trong mã nguồn của một giá trị thuộc kiểu số nguyên, số thực, hoặc chuỗi.

#### Literal số nguyên

Literal số nguyên trong TyC **luôn được viết ở hệ thập phân** (cơ số 10). Một số thập phân là một chuỗi chữ số (0-9) và có ít nhất một chữ số. Literal số nguyên có thể có dấu trừ (`-`) ở trước để biểu diễn giá trị âm.
Các số nguyên hợp lệ: `0` `100` `255` `2500` `-45`
Literal số nguyên có kiểu **int**.

#### Literal số thực

Literal số thực biểu diễn số floating-point. Có thể viết dạng thập phân (vd: `3.14`, `0.5`, `123.456`) hoặc dạng khoa học (vd: `1.23e4`, `5.67E-2`). Literal số thực có thể có dấu trừ (`-`) ở trước.

Các số thực hợp lệ: `0.0` `3.14` `-2.5` `1.23e4` `5.67E-2` `1.` `.5`
Literal số thực có kiểu **float**.

#### Literal chuỗi

**Literal chuỗi** gồm không hoặc nhiều ký tự được bao bởi dấu ngoặc kép (`"`). Dùng các chuỗi escape (liệt kê bên dưới) để biểu diễn ký tự đặc biệt trong chuỗi.

Nếu ký tự xuống dòng hoặc EOF xuất hiện bên trong literal chuỗi thì đó là lỗi ở thời điểm biên dịch.
Các escape sequence được hỗ trợ:

```
\b   backspace
\f   formfeed
\r   carriage return
\n   newline
\t   horizontal tab
\"   double quote
\\   backslash
```

Ví dụ hợp lệ:

```tyc
"This is a string containing tab \t"
"He asked me: \"Where is John?\""
""
```

Literal chuỗi có kiểu **string**.

---

## Hệ thống kiểu

Kiểu dữ liệu giới hạn các giá trị mà một biến có thể chứa (ví dụ: một định danh `x` có kiểu `int` không thể chứa giá trị "hello"...), giới hạn các giá trị mà một biểu thức có thể tạo ra, và các phép toán được hỗ trợ trên các giá trị đó (ví dụ: không thể áp dụng phép `+` cho hai giá trị kiểu chuỗi...).

### Kiểu nguyên thủy (Primitive Type)

#### Số nguyên (Integer)

Từ khóa `int` được dùng để biểu diễn kiểu số nguyên. Một giá trị kiểu số nguyên có thể dương hoặc âm. Chỉ các toán tử sau có thể áp dụng lên giá trị số nguyên:
`+ - * / % == != < <= > >= && || ! ++ --`

#### Số thực (Float)

Từ khóa `float` biểu diễn kiểu số thực dấu chấm động. Một giá trị kiểu float có thể dương hoặc âm. Chỉ các toán tử sau có thể áp dụng lên giá trị float:
`+ - * / == != < <= > >=`

Lưu ý rằng toán tử chia lấy dư (`%`) và các toán tử logic (`&&`, `||`, `!`) không áp dụng cho float. Ngoài ra, toán tử tăng (`++`) và giảm (`--`) cũng không áp dụng cho float.

#### Chuỗi (String)

Từ khóa `string` biểu diễn kiểu chuỗi. Không có toán tử nào tác động lên giá trị chuỗi, ngoại trừ phép gán và việc truyền/nhận giá trị qua tham số hoặc kiểu trả về của hàm. Kiểu chuỗi chủ yếu được dùng cho thao tác nhập/xuất.

#### Void

Từ khóa `void` được dùng để biểu diễn kiểu void. Kiểu này chỉ được dùng làm kiểu trả về của hàm khi hàm không trả về giá trị. Kiểu này **không** được phép dùng để khai báo biến hoặc tham số.

### Kiểu struct

Từ khóa `struct` được dùng để định nghĩa một kiểu dữ liệu tổng hợp (composite) nhằm gom nhóm các biến có kiểu khác nhau. Một khai báo struct định nghĩa một kiểu mới có thể được sử dụng xuyên suốt chương trình.

#### Khai báo struct

Một khai báo struct có dạng sau:

```tyc
struct <identifier> {
    <type1> <member1>;
    <type2> <member2>;
    ...
    <typeN> <memberN>;
};
```

Trong đó:

- `<identifier>` là tên struct
- Mỗi `<type>` phải là kiểu tường minh (`int`, `float`, `string`, hoặc một kiểu struct khác)
- Mỗi `<member>` là tên trường/thành viên (định danh)
- **Lưu ý:** Thành viên struct không thể dùng `auto` để suy luận kiểu — kiểu phải được khai báo tường minh
- **Lưu ý:** Không hỗ trợ struct lồng nhau (struct bên trong struct)

**Các quy tắc quan trọng:**

- Thành viên struct không thể dùng `auto` — chỉ cho phép kiểu tường minh
- Định nghĩa struct không thể lồng nhau (không có khai báo struct bên trong một khai báo struct khác)
- Tuy nhiên, thành viên struct có thể có kiểu là struct khác (dùng các kiểu struct đã khai báo trước đó)
- Tên struct phải là duy nhất trong chương trình
- Thành viên struct có thể là kiểu nguyên thủy (`int`, `float`, `string`) hoặc kiểu struct khác (được khai báo trước khi sử dụng)

Ví dụ:

```tyc
struct Point {
    int x;
    int y;
};

struct Person {
    string name;
    int age;
    float height;
};
```

#### Khai báo biến struct

Một biến struct có thể được khai báo bằng cách dùng tên struct làm kiểu:

```tyc
<struct_name> <identifier>;                    // không khởi tạo
<struct_name> <identifier> = {<member_list>};  // có khởi tạo
```

Trong đó:

- `<struct_name>` là tên một kiểu struct đã được khai báo trước đó
- `<identifier>` là tên biến
- `<member_list>` là danh sách các biểu thức khởi tạo, ngăn cách bằng dấu phẩy (hoặc rỗng để tạo struct rỗng)

**Quy tắc khởi tạo struct:**

- Khi khởi tạo struct bằng `{<member_list>}`, số lượng biểu thức trong `<member_list>` phải đúng bằng số lượng thành viên của struct
- Mỗi biểu thức trong `<member_list>` phải theo đúng thứ tự các thành viên trong struct
- Kiểu của mỗi biểu thức khởi tạo phải khớp kiểu của thành viên tương ứng:
  - Biểu thức thứ nhất khởi tạo thành viên thứ nhất
  - Biểu thức thứ hai khởi tạo thành viên thứ hai
  - Và cứ tiếp tục như vậy...
- Mỗi biểu thức trong `<member_list>` có thể là literal, biến, lời gọi hàm, hoặc bất kỳ biểu thức nào miễn là nó đánh giá ra đúng kiểu
- Nếu biến struct được khai báo mà không khởi tạo, mọi thành viên của nó có giá trị không xác định cho đến khi được gán

Ví dụ:

```tyc
Point p1;                      // chưa khởi tạo
Point p2 = {10, 20};          // khởi tạo: x=10, y=20

Person person1;               // chưa khởi tạo
Person person2 = {"John", 25, 1.75};  // khởi tạo: name="John", age=25, height=1.75
```

#### Truy cập thành viên struct

Truy cập thành viên struct bằng toán tử dấu chấm (`.`):

```tyc
<struct_variable>.<member_name>
```

Ví dụ:

```tyc
Point p = {10, 20};
p.x = 30;           // gán cho thành viên x
auto x_coord = p.x; // đọc thành viên x
printInt(p.x);      // dùng thành viên x trong biểu thức
```

#### Các phép toán trên struct

- **Gán (Assignment)**: Giá trị struct có thể được gán bằng `=`. Phép gán sẽ sao chép toàn bộ giá trị các thành viên.
- **So sánh bằng (Equality)**: Kiểu struct không hỗ trợ các toán tử so sánh bằng (`==`, `!=`).
- **Số học (Arithmetic)**: Kiểu struct không hỗ trợ các toán tử số học.
- **Truy cập thành viên (Member Access)**: Dùng toán tử dấu chấm (`.`) để truy cập thành viên.

Ví dụ:

```tyc
Point p1 = {10, 20};
Point p2;
p2 = p1;        // Sao chép mọi thành viên: p2.x = 10, p2.y = 20
p2.x = 30;      // Sửa thành viên
// p1 == p2;    // Lỗi: không hỗ trợ so sánh bằng cho struct
```

### Khai báo biến

TyC hỗ trợ hai cách khai báo biến:

1. **Suy luận kiểu với `auto`**: kiểu có thể được suy luận từ biểu thức khởi tạo (nếu có)
2. **Khai báo kiểu tường minh**: kiểu được khai báo rõ ràng bằng các từ khóa kiểu (`int`, `float`, `string`, hoặc tên kiểu struct)

#### Các dạng khai báo biến

**Dùng `auto` và có khởi tạo (suy luận kiểu):**

```tyc
auto <identifier> = <expression>;
```

**Dùng `auto` nhưng không khởi tạo:**

```tyc
auto <identifier>;
```

Lưu ý: Khi dùng `auto` mà không khởi tạo, kiểu của biến phải được xác định từ các phép gán hoặc cách sử dụng về sau. Tuy nhiên, nếu biến được dùng trước khi được gán thì sẽ phát sinh lỗi.

**Dùng kiểu tường minh và có khởi tạo:**

```tyc
<type> <identifier> = <expression>;
```

**Dùng kiểu tường minh nhưng không khởi tạo:**

```tyc
<type> <identifier>;
```

Trong đó `<type>` là một trong các kiểu: `int`, `float`, `string`, hoặc tên kiểu struct

#### Ví dụ

```tyc
// Dùng auto và có khởi tạo
auto x = 10;           // x là int (suy luận)
auto y = 3.14;         // y là float (suy luận)
auto msg = "hello";    // msg là string (suy luận)
auto sum = x + y;      // sum là float (suy luận)

// Dùng auto nhưng không khởi tạo (kiểu suy luận từ lần dùng đầu tiên)
auto a;
a = 10;                // a là int (suy luận từ lần dùng đầu tiên - phép gán)
auto b;
b = 3.14;              // b là float (suy luận từ lần dùng đầu tiên - phép gán)
auto c;
c = readInt();         // c là int (suy luận từ lần dùng đầu tiên - kiểu trả về hàm)

// Dùng kiểu tường minh và có khởi tạo
int x = 10;
float d = 3.14;
string s = "hello";
int result = x + 5;

// Dùng kiểu tường minh nhưng không khởi tạo
int e;
float f;
string t;
e = 10;                // e đã là int
f = 3.14;              // f đã là float
```

**Các quy tắc quan trọng:**

- Khi dùng `auto` và có khởi tạo, kiểu được suy luận từ biểu thức khởi tạo
- Khi dùng `auto` và không khởi tạo, kiểu được suy luận từ lần dùng đầu tiên của biến (phép gán, biểu thức, đối số hàm, giá trị trả về, ...)
- Khi dùng kiểu tường minh, khởi tạo là tùy chọn
- Nếu một biến được dùng trong ngữ cảnh mà kiểu của nó không thể xác định, sẽ phát sinh lỗi ngữ nghĩa

---

## Biểu thức

**Biểu thức (Expressions)** là các cấu trúc được tạo thành từ toán tử và toán hạng. Chúng tính toán trên các toán hạng và trả về dữ liệu mới. Trong TyC có hai loại phép toán: một ngôi (unary) và hai ngôi (binary). Phép toán một ngôi làm việc với một toán hạng, còn phép toán hai ngôi làm việc với hai toán hạng.

### Biểu thức số học (Arithmetic Expression)

Biểu thức số học dùng các toán tử sau:

| **Toán tử** | **Phép toán**                      | **Kiểu toán hạng** | **Kiểu kết quả**                       |
| ----------- | ---------------------------------- | ------------------ | -------------------------------------- |
| `+`         | Dấu cộng một ngôi (giữ nguyên dấu) | int hoặc float     | giống toán hạng                        |
| `-`         | Dấu trừ một ngôi (đổi dấu)         | int hoặc float     | giống toán hạng                        |
| `+`         | Cộng hai ngôi                      | int hoặc float     | int nếu cả hai là int, ngược lại float |
| `-`         | Trừ hai ngôi                       | int hoặc float     | int nếu cả hai là int, ngược lại float |
| `*`         | Nhân hai ngôi                      | int hoặc float     | int nếu cả hai là int, ngược lại float |
| `/`         | Chia hai ngôi                      | int hoặc float     | int nếu cả hai là int, ngược lại float |
| `%`         | Lấy dư                             | int                | int                                    |

Toán hạng của `+`, `-`, `*`, `/` có thể là kiểu **int** hoặc **float**. Nếu cả hai toán hạng đều là int thì kết quả là int. Nếu có ít nhất một toán hạng là float thì kết quả là float.

Toán hạng của `%` chỉ được phép là **int**, và kết quả luôn là **int**.

### Biểu thức quan hệ (Relational Expression)

**Toán tử quan hệ** thực hiện so sánh trên các toán hạng. Toán hạng có thể là kiểu **int** hoặc **float**. Mọi phép toán quan hệ đều cho ra kết quả kiểu **int** (0 là sai, khác 0 là đúng). Các toán tử quan hệ gồm:

| **Toán tử** | **Ý nghĩa**       | **Kiểu toán hạng** | **Kiểu kết quả** |
| ----------- | ----------------- | ------------------ | ---------------- |
| `==`        | Bằng              | int hoặc float     | int              |
| `!=`        | Khác              | int hoặc float     | int              |
| `>`         | Lớn hơn           | int hoặc float     | int              |
| `<`         | Nhỏ hơn           | int hoặc float     | int              |
| `>=`        | Lớn hơn hoặc bằng | int hoặc float     | int              |
| `<=`        | Nhỏ hơn hoặc bằng | int hoặc float     | int              |

### Biểu thức logic (Logical Expression)

**Biểu thức logic** gồm các toán tử logic như `&&` (AND), `||` (OR), `!` (NOT). Toán hạng của các toán tử này phải là kiểu **int** (0 là sai, khác 0 là đúng), và kiểu kết quả cũng là **int** (0 là sai, khác 0 là đúng).

### Biểu thức tăng/giảm (Increment and Decrement Expression)

TyC hỗ trợ toán tử tăng/giảm dạng prefix và postfix. Các toán tử này chỉ áp dụng cho kiểu **int**:

| **Toán tử** | **Phép toán**                 | **Kiểu toán hạng** | **Kiểu kết quả** |
| ----------- | ----------------------------- | ------------------ | ---------------- |
| `++`        | Tăng trước (prefix increment) | int                | int              |
| `--`        | Giảm trước (prefix decrement) | int                | int              |
| `++`        | Tăng sau (postfix increment)  | int                | int              |
| `--`        | Giảm sau (postfix decrement)  | int                | int              |

Toán hạng phải là kiểu **int**. Giá trị float không thể dùng với toán tử tăng/giảm.

### Biểu thức gọi hàm (Function Call Expression)

**Lời gọi hàm** là một biểu thức dùng để gọi một hàm. Dạng:

```tyc
<identifier>(<argument_list>)
```

trong đó `<argument_list>` là danh sách các biểu thức ngăn cách bằng dấu phẩy (hoặc rỗng). Kiểu của biểu thức lời gọi hàm là kiểu trả về của hàm được gọi.

### Biểu thức gán (Assignment Expression)

**Biểu thức gán** gán một giá trị cho biến và cũng có thể được dùng như một biểu thức. Dạng:

```tyc
<identifier> = <expression>
```

hoặc

```tyc
<member_access> = <expression>
```

Biểu thức gán có tính kết hợp phải (right-associative), cho phép gán chuỗi như `x = y = z = 10;`, được phân tích là `x = (y = (z = 10));`. Biểu thức gán có thể xuất hiện trong ngữ cảnh biểu thức, ví dụ: `int y = (x = 5) + 7;`.

### Biểu thức cơ sở (Primary Expression)

Biểu thức cơ sở gồm:

- **Định danh**: `x`, `counter`, `myVar`
- **Literal**: `123`, `3.14`, `"hello"`
- **Biểu thức trong ngoặc**: `(x + y)`
- **Truy cập thành viên**: `structVar.memberName`

### Độ ưu tiên và tính kết hợp của toán tử

Thứ tự ưu tiên của toán tử (từ cao xuống thấp):

| **Toán tử**                   | **Tính kết hợp** |
| ----------------------------- | ---------------- |
| `++`, `--` (postfix)          | trái             |
| `++`, `--` (prefix)           | phải             |
| `!`, `-` (unary), `+` (unary) | phải             |
| `.` (truy cập thành viên)     | trái             |
| `*`, `/`, `%`                 | trái             |
| `+`, `-` (binary)             | trái             |
| `<`, `<=`, `>`, `>=`          | trái             |
| `==`, `!=`                    | trái             |
| `&&`                          | trái             |
| `\|\|`                        | trái             |
| `=`                           | phải             |

### Thứ tự đánh giá (Evaluation Order)

TyC yêu cầu toán hạng bên trái của một toán tử nhị phân phải được đánh giá trước, trước khi bất kỳ phần nào của toán hạng bên phải được đánh giá. Tương tự, trong lời gọi hàm, các tham số thực (actual parameters) phải được đánh giá từ trái sang phải.

Mọi toán hạng của một toán tử đều phải được đánh giá trước khi thực hiện phép toán. Có hai ngoại lệ là các toán tử logic `&&` và `||`: chúng vẫn được đánh giá từ trái sang phải, nhưng được đảm bảo sẽ dừng đánh giá ngay khi đã biết được đúng/sai. Điều này được gọi là đánh giá ngắn mạch (short-circuit evaluation).

---

## Câu lệnh

Một câu lệnh (statement) — không trả về giá trị nào (ngoại trừ câu lệnh `return`) — mô tả hành động mà chương trình thực hiện. Có nhiều loại câu lệnh như sau.

### Câu lệnh khai báo biến

Một **khai báo biến** khai báo một biến. Biểu thức khởi tạo là tùy chọn:

**Suy luận kiểu (dùng `auto`):**

```tyc
auto <identifier> = <expression>;    // có khởi tạo
auto <identifier>;                  // không khởi tạo
```

**Khai báo kiểu tường minh:**

```tyc
<type> <identifier> = <expression>;  // có khởi tạo
<type> <identifier>;                 // không khởi tạo
```

Trong đó `<type>` là một trong: `int`, `float`, `string`, hoặc tên kiểu struct

**Quy tắc suy luận kiểu:**

- Khi dùng `auto` và có khởi tạo: kiểu được suy luận từ biểu thức khởi tạo
- Khi dùng `auto` và không khởi tạo: kiểu được suy luận từ lần dùng đầu tiên của biến (phép gán, biểu thức, đối số hàm, ...)
- Khi dùng kiểu tường minh và có khởi tạo: kiểu của biểu thức khởi tạo phải khớp kiểu khai báo
- Khi dùng kiểu tường minh và không khởi tạo: biến có kiểu tường minh đã khai báo

Ví dụ:

```tyc
// Dùng auto và có khởi tạo
auto x = 10;           // x là int (suy luận)
auto y = 3.14;         // y là float (suy luận)
auto msg = "hello";    // msg là string (suy luận)
auto sum = x + y;      // sum là float (suy luận)

// Dùng auto nhưng không khởi tạo
auto a;
a = 10;                // a là int (suy luận từ lần dùng đầu tiên - phép gán)

// Dùng kiểu tường minh và có khởi tạo
int b = 10;
float c = 3.14;
string s = "hello";

// Dùng kiểu tường minh nhưng không khởi tạo
int d;
float e;
string t;
```

### Câu lệnh khối (Block Statement)

Câu lệnh khối bắt đầu bằng dấu ngoặc nhọn trái `{` và kết thúc bằng dấu ngoặc nhọn phải `}`. Bên trong có thể chứa danh sách khai báo biến và các câu lệnh.

Ví dụ:

```tyc
{
    auto x = 10;
    auto y = 20;
    auto sum = x + y;
    printInt(sum);
}
```

### Câu lệnh gán (Assignment Statement)

Một **câu lệnh gán** gán giá trị cho một biến. Dạng:

```tyc
<identifier> = <expression>;
```

Kiểu của giá trị từ `<expression>` phải khớp kiểu của biến.

Ví dụ:

```tyc
x = 5;
x = x + 1;
```

### Câu lệnh if

Câu lệnh **if** thực thi có điều kiện một trong hai câu lệnh dựa trên giá trị của một biểu thức. Dạng:

```tyc
if (<expression>) <statement>
```

hoặc

```tyc
if (<expression>) <statement> else <statement>
```

trong đó `<expression>` đánh giá ra một giá trị **int** (0 là sai, khác 0 là đúng). Nếu biểu thức khác 0 thì thực thi `<statement>` đầu tiên. Nếu biểu thức bằng 0 và có nhánh `else` thì thực thi câu lệnh sau `else`. Nếu không có `else` và biểu thức bằng 0 thì bỏ qua if.

Ví dụ:

```tyc
if (flag) {
    printInt(1);
} else {
    printInt(0);
}
```

### Câu lệnh while

Câu lệnh **while** cho phép thực thi lặp một hoặc nhiều câu lệnh khi điều kiện còn đúng. Dạng:

```tyc
while (<expression>) <statement>
```

`<expression>` phải đánh giá ra kiểu **int** (0 là sai, khác 0 là đúng). `<statement>` được thực thi lặp lại miễn là biểu thức khác 0.

Ví dụ:

```tyc
auto i = 0;
while (i < 10) {
    printInt(i);
    ++i;
}
```

### Câu lệnh for

Câu lệnh **for** cho phép thực thi lặp một hoặc nhiều câu lệnh. Dạng:

```tyc
for (<init>; <condition>; <update>) <statement>
```

Trong đó:

- `<init>` là khai báo biến hoặc phép gán (tùy chọn)
- `<condition>` là một biểu thức đánh giá ra int (tùy chọn; nếu bỏ qua thì xem như luôn đúng)
- `<update>` là phép gán, tăng, hoặc giảm (tùy chọn)

Ví dụ:

```tyc
for (auto i = 0; i < 10; ++i) {
    printInt(i);
}
```

### Câu lệnh switch

Câu lệnh **switch** cho phép chọn giữa nhiều nhánh dựa trên giá trị của một biểu thức. Dạng:

```tyc
switch (<expression>) {
    case <constant_expression>:
        <statement_list>
    case <constant_expression>:
        <statement_list>
    ...
    default:
        <statement_list>
}
```

Trong đó:

- `<expression>` phải đánh giá ra một giá trị **int**
- `<constant_expression>` là literal số nguyên hoặc biểu thức hằng đánh giá ra số nguyên
- Mỗi nhãn `case` phải theo sau bởi dấu hai chấm (`:`)
- Nhánh `default` là tùy chọn và có thể xuất hiện ở bất kỳ vị trí nào trong switch
- `<statement_list>` có thể rỗng hoặc chứa một hoặc nhiều câu lệnh
- Giống C, **switch của TyC có hành vi rơi-through (fall-through)** — thực thi sẽ tiếp tục sang case tiếp theo trừ khi có `break`

**Quan trọng:** Switch trong TyC theo kiểu rơi-through như C. Thực thi sẽ rơi xuống các case tiếp theo nếu không bị kết thúc bởi câu lệnh `break`. Bạn có thể dùng nhiều nhãn case để chia sẻ cùng một khối lệnh cho nhiều giá trị.

Ví dụ:

```tyc
auto day = 2;
switch (day) {
    case 1:
        printInt(1);
        break;
    case 2:
    case 3:
        printInt(2);
        break;
    default:
        printInt(0);
}
```

Trong ví dụ trên, cả case 2 và case 3 đều thực thi cùng đoạn mã (in ra 2) vì case 2 sẽ rơi xuống case 3.

### Câu lệnh break

Câu lệnh **break** cho phép thoát khỏi vòng lặp hoặc switch ngay cả khi điều kiện kết thúc chưa thỏa. Nó có thể dùng để kết thúc một vòng lặp vô hạn, hoặc buộc vòng lặp kết thúc trước khi tới điểm kết thúc tự nhiên. `break` phải nằm trong vòng lặp (while/for) hoặc trong switch. Nếu không, sẽ phát sinh lỗi (được thảo luận ở giai đoạn phân tích ngữ nghĩa). Cú pháp:

`break;`

Trong switch, `break` kết thúc switch và chuyển điều khiển tới câu lệnh ngay sau switch. Nếu không có `break`, thực thi sẽ rơi xuống nhãn case tiếp theo. Thông thường `break` được đặt ở cuối mỗi khối case để tránh rơi-through.

### Câu lệnh continue

Câu lệnh **continue** làm chương trình bỏ qua phần còn lại của thân vòng lặp ở lần lặp hiện tại như thể đã tới cuối khối lệnh, và nhảy đến lần lặp tiếp theo. `continue` phải nằm trong vòng lặp (while/for). Nếu không, sẽ phát sinh lỗi (được thảo luận ở giai đoạn phân tích ngữ nghĩa). Cú pháp:

`continue;`

### Câu lệnh return

Câu lệnh **return** chuyển điều khiển về cho bên gọi (caller) của hàm đang chứa nó. Dạng:

`return <expression>;`

hoặc với hàm void:

`return;`

Kiểu của biểu thức phải khớp kiểu trả về của hàm.

### Câu lệnh biểu thức (Expression Statement)

Một **câu lệnh biểu thức** là một biểu thức theo sau bởi dấu chấm phẩy. Câu lệnh biểu thức được dùng vì tác dụng phụ (ví dụ: lời gọi hàm).

Ví dụ:

```tyc
printInt(x);
x + y;  // hợp lệ nhưng không có tác dụng hữu ích
```

---

## Suy luận kiểu

### Hệ suy luận kiểu hoàn chỉnh

TyC sử dụng hệ suy luận kiểu hoàn chỉnh, trong đó kiểu được suy luận xuyên suốt toàn bộ chương trình. Trình biên dịch suy luận kiểu từ nhiều nguồn như mô tả bên dưới.

### Các quy tắc suy luận kiểu

#### Quy tắc 1: Suy luận kiểu cho literal

Literal có kiểu vốn có:

- **Literal số nguyên** (`123`, `-45`, `0`) → kiểu `int`
- **Literal số thực** (`9.0`, `12e8`, `1.`, `0.33E-3`, `-3.14`) → kiểu `float`
- **Literal chuỗi** (`"hello"`, `"world"`) → kiểu `string`

#### Quy tắc 2: Suy luận kiểu trong khai báo biến

**2.1 Khai báo biến với `auto` và có khởi tạo:**

- Kiểu được suy luận từ biểu thức khởi tạo
- Kiểu của biến chính là kiểu của biểu thức khởi tạo

```tyc
auto x = 10;           // x: int (từ literal số nguyên)
auto y = 3.14;         // y: float (từ literal số thực)
auto msg = "hello";    // msg: string (từ literal chuỗi)
auto z = x + y;        // z: float (từ kiểu kết quả biểu thức)
```

**2.2 Khai báo biến với `auto` nhưng không khởi tạo:**

- Kiểu được suy luận từ lần sử dụng đầu tiên của biến
- Kiểu của biến được quyết định bởi ngữ cảnh của lần dùng đầu tiên:
  - Nếu lần dùng đầu là phép gán: kiểu là kiểu của biểu thức bên phải
  - Nếu lần dùng đầu nằm trong một biểu thức: kiểu được quyết định bởi yêu cầu kiểu của biểu thức
  - Nếu lần dùng đầu là đối số hàm: kiểu được quyết định bởi kiểu tham số của hàm
  - Nếu lần dùng đầu là giá trị trả về: kiểu được quyết định bởi kiểu trả về của hàm
- Nếu biến được dùng trong ngữ cảnh mà kiểu không thể xác định, sẽ phát sinh lỗi ngữ nghĩa

```tyc
auto a;                // ban đầu chưa biết kiểu
a = 10;                // a: int (suy luận từ phép gán - lần dùng đầu)
auto b;
b = 3.14;              // b: float (suy luận từ phép gán - lần dùng đầu)
auto c;
c = a + b;             // c: float (suy luận từ biểu thức - lần dùng đầu)

auto x;
x = readInt();         // x: int (suy luận từ kiểu trả về hàm - lần dùng đầu)

auto y;
// printInt(y);        // Lỗi: không thể suy luận kiểu chỉ từ lời gọi printInt()
y = 10;                // y: int (suy luận từ lần dùng đầu - phép gán)
printInt(y);           // Lúc này y là int nên có thể dùng printInt
```

**2.3 Khai báo biến kiểu tường minh và có khởi tạo:**

- Kiểu của biến là kiểu được khai báo tường minh
- Kiểu của biểu thức khởi tạo phải khớp với kiểu khai báo (cần kiểm tra kiểu)

```tyc
int x = 10;            // x: int (tường minh)
float y = 3.14;        // y: float (tường minh)
string s = "hello";    // s: string (tường minh)
int z = x + 5;         // z: int (tường minh, biểu thức phải ra int)
```

**2.4 Khai báo biến kiểu tường minh nhưng không khởi tạo:**

- Kiểu của biến là kiểu tường minh
- Biến có giá trị không xác định cho đến khi được gán

```tyc
int a;                 // a: int (tường minh)
float b;               // b: float (tường minh)
string c;              // c: string (tường minh)
a = 10;                // gán cho biến int
```

#### Quy tắc 3: Suy luận kiểu cho biểu thức

Kiểu của một biểu thức được suy luận từ các thành phần của nó:

**3.1 Biểu thức cơ sở (Primary Expressions):**

- **Định danh**: kiểu là kiểu đã khai báo của định danh
  - Nếu định danh là biến: kiểu là kiểu của biến
  - Nếu định danh là hàm: kiểu là kiểu trả về của hàm (khi gọi hàm)

- **Literal**: kiểu theo Quy tắc 1

- **Biểu thức trong ngoặc**: `(expr)` → kiểu là kiểu của `expr`

- **Truy cập thành viên**: `expr.memberName` → kiểu là kiểu của thành viên trong struct
  - `expr` phải có kiểu struct
  - `memberName` phải là thành viên của kiểu struct đó

**3.2 Suy luận kiểu cho biểu thức một ngôi:**

| **Biểu thức** | **Kiểu toán hạng** | **Kiểu kết quả** |
| ------------- | ------------------ | ---------------- |
| `+expr`       | `int` hoặc `float` | giống toán hạng  |
| `-expr`       | `int` hoặc `float` | giống toán hạng  |
| `!expr`       | `int`              | `int`            |
| `++expr`      | `int`              | `int`            |
| `--expr`      | `int`              | `int`            |

**3.3 Suy luận kiểu cho biểu thức hậu tố (postfix):**

| **Biểu thức** | **Kiểu toán hạng** | **Kiểu kết quả**    |
| ------------- | ------------------ | ------------------- |
| `expr++`      | `int`              | `int`               |
| `expr--`      | `int`              | `int`               |
| `expr(args)`  | gọi hàm            | kiểu trả về của hàm |

**3.4 Suy luận kiểu cho biểu thức nhị phân:**

**Toán tử số học:**

| **Toán tử**        | **Toán hạng trái** | **Toán hạng phải** | **Kiểu kết quả** |
| ------------------ | ------------------ | ------------------ | ---------------- |
| `+`, `-`, `*`, `/` | `int`              | `int`              | `int`            |
| `+`, `-`, `*`, `/` | `int`              | `float`            | `float`          |
| `+`, `-`, `*`, `/` | `float`            | `int`              | `float`          |
| `+`, `-`, `*`, `/` | `float`            | `float`            | `float`          |
| `%`                | `int`              | `int`              | `int`            |

**Toán tử quan hệ:**

| **Toán tử**                      | **Toán hạng trái** | **Toán hạng phải** | **Kiểu kết quả** |
| -------------------------------- | ------------------ | ------------------ | ---------------- |
| `==`, `!=`, `<`, `<=`, `>`, `>=` | `int` hoặc `float` | `int` hoặc `float` | `int`            |

**Toán tử logic:**

| **Toán tử**  | **Toán hạng trái** | **Toán hạng phải** | **Kiểu kết quả** |
| ------------ | ------------------ | ------------------ | ---------------- |
| `&&`, `\|\|` | `int`              | `int`              | `int`            |
| `!`          | `int`              | N/A (một ngôi)     | `int`            |

**3.5 Suy luận kiểu cho lời gọi hàm:**

- **Gọi hàm**: `identifier(args)` → kiểu là kiểu trả về của hàm được gọi
- Kiểu trả về của hàm có thể khai báo tường minh hoặc suy luận từ các câu lệnh return

**3.6 Suy luận kiểu cho biểu thức gán:**

- **Gán**: `identifier = expr` → kiểu là kiểu của `identifier` (vế trái)
- Kiểu của `expr` phải khớp với kiểu của `identifier`

#### Quy tắc 4: Tương thích kiểu và kiểm tra kiểu

**4.1 Tương thích khi gán:**

- Kiểu vế trái phải khớp kiểu vế phải
- Với khai báo kiểu tường minh: kiểu biểu thức khởi tạo phải khớp kiểu khai báo

**4.2 Tương thích kiểu theo toán tử:**

- Mỗi toán tử chỉ áp dụng cho các kiểu cụ thể như mô tả ở Quy tắc 3
- Kiểu toán hạng phải phù hợp yêu cầu của toán tử

**4.3 Tương thích kiểu khi gọi hàm:**

- Kiểu đối số phải khớp kiểu tham số
- Số lượng đối số phải khớp số lượng tham số

#### Quy tắc 5: Khai báo kiểu trả về của hàm

- Kiểu trả về của hàm có thể được khai báo tường minh hoặc bỏ qua (để suy luận)
- Khi bỏ qua kiểu trả về, kiểu được suy luận từ các câu lệnh return trong hàm:
  - Nếu mọi return đều trả về giá trị kiểu `T` thì kiểu trả về suy luận là `T`
  - Nếu không có return hoặc chỉ có `return;` thì kiểu trả về suy luận là `void`
- Mọi câu lệnh `return` trong một hàm phải trả về đúng kiểu trả về đã suy luận/khai báo (hoặc không trả về giá trị với `void`)

### Gán kiểu chặt chẽ theo toán tử (Strict Operator Typing)

**Mỗi toán tử chỉ áp dụng cho một số kiểu nhất định:**

- **Toán tử số học** (`+`, `-`, `*`, `/`): áp dụng lên `int` hoặc `float` (kết quả là `int` nếu cả hai toán hạng là int, ngược lại là `float`)
- **Toán tử lấy dư** (`%`): chỉ áp dụng lên `int` (kết quả `int`)
- **Toán tử quan hệ** (`==`, `!=`, `<`, `<=`, `>`, `>=`): áp dụng lên `int` hoặc `float` (kết quả luôn là `int`)
- **Toán tử logic** (`&&`, `||`, `!`): chỉ áp dụng lên `int` (kết quả `int`, 0 là sai, khác 0 là đúng)
- **Tăng/giảm** (`++`, `--`): chỉ áp dụng lên `int` (kết quả `int`)

**Các ràng buộc:**

- Không thể cộng hai chuỗi: `"hello" + "world"` là lỗi kiểu
- Không thể so sánh chuỗi: `"a" < "b"` là lỗi kiểu
- Không thể dùng `%` với float: `3.14 % 2` là lỗi kiểu
- Không thể dùng toán tử logic với float: `3.14 && 2.5` là lỗi kiểu
- Không thể dùng tăng/giảm cho float: `++x` khi `x` là float là lỗi kiểu
- Không thể dùng các toán tử số học/quan hệ/logic cho giá trị chuỗi

### Ví dụ về suy luận kiểu

```tyc
// Quy tắc 2.1: auto có khởi tạo
auto x = 10;              // x: int (từ literal số nguyên)
auto y = 20;              // y: int (từ literal số nguyên)
auto z = x + y;           // z: int (cả hai toán hạng là int)
auto f = 3.14;            // f: float (từ literal số thực)
auto g = 2.5;             // g: float (từ literal số thực)
auto h = f + g;           // h: float (ít nhất một toán hạng là float)
auto mixed = x + f;       // mixed: float (một toán hạng là float)
auto flag = x < y;        // flag: int (toán tử quan hệ trả về int)
auto result = flag && 1;  // result: int (toán tử logic trả về int)
auto msg = "hello";       // msg: string (từ literal chuỗi)

// Quy tắc 2.2: auto không khởi tạo
auto a;
a = 10;                   // a: int (suy luận từ lần dùng đầu - phép gán)
auto b;
b = 3.14;                 // b: float (suy luận từ lần dùng đầu - phép gán)
auto c;
c = a + b;                // c: float (suy luận từ lần dùng đầu - biểu thức)
auto d;
d = readInt();            // d: int (suy luận từ lần dùng đầu - kiểu trả về hàm)

// Quy tắc 2.3: khai báo kiểu tường minh và có khởi tạo
int e = 10;
float f = 3.14;
string s = "hello";
int sum1 = e + 5;         // sum1: int (tường minh, biểu thức phải ra int)

// Quy tắc 2.4: khai báo kiểu tường minh nhưng không khởi tạo
int i;
float j;
string t;
i = 10;                   // gán cho biến int
j = 3.14;                 // gán cho biến float

// Quy tắc 3: ví dụ suy luận kiểu biểu thức
auto expr1 = 10 + 20;           // expr1: int (cả hai toán hạng int)
auto expr2 = 10 + 3.14;         // expr2: float (một toán hạng float)
auto expr3 = 3.14 + 2.5;        // expr3: float (cả hai toán hạng float)
auto expr4 = 10 % 3;            // expr4: int (modulus trả về int)
auto expr5 = 10 < 20;           // expr5: int (quan hệ trả về int)
auto expr6 = 10 && 1;           // expr6: int (logic trả về int)
auto expr7 = ++x;               // expr7: int (tăng trả về int)

// Khai báo hàm (Quy tắc 5)
int add(int a, int b) {
    return a + b;         // trả về int
}

float multiply(float a, float b) {
    return a * b;         // trả về float
}

// Gọi hàm (Quy tắc 3.5)
auto sum2 = add(5, 3);               // sum2: int (hàm trả về int)
int sum3 = add(5, 3);                // sum3: int (kiểu tường minh)
auto product1 = multiply(2.5, 3.0);  // product1: float (hàm trả về float)
float product2 = multiply(2.5, 3.0); // product2: float (kiểu tường minh)
```

---

## Quy tắc phạm vi

Có 2 mức phạm vi: toàn cục (global) và cục bộ (local).

### Phạm vi toàn cục

Tất cả tên hàm và tên struct đều có phạm vi toàn cục. Một tên hàm hoặc tên struct có thể được nhìn thấy ở mọi nơi trong chương trình. Các hàm có thể được gọi từ bất kỳ hàm nào, và các kiểu struct có thể được dùng trong toàn bộ chương trình.

### Phạm vi cục bộ

Tất cả biến được khai báo trong một hàm (bao gồm cả tham số) đều có phạm vi cục bộ. Chúng có hiệu lực từ vị trí được khai báo đến hết khối hoặc hàm bao quanh. Các biến được khai báo trong các khối lồng nhau sẽ che khuất (shadow) các biến trùng tên ở phạm vi ngoài.

---

## Nhập và xuất

Để thực hiện thao tác nhập/xuất, TyC cung cấp các hàm dựng sẵn (built-in) sau:

| **Khai báo hàm**                  | **Ngữ nghĩa**                 |
| --------------------------------- | ----------------------------- |
| `int readInt();`                  | Đọc một số nguyên từ bàn phím |
| `float readFloat();`              | Đọc một số thực từ bàn phím   |
| `string readString();`            | Đọc một chuỗi từ bàn phím     |
| `void printInt(int value);`       | Ghi một số nguyên ra màn hình |
| `void printFloat(float value);`   | Ghi một số thực ra màn hình   |
| `void printString(string value);` | Ghi một chuỗi ra màn hình     |

---

## Chương trình ví dụ

### Ví dụ 1: Hello World

```tyc
void main() {
    printString("Hello, World!");
}
```

### Ví dụ 2: Máy tính đơn giản

```tyc
int add(int x, int y) {
    return x + y;
}

int multiply(int x, int y) {
    return x * y;
}

void main() {
    auto a = readInt();
    auto b = readInt();

    auto sum = add(a, b);
    auto product = multiply(a, b);

    printInt(sum);
    printInt(product);
}
```

### Ví dụ 3: Vòng lặp kèm điều kiện

```tyc
void main() {
    auto n = readInt();
    auto i = 0;

    while (i < n) {
        printInt(i);
        ++i;
    }

    for (auto j = 0; j < n; ++j) {
        if (j % 2 == 0) {
            printInt(j);
        }
    }
}
```

### Ví dụ 4: Hàm giai thừa

```tyc
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main() {
    auto num = readInt();
    auto result = factorial(num);
    printInt(result);
}
```

### Ví dụ 5: Khai báo biến với khởi tạo tùy chọn

```tyc
void main() {
    // Dùng auto và có khởi tạo
    auto x = readInt();
    auto y = readFloat();
    auto name = readString();

    // Dùng auto nhưng không khởi tạo
    auto sum;
    sum = x + y;              // sum: float (suy luận từ lần dùng đầu - phép gán)

    // Dùng kiểu tường minh và có khởi tạo
    int count = 0;
    float total = 0.0;
    string greeting = "Hello, ";

    // Dùng kiểu tường minh nhưng không khởi tạo
    int i;
    float f;
    i = readInt();            // gán cho int
    f = readFloat();          // gán cho float

    printFloat(sum);
    printString(greeting);
    printString(name);

    // Lưu ý: KHÔNG hỗ trợ nối chuỗi
    // Vì toán tử + chỉ áp dụng cho int hoặc float, không áp dụng cho string
}
```

### Ví dụ 6: Sử dụng struct

```tyc
struct Point {
    int x;
    int y;
};

struct Person {
    string name;
    int age;
    float height;
};

void main() {
    // Khai báo biến struct không khởi tạo
    Point p1;
    p1.x = 10;
    p1.y = 20;

    // Khai báo biến struct có khởi tạo
    Point p2 = {30, 40};

    // Truy cập và chỉnh sửa thành viên
    printInt(p2.x);
    printInt(p2.y);

    // Gán struct
    p1 = p2;  // Sao chép mọi thành viên

    // Sử dụng struct Person
    Person person1 = {"John", 25, 1.75};
    printString(person1.name);
    printInt(person1.age);
    printFloat(person1.height);

    // Sửa thành viên
    person1.age = 26;
    person1.height = 1.76;

    // Dùng struct với auto
    auto p3 = p2;  // p3: Point (suy luận từ phép gán)
    printInt(p3.x);
}
```

---

## Tóm tắt ngữ pháp

Một chương trình TyC bao gồm một dãy các khai báo struct và khai báo hàm.

**Khai báo struct:**

- Mỗi khai báo struct định nghĩa một kiểu tổng hợp mới với các thành viên có tên
- Thành viên struct phải có kiểu tường minh (`int`, `float`, `string`, hoặc một kiểu struct khác)
- Thành viên struct không thể dùng `auto` để suy luận kiểu
- Định nghĩa struct không thể lồng nhau (không có khai báo struct bên trong một khai báo struct khác)
- Tuy nhiên, thành viên struct có thể có kiểu là struct khác (dùng các kiểu struct đã khai báo trước đó)

**Khai báo hàm:**

- Mỗi hàm có:
  - Một kiểu trả về tùy chọn (hoặc có thể suy luận)
  - Một định danh (tên hàm)
  - Danh sách tham số (tùy chọn)
  - Một khối chứa các câu lệnh
- Tên hàm phải là duy nhất (không hỗ trợ nạp chồng)

Các thành phần cấu trúc chính gồm:

- **Struct**: Kiểu tổng hợp với các thành viên có tên và kiểu tường minh
- **Hàm**: Khai báo với kiểu trả về, tham số và thân hàm
- **Câu lệnh**: Khai báo biến, gán, điều khiển luồng (if, while, for, switch-case), break, continue, return, câu lệnh biểu thức và khối
- **Biểu thức**: Biểu thức cơ sở (định danh, literal, biểu thức trong ngoặc, truy cập thành viên), phép toán một ngôi, phép toán hai ngôi theo độ ưu tiên, lời gọi hàm và phép toán hậu tố (tăng/giảm)
- **Kiểu**: `int`, `float`, `string`, `void`, kiểu struct, và suy luận kiểu bằng `auto`
- **Khai báo biến**: Có thể dùng `auto` để suy luận kiểu hoặc dùng kiểu tường minh (`int`, `float`, `string`, hoặc tên kiểu struct)
- **Literal**: Literal số nguyên, số thực và chuỗi

**Độ ưu tiên toán tử** (như mô tả ở phần Biểu thức):

1. Toán tử hậu tố (`++`, `--`)
2. Toán tử tiền tố/một ngôi (`!`, `-`, `+`, `++`, `--`)
3. Truy cập thành viên (`.`)
4. Nhân/chia/lấy dư (`*`, `/`, `%`)
5. Cộng/trừ (`+`, `-`)
6. Quan hệ (`<`, `<=`, `>`, `>=`)
7. Bằng/khác (`==`, `!=`)
8. AND logic (`&&`)
9. OR logic (`||`)
10. Gán (`=`)

**Lưu ý**: Các luật ngữ pháp đầy đủ phải do sinh viên định nghĩa trong file ngữ pháp ANTLR4 (`TyC.g4`). Đặc tả này cung cấp các yêu cầu và ví dụ, nhưng việc cài đặt ngữ pháp chi tiết là một phần của bài tập.

---

**Hết đặc tả**
