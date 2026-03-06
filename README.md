# run-study

## Windows 用户：无需 Python，直接双击单文件运行
如果你是 Windows 系统，并且不想跑 Python，请直接使用仓库里的：

- `windows-ppt2pdf.hta`

使用方法：
1. 确保电脑已安装 **Microsoft PowerPoint**。
2. 双击 `windows-ppt2pdf.hta` 打开工具。
3. 选择“输入文件夹”（放 `.ppt/.pptx`）和“输出文件夹”。
4. 点击“开始批量转换”。

> 说明：`.hta` 是 Windows 的 HTML Application，本质是单文件 HTML 应用，可直接在本机调用 PowerPoint 做转换。

---

## Python Web 版（可选）
一个网页端批量 PPT 转 PDF 工具（FastAPI）。

### 快速启动
```bash
pip install -r requirements.txt
python run.py
```

### 手动启动
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
浏览器访问：`http://localhost:8000`

## 功能
- 支持一次上传多个 `.ppt` / `.pptx` 文件。
- Web 版后端调用 LibreOffice (`soffice`) 进行转换。
- Windows 单文件版调用本机 PowerPoint COM 进行转换。
