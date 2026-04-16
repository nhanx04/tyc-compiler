# Ngôn ngữ lập trình TyC - Ràng buộc ngữ nghĩa và các loại lỗi

**Tài liệu tham chiếu Phân tích ngữ nghĩa tĩnh**  
**Phiên bản 1.0 - Tháng 01/2026**

## Tổng quan

Tài liệu này mô tả đầy đủ các ràng buộc ngữ nghĩa và loại lỗi mà bộ kiểm tra ngữ nghĩa tĩnh của TyC phải phát hiện. TyC là ngôn ngữ thủ tục có suy luận kiểu hoàn chỉnh, hỗ trợ `struct`, và kiểm tra kiểu chặt chẽ: mỗi toán tử có yêu cầu kiểu rõ ràng.

## Tóm tắt các loại lỗi

Bộ kiểm tra ngữ nghĩa tĩnh TyC phải phát hiện và báo cáo các lỗi sau:

1. **Redeclared** - Khai báo trùng biến, hàm, struct, tham số, hoặc thành viên struct (bao gồm biến cục bộ trùng tên tham số trong cùng hàm)
2. **UndeclaredIdentifier** - Sử dụng biến/tham số chưa khai báo
3. **UndeclaredFunction** - Gọi hàm chưa khai báo
4. **UndeclaredStruct** - Sử dụng kiểu struct chưa khai báo
5. **TypeCannotBeInferred** - `auto` không suy ra được kiểu; thông báo dạng `TypeCannotBeInferred(<ctx>)` với `<ctx>` là một AST node (`str` theo `src/utils/nodes.py`)
6. **TypeMismatchInStatement** - Sai kiểu trong câu lệnh (if, while, for, return, assignment)
7. **TypeMismatchInExpression** - Sai kiểu trong biểu thức (toán tử, gọi hàm, truy cập thành viên, struct literal theo kiểu kỳ vọng)
8. **MustInLoop** - `break`/`continue` nằm ngoài ngữ cảnh vòng lặp

---

## Đặc tả chi tiết các loại lỗi

### 1. Redeclared Variable/Function/Struct/Parameter/Member (Khai báo trùng)

**Quy tắc:** Mọi khai báo phải duy nhất trong phạm vi tương ứng theo đặc tả TyC.

**Ngoại lệ:** `Redeclared(<kind>, <identifier>)`
- `<kind>`: loại thực thể bị khai báo trùng (`Variable`, `Function`, `Struct`, `Parameter`, `Member`)
- `<identifier>`: tên bị trùng

**Quy tắc theo phạm vi:**
- **Phạm vi toàn cục:** tên struct phải duy nhất trong các struct; tên hàm phải duy nhất trong các hàm (không overloading). **Tên struct và tên hàm là hai namespace khác nhau** nên có thể trùng nhau.
- **Phạm vi hàm:** tham số thuộc phạm vi hàm, nhìn thấy trong toàn bộ thân hàm. Tên tham số trong cùng danh sách tham số phải duy nhất. **Không được khai báo biến cục bộ trùng tên tham số ở bất kỳ block lồng nhau nào trong cùng hàm** (báo `Redeclared(Variable, <name>)`).
- **Phạm vi block cục bộ:** biến trong cùng block phải duy nhất.
- **Shadowing:** block lồng nhau có thể che khuất biến cục bộ của block ngoài (nhưng không được che tham số của hàm).

### 2. Undeclared Identifier (Định danh chưa khai báo)

**Quy tắc:** Mọi biến/tham số phải được khai báo trước khi sử dụng.

**Ngoại lệ:** `UndeclaredIdentifier(<identifier>)`

**Quy tắc phân giải định danh:**
- Tìm từ scope trong cùng ra ngoài
- Biến phải được khai báo trước khi dùng trong scope hiện tại hoặc scope bao ngoài
- Biểu thức khởi tạo của một biến được kiểm tra khi chính biến đó **chưa** vào scope
- Tham số nhìn thấy trong toàn bộ thân hàm
- TyC không có biến toàn cục (toàn cục chỉ có khai báo hàm/struct)

### 3. Undeclared Function (Hàm chưa khai báo)

**Quy tắc:** Hàm phải được khai báo trước khi gọi.

**Ngoại lệ:** `UndeclaredFunction(<function-name>)`

**Quy tắc hàm:**
- Hàm thuộc phạm vi toàn cục
- Lời gọi hợp lệ khi hàm đã được khai báo trước điểm gọi
- Không overloading
- Hàm dựng sẵn được xem như đã khai báo ngầm: `readInt`, `readFloat`, `readString`, `printInt`, `printFloat`, `printString`

### 4. Undeclared Struct (Struct chưa khai báo)

**Quy tắc:** Kiểu struct phải được khai báo trước khi dùng.

**Ngoại lệ:** `UndeclaredStruct(<struct-name>)`

**Quy tắc struct:**
- Struct thuộc phạm vi toàn cục
- Tên struct duy nhất trong tập struct
- Thành viên struct không được dùng `auto`
- Kiểu thành viên không được là chính struct đang khai báo

### 5. Type Cannot Be Inferred (Không thể suy luận kiểu)

**Quy tắc:** Mọi binding `auto` phải được chốt kiểu từ khởi tạo hoặc từ lần dùng ràng buộc kiểu về sau.

**Ngoại lệ:** `TypeCannotBeInferred(<ctx>)` với `<ctx>` là AST node đầu tiên gây bế tắc suy luận (định dạng `__str__` của `src/utils/nodes.py`).

**Nguyên tắc suy luận:**
- Có khởi tạo → suy ra từ biểu thức khởi tạo
- Không khởi tạo → suy ra từ lần sử dụng đầu tiên có đủ ràng buộc
- Nếu vẫn mơ hồ hoặc không được dùng để chốt kiểu → báo lỗi này

**Quy tắc báo lỗi:**
- Mỗi lần chạy chỉ báo một lỗi ngữ nghĩa
- Với `TypeCannotBeInferred`, báo lỗi đầu tiên gặp trong thứ tự duyệt ngữ nghĩa

### 6. Type Mismatch In Statement (Sai kiểu trong câu lệnh)

**Quy tắc:** Mọi câu lệnh phải thỏa quy tắc kiểu của TyC.

**Ngoại lệ:** `TypeMismatchInStatement(<statement>)`

**Quy tắc kiểu cho câu lệnh:**
- **if/while/for:** điều kiện phải có kiểu `int`
- **for:** init/condition/update phải hợp lệ theo quy tắc riêng; condition vẫn phải là `int`
- **gán (`ExprStmt` chứa `AssignExpr`):** vế trái và vế phải cùng kiểu; gán struct phải cùng đúng kiểu struct; không ép kiểu ngầm trong phép gán
- **struct literal ở vế phải:** nếu sai số trường hoặc sai kiểu từng trường theo kiểu struct kỳ vọng thì lỗi là **`TypeMismatchInExpression(<StructLiteral>)`**
- **return:**
  - hàm `void` chỉ hợp lệ với `return;`
  - hàm non-void phải `return <expr>;` cùng kiểu trả về
  - hàm suy luận kiểu trả về: kiểu được chốt theo các return-value hợp lệ đầu tiên; các return-value sau phải đồng nhất
- **switch:** biểu thức switch phải là `int`; nhãn case phải là hằng số nguyên hoặc biểu thức hằng đánh giá ra `int`

**Hành vi của biểu thức gán:**
- Gán là biểu thức, không chỉ là câu lệnh
- Kết hợp phải: `x = y = z = 10` → `x = (y = (z = 10))`
- Giá trị của biểu thức gán là giá trị của LHS sau khi gán
- Kiểu của biểu thức gán là kiểu của LHS
- LHS phải là identifier hoặc member access
- Có thể dùng trong ngữ cảnh biểu thức: `int y = (x = 5) + 7;`

### 7. Type Mismatch In Expression (Sai kiểu trong biểu thức)

**Quy tắc:** Mọi biểu thức phải thỏa quy tắc kiểu cho toán tử/phép toán của TyC.

**Ngoại lệ:** `TypeMismatchInExpression(<expression>)`

**Quy tắc kiểu cho biểu thức:**
- **`+ - * /`**: 2 toán hạng phải là `int` hoặc `float`; kết quả `int` nếu cả hai là `int`, ngược lại `float`
- **`%`**: cả hai toán hạng phải là `int`, kết quả `int`
- **`== != < <= > >=`**: toán hạng phải là `int`/`float`, kết quả `int`
- **`&& ||`**: cả hai toán hạng kiểu `int`, kết quả `int`
- **`!`**: toán hạng kiểu `int`, kết quả `int`
- **`++ --` (prefix/postfix)**: toán hạng kiểu `int`, đồng thời phải là identifier hoặc member access
- **`.` (member access)**: vế trái phải là kiểu struct; vế phải phải là thành viên hợp lệ của struct đó; kiểu kết quả là kiểu của thành viên
- **gọi hàm**: số lượng tham số thực phải khớp số tham số hình thức; kiểu từng đối số phải khớp (không ép kiểu); kiểu kết quả là kiểu trả về
- **struct literal theo kiểu kỳ vọng**: số trường và kiểu từng trường phải khớp đúng struct đích; sai thì báo `TypeMismatchInExpression(<StructLiteral>)`
- **biểu thức gán**: LHS phải là identifier hoặc member access; hai vế phải cùng kiểu; kiểu kết quả là kiểu LHS

### 8. Break/Continue Not In Loop (break/continue ngoài vòng lặp)

**Quy tắc:** `break` và `continue` chỉ hợp lệ trong vòng lặp (`for`, `while`).

**Ngoại lệ:** `MustInLoop(<statement>)`

**Quy tắc ngữ cảnh vòng lặp:**
- `break`/`continue` hợp lệ khi nằm trong thân `for` hoặc `while`
- `break` cũng hợp lệ trong `switch`; `continue` thì không
- Có thể nằm trong `if` lồng bên trong vòng lặp
- Không được “kế thừa” ngữ cảnh vòng lặp qua biên hàm
- Phải nằm trong scope từ vựng của vòng lặp

---

## Hướng dẫn cài đặt

### Thứ tự ưu tiên phát hiện lỗi

**Duyệt một lần, lỗi đầu tiên thắng (toàn chương trình).** Checker thực hiện một lượt duyệt ngữ nghĩa (thường DFS). Chỉ báo **một** lỗi duy nhất: lỗi ngữ nghĩa đầu tiên gặp theo thứ tự duyệt đã chọn.

- Có thể có pass nội bộ/deferred check (ví dụ suy luận kiểu trả về), miễn là quy tắc báo lỗi vẫn là “lỗi đầu tiên theo thứ tự duyệt”.
- Các “tier” chỉ dùng để phân loại và tie-break **trong cùng tier**, không phải hàng đợi ưu tiên toàn cục vượt lên thứ tự duyệt thực tế.

**Các tầng lỗi (để tài liệu hóa và tie-break cùng tầng):**
1. **Lỗi khai báo**: Redeclared, UndeclaredIdentifier, UndeclaredFunction, UndeclaredStruct
2. **Lỗi suy luận kiểu**: TypeCannotBeInferred
3. **Lỗi kiểu**: TypeMismatchInStatement, TypeMismatchInExpression
4. **Lỗi điều khiển luồng**: MustInLoop

Trong cùng một tầng: nếu có nhiều lỗi cùng tầng xuất hiện trước khi dừng, báo lỗi đầu tiên theo thứ tự duyệt.

### Quản lý phạm vi

Mô hình phạm vi từ vựng (block, shadowing, phạm vi `for` init và thân vòng lặp) được định nghĩa chuẩn trong `tyc_specification.md` mục **Scope Rules**. Checker nên bám theo mô hình này.

- **Phạm vi toàn cục:** hàm và struct (mỗi loại tên duy nhất trong chính loại đó; tên hàm và tên struct có thể trùng nhau)
- **Phạm vi hàm:** tham số nhìn thấy trong toàn bộ thân hàm; biến local không được trùng tên tham số
- **Phạm vi block cục bộ:** biến khai báo trong `{}`
- **Phạm vi lồng nhau:** block trong có thể che biến local ngoài (không che tham số hàm)

### Hệ thống suy luận kiểu

TyC dùng suy luận kiểu hoàn chỉnh theo các quy tắc:
1. **Literal**: `int` / `float` / `string` như thông thường
2. **`auto`**: có init thì suy từ init; không init thì suy từ lần dùng đầu tiên có ràng buộc
3. **Thất bại suy luận**: mơ hồ hoặc không chốt được kiểu → `TypeCannotBeInferred(<ctx>)`
4. **Biểu thức**: áp dụng quy tắc toán tử/toán hạng sau khi kiểu đã biết
5. **Giá trị trả về hàm**: có thể tường minh hoặc suy từ toàn bộ các return của hàm (theo Rule 5 trong specification)

### Quy tắc hệ kiểu

- Kiểu chặt: không ép kiểu ngầm, ngoại trừ quy tắc số học `int + float -> float`
- Không overloading hàm
- Kiểu struct phải khai báo trước khi dùng
- `void` chỉ dùng làm kiểu trả về của hàm, không dùng cho biến/tham số

### Hàm dựng sẵn

Các hàm sau được khai báo ngầm định:
- `int readInt()`
- `float readFloat()`
- `string readString()`
- `void printInt(int value)`
- `void printFloat(float value)`
- `void printString(string value)`

### Điểm vào chương trình

Chương trình TyC phải có ít nhất một hàm `main` không tham số và trả về `void`. Đây là entry point của chương trình.

---

*Tài liệu dành cho Phân tích ngữ nghĩa tĩnh TyC*  
*Cập nhật lần cuối: Tháng 04/2026*
