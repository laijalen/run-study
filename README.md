# run-study

一个网页端批量 PPT 转 PDF 工具（FastAPI）。

## 你要的“直接打开网页就使用”
先启动服务，然后浏览器会自动打开到工具页面：

```bash
python run.py
```

打开后直接上传多个 `.ppt/.pptx` 即可转换并下载 ZIP。

## 手动启动（可选）
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 安装 LibreOffice 并确保 `soffice` 在 PATH 中。
3. 启动服务：
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. 浏览器访问：`http://localhost:8000`

## 功能
- 支持一次上传多个 `.ppt` / `.pptx` 文件。
- 后端调用 LibreOffice (`soffice`) 进行转换。
- 将全部 PDF 打包为 `converted_pdfs.zip` 自动下载。

## 注意事项
- 服务端必须有 LibreOffice；否则无法执行 PPT 到 PDF 的转换。
- 上传的原始文件和中间产物存放在临时目录，处理完成后会清理。
