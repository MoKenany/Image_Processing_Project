# الشرح الشامل لبرنامج معالجة الصور (Image Processing)

هذا الملف مصمم لكي يشرح لك كل سطر، كل دالة، وكل كلمة في كود البرنامج بالتفصيل الممل، كما لو كنت تتعلم البرمجة من الصفر.

---

## 1. استدعاء المكتبات (Imports)
في بداية أي كود بايثون، نقوم بجلب "أدوات جاهزة" (مكتبات) لكي نستخدمها بدل كتابة كل شيء من الصفر.

```python
import customtkinter as ctk
```
- `import`: تعني "أحضر لي".
- `customtkinter`: هي مكتبة تُستخدم لصنع واجهات المستخدم (أزرار، نوافذ، الخ) بشكل عصري وجميل (Dark mode).
- `as ctk`: تعني "بدلاً من كتابة الكلمة الطويلة customtkinter كل مرة، سأسميها ctk اختصاراً".

```python
from tkinter import filedialog, messagebox
```
- `tkinter`: هي المكتبة الأساسية في بايثون لعمل النوافذ.
- `filedialog`: أداة تفتح لك نافذة لكي تختار ملف من الكمبيوتر (مثل اختيار صورة لفتحها أو حفظها).
- `messagebox`: أداة لإظهار رسائل منبثقة (Pop-ups) للمستخدم.

```python
from PIL import Image, ImageFilter, ImageEnhance, ImageTk
```
- `PIL` (Pillow): مكتبة شهيرة جداً للتعامل مع الصور في بايثون.
- `Image`: لفتح وتعديل أساسيات الصورة.
- `ImageFilter`: يحتوي على فلاتر جاهزة مثل فلتر زيادة التفاصيل (Detail).
- `ImageEnhance`: للتحكم في الإضاءة والألوان.
- `ImageTk`: لتحويل الصورة إلى صيغة تفهمها نافذة الـ `tkinter` لكي تظهر على الشاشة.

```python
import cv2
```
- `cv2`: مكتبة OpenCV العظيمة، وهي المعيار العالمي لمعالجة الصور والذكاء الاصطناعي الخاص بالرؤية. نستخدمها هنا لتطبيق الفلاتر الهندسية والضوضاء.

```python
import numpy as np
```
- `numpy`: مكتبة للعمليات الرياضية المعقدة. لأن الكمبيوتر يرى الصورة كأنها جدول (مصفوفة - Matrix) مليء بالأرقام، نستخدم numpy لتعديل هذه الأرقام (مثل إضافة النويز). و `as np` لاختصار الاسم.

---

## 2. إعدادات شكل البرنامج
```python
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
```
- `set_appearance_mode("dark")`: تجعل خلفية البرنامج سوداء (الوضع الليلي المريح للعين).
- `set_default_color_theme("blue")`: تجعل اللون الأساسي للأزرار أزرق.

---

## 3. تعريف البرنامج (الكلاس الرئيسي)
```python
class AdvancedVisionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
```
- `class`: الكلاس هو القالب الذي نبني به البرنامج.
- `AdvancedVisionApp`: اسم اخترناه لبرنامجنا.
- `(ctk.CTk)`: تعني أن برنامجنا سيرث خصائص النافذة الرئيسية من مكتبة الواجهات.
- `def __init__(self):`: الدالة التي يتم تشغيلها **أولاً وتلقائياً** بمجرد فتح البرنامج. 
- `super().__init__()`: سطر إجباري لتجهيز النافذة الرئيسية في الخلفية.

```python
        self.title("Vision Pro - Advanced Multi-Layer Editor")
        self.geometry("1350x800")
```
- `self.title`: يحدد النص الذي يظهر أعلى شريط النافذة.
- `self.geometry`: يحدد عرض وارتفاع النافذة عند فتحها (1350 بيكسل عرض، 800 طول).

---

## 4. متغيرات تخزين الصور (Image Data)
```python
        self.original_pil = None
        self.current_processed_pil = None
        self.history = [] 
        self.input_tk = None
        self.output_tk = None
```
هنا نقوم بتجهيز "صناديق فارغة" (`None`) لنضع فيها الصور لاحقاً:
- `original_pil`: سيحتفظ بالصورة الأصلية التي تم استيرادها بدون أي تعديل.
- `current_processed_pil`: سيحتفظ بالصورة بعد كل تعديل يتم عليها (الصورة الحالية).
- `history`: قائمة (List) فارغة `[]` سنخزن فيها كل خطوة قمنا بها لكي نتمكن من التراجع (Undo).
- `input_tk` و `output_tk`: متغيرات لتخزين الصورة بصيغة تقبل العرض على الشاشة.

---

## 5. تقسيم الشاشة (Layout)
```python
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
```
- الشاشة مقسمة لجدول (Grid).
- `weight=1`: تعني "خذ كل المساحة المتبقية". هنا نقول أن العمود رقم 1 (الذي فيه الصور) يجب أن يتمدد ليأخذ باقي الشاشة.

---

## 6. تصميم الشريط الجانبي (Sidebar)
```python
        self.sidebar = ctk.CTkScrollableFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
```
- `CTkScrollableFrame`: إطار يمكن النزول فيه للأسفل (Scroll) عرضه 300 بيكسل، وحوافه غير دائرية (corner_radius=0).
- `grid(...)`: يضع هذا الإطار في الصف 0، والعمود 0 (على اليسار). `sticky="nsew"` تعني تمدد الإطار في كل الاتجاهات الأربعة (شمال، جنوب، شرق، غرب) ليملأ مكانه.

```python
        ctk.CTkLabel(self.sidebar, text="CONTROL PANEL", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
```
- `CTkLabel`: نص عادي يكتب على الشاشة (ليس زر).
- `text`: النص هو "CONTROL PANEL".
- `font`: حجم الخط 20 ونوعه عريض (bold).
- `.pack(pady=20)`: وضع النص في الشاشة وترك مسافة 20 بيكسل فوقه وتحته.

### الأزرار الرئيسية (Import, Undo, Reset, Save)
```python
        self.btn_import = ctk.CTkButton(self.sidebar, text="IMPORT IMAGE", fg_color="#27ae60", command=self.load_image)
        self.btn_import.pack(pady=10, padx=20, fill="x")
```
- `CTkButton`: زر قابل للضغط.
- `fg_color`: لونه أخضر (`#27ae60`).
- `command=self.load_image`: **أهم جزء!** هذا يربط الزر بدالة اسمها `load_image` (سيتم شرحها لاحقاً) لكي تنفذ الأوامر عند الضغط عليه.
- `fill="x"`: تجعل الزر يتمدد بالعرض ليملأ الشريط.

*(باقي الأزرار نفس الفكرة: زر Undo، زر Reset، زر Save).*

---

## 7. إضافة الفلاتر
لأن الأكواد ستتكرر للأزرار، تم عمل دوال مساعدة لإنشاء الأزرار بسهولة:

```python
        self.add_section("GEOMETRIC OPERATIONS")
        self.create_edit_btn("Flip Horizontal", "flip_h")
```
هنا نستدعي دوال (سنشرحها بالأسفل) لعمل عناوين للأقسام وأزرار، مثلاً `create_edit_btn` تأخذ اسم الزر الذي يراه المستخدم، والكلمة السرية `flip_h` التي سيفهمها كود المعالجة. تم تكرار هذا لكل الفلاتر.

---

## 8. منطقة عرض الصور (Viewport)
```python
        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
```
- إطار شفاف نضعه في العمود رقم 1 (على اليمين) لعرض الصور.

```python
        self.input_label = self.create_image_slot(self.view_container, "ORIGINAL", 0)
        self.output_label = self.create_image_slot(self.view_container, "CURRENT RESULT", 1, color="#1abc9c")
```
- قمنا بعمل مكان للصورة الأصلية، ومكان آخر لنتيجة التعديل (وكلها تستخدم دالة مساعدة سنشرحها الآن).

---

## 9. الدوال المساعدة (Helper Functions)
```python
    def add_section(self, txt):
        ctk.CTkLabel(self.sidebar, text=txt, font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db").pack(pady=(20, 5))
```
- دالة تأخذ نص `txt` وتطبعه كعنوان لونه أزرق فاتح (`#3498db`) لتقسيم الشريط الجانبي.

```python
    def create_edit_btn(self, txt, mode):
        btn = ctk.CTkButton(self.sidebar, text=txt, command=lambda: self.apply_cumulative_filter(mode), fg_color="#34495e")
        btn.pack(pady=2, padx=30, fill="x")
```
- دالة تصنع أزرار الفلاتر.
- `command=lambda: self.apply_cumulative_filter(mode)`: `lambda` هي طريقة لإرسال "باراميتر" (معلومة إضافية) للدالة عند الضغط على الزر. المعلومة هي `mode` (مثلاً: `gray`, `flip_h` ... الخ).

---

## 10. تشغيل الأزرار الرئيسية

### دالة تحميل الصورة (load_image)
```python
    def load_image(self):
        path = filedialog.askopenfilename()
```
- تفتح نافذة للبحث عن صورة في الكمبيوتر. المتغير `path` سيحفظ "مسار" الصورة (مثلاً C:/images/pic.png).

```python
        if path:
            img = Image.open(path).convert("RGB")
```
- `if path`: إذا اختار المستخدم صورة فعلاً (ولم يلغِ النافذة).
- `Image.open`: تفتح الصورة، و `convert("RGB")` تجبر الصورة أن تكون بنظام الألوان الأحمر والأخضر والأزرق (حتى لو كانت أبيض وأسود) لمنع الأخطاء البرمجية اللاحقة.

```python
            img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
```
- `thumbnail`: تقوم بتصغير الصورة بحيث لا يزيد طولها أو عرضها عن 1000 بيكسل. هذا مهم جداً لمنع التطبيق من التهنيج مع الصور الضخمة.

```python
            self.original_pil = img
            self.current_processed_pil = self.original_pil.copy()
            self.history = [self.original_pil.copy()]
            self.update_view(is_input=True)
            self.update_view(is_input=False)
            self.btn_save.configure(state="normal")
```
- نحفظ الصورة في `original_pil`.
- نأخذ نسخة للـ `current_processed_pil` (التي سنتلاعب بها).
- نحفظ النسخة الأولى في قائمة `history`.
- نحدث الشاشة لعرض الصور (`update_view`).
- نفعل زر الحفظ (نجعله `normal` بعد أن كان معطلاً).

### دالة التراجع (undo_last)
```python
    def undo_last(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current_processed_pil = self.history[-1].copy()
            self.update_view(is_input=False)
```
- تتأكد أن قائمة التاريخ فيها أكثر من خطوة.
- `.pop()`: تحذف آخر خطوة من التاريخ.
- `self.history[-1]`: تأخذ الصورة التي قبلها مباشرة (آخر عنصر متبقي في القائمة) وتجعلها هي الصورة الحالية.

### دالة الاستعادة للأصل (reset_image)
```python
    def reset_image(self):
        if self.original_pil:
            self.current_processed_pil = self.original_pil.copy()
            self.history = [self.original_pil.copy()]
```
- ترجع الصورة الحالية إلى النسخة الأصلية بالضبط، وتمسح كل التاريخ السابق.

---

## 11. قلب البرنامج: دالة معالجة الصور (apply_cumulative_filter)
هذه الدالة هي العقل المدبر. تأخذ كلمة `mode` وتنفذ المعالجة الرياضية المناسبة:

```python
    def apply_cumulative_filter(self, mode):
        if not self.current_processed_pil: return
```
- إذا لم تكن هناك صورة أصلاً، أنهي الدالة فوراً ولا تفعل شيء.

```python
        if self.current_processed_pil.mode != "RGB":
            self.current_processed_pil = self.current_processed_pil.convert("RGB")
```
- أمان إضافي: يتأكد أن الصورة دائماً نظام ألوانها RGB قبل البدء.

```python
        cv_img = cv2.cvtColor(np.array(self.current_processed_pil), cv2.COLOR_RGB2BGR)
```
- هذه أخطر وأهم خطوة: مكتبة PIL تقرأ الألوان بترتيب (أحمر، أخضر، أزرق RGB). لكن مكتبة OpenCV الخوارزمية تقرأهم بالعكس (أزرق، أخضر، أحمر BGR).
- `np.array`: تحول صورة PIL إلى جدول أرقام رياضي (مصفوفة).
- `cv2.cvtColor`: تعكس الألوان من RGB إلى BGR لكي تعمل فلاتر الـ OpenCV بشكل صحيح.

### عمليات هندسية
```python
        if mode == "flip_h":
            res = cv2.flip(cv_img, 1) 
            self.current_processed_pil = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
```
- `cv2.flip(..., 1)`: يعكس الصورة أفقياً (كأنك تنظر في مرآة). رقم 1 يعني أفقياً، ورقم 0 يعني رأسياً.
- السطر الثاني يحول النتيجة `res` من BGR إلى RGB مرة أخرى، ثم يرجعها لصيغة PIL لتُعرض في البرنامج.

```python
        elif mode == "crop":
            w, h = self.current_processed_pil.size
            box = (w*0.25, h*0.25, w*0.75, h*0.75)
            self.current_processed_pil = self.current_processed_pil.crop(box)
```
- نأخذ عرض `w` وطول `h` الصورة.
- نحدد صندوق القطع (يبدأ من الربع 25% وينتهي في الثلاث أرباع 75%) ليقطع قلب الصورة فقط.

### النويز والفلاتر
```python
        elif mode == "median":
            res = cv2.medianBlur(cv_img, 5)
```
- `medianBlur`: فلتر إزالة نويز (خاصة الـ Salt & Pepper). يأخذ مربع حجمه 5x5 بيكسل، يرتب الألوان بداخله، ويختار اللون الأوسط (الوسيط). هذا يلغي أي نقطة بيضاء أو سوداء شاذة!

```python
        elif mode == "noise_gaussian":
            noise = np.random.normal(0, 25, cv_img.shape).astype(np.float32)
            noisy = cv2.add(cv_img.astype(np.float32), noise)
            res = np.clip(noisy, 0, 255).astype(np.uint8)
```
- `np.random.normal(0, 25, ...)`: يولد أرقام عشوائية (نويز) متوسطها 0 وشدتها 25.
- `cv2.add`: يجمع هذه الأرقام العشوائية مع أرقام الصورة الأصلية (البيكسلات).
- `np.clip`: يضمن أن القيم الناتجة لا تزيد عن 255 (الحد الأقصى للون الأبيض) ولا تقل عن 0 (الحد الأدنى للون الأسود).

```python
        elif mode == "noise_sp":
            res = cv_img.copy()
            prob = 0.05
            white_noise = np.random.rand(res.shape[0], res.shape[1]) < (prob / 2)
            black_noise = np.random.rand(res.shape[0], res.shape[1]) < (prob / 2)
            res[white_noise] = [255, 255, 255]
            res[black_noise] = [0, 0, 0]
```
- `prob = 0.05`: احتمال النويز هو 5%.
- نولد مصفوفة احتمالات ونرى أين تقع تحت 2.5% لنجعلها أبيض `[255,255,255]`، وأين تقع لتكون أسود `[0,0,0]`. هذا يصنع تأثير نقط الملح (أبيض) والفلفل (أسود).

```python
        elif mode == "canny":
            res = cv2.Canny(cv_img, 100, 200)
```
- `Canny`: أشهر خوارزمية لاستخراج حواف الصورة (Edge Detection). تبحث عن أي اختلاف حاد في الألوان. (100 و 200 هي العتبات الدنيا والقصوى لتحديد الحافة).

### الألوان والسطوع
```python
        elif mode == "invert_np":
            res_array = 255 - np.array(self.current_processed_pil)
            self.current_processed_pil = Image.fromarray(res_array)
```
- لعكس الألوان (النيجاتيف): نقوم بطرح قيمة كل بيكسل من 255. (الأبيض 255 يصبح 0 أسود، والعكس).

```python
        elif mode == "brightness":
            enhancer = ImageEnhance.Brightness(self.current_processed_pil)
            self.current_processed_pil = enhancer.enhance(1.5)
```
- يستخدم مكتبة PIL الجاهزة لزيادة السطوع (Brightness) بنسبة مرة ونصف (1.5).

### ختام الدالة
```python
        self.history.append(self.current_processed_pil.copy())
        self.update_view(is_input=False)
```
- بعد أي عملية، ننسخ النتيجة ونضيفها لـ `history` لكي يعمل زر التراجع.
- نستدعي دالة تحديث الشاشة لتظهر النتيجة الجديدة.

---

## 12. تحديث الشاشة وعرض الصور (update_view)
```python
    def update_view(self, is_input=True):
        img = self.original_pil if is_input else self.current_processed_pil
        temp = img.copy()
        temp.thumbnail((500, 500), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(temp)
```
- الشاشة لا يمكن أن تعرض صورة بحجمها الكامل (1000 بيكسل) لأنها ستخرج عن الإطار.
- هنا نأخذ نسخة مصغرة `thumbnail` بحجم أقصاه 500x500 بيكسل.
- `ImageTk.PhotoImage`: هذا يحول الصورة إلى صيغة يفهمها برنامج الواجهة (Tkinter).

```python
        if is_input:
            self.input_tk = tk_img
            self.input_label.configure(image=self.input_tk, text="")
        else:
            self.output_tk = tk_img
            self.output_label.configure(image=self.output_tk, text="")
```
- إذا كنا نحدث الصورة الأصلية (is_input)، نضعها في الجانب الأيسر.
- إذا كانت الصورة المعدلة (Output)، نضعها في الجانب الأيمن.
- `text=""` تحذف النص الافتراضي ("Import an image").

---

## 13. زر التشغيل (التشغيل الرئيسي)
```python
if __name__ == "__main__":
    app = AdvancedVisionApp()
    app.mainloop()
```
- هذا السطر الأخير يخبر بايثون: "إذا قمت بتشغيل هذا الملف بشكل مباشر، قم بإنشاء نسخة من برنامجنا `AdvancedVisionApp()`".
- `app.mainloop()`: هذه الدالة تحافظ على بقاء البرنامج مفتوحاً على الشاشة ينتظر ضغطات المستخدم، ولولاها لظهر البرنامج واختفى في جزء من الثانية!
