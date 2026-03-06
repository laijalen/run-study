const form = document.getElementById('convert-form');
const input = document.getElementById('files');
const fileList = document.getElementById('file-list');
const statusNode = document.getElementById('status');
const submitBtn = document.getElementById('submit-btn');
const uploadBox = document.querySelector('.upload-box');

const renderFileList = () => {
  fileList.innerHTML = '';
  const files = [...input.files];
  files.forEach((file) => {
    const item = document.createElement('li');
    item.textContent = file.name;
    fileList.appendChild(item);
  });
};

input.addEventListener('change', renderFileList);

['dragenter', 'dragover'].forEach((eventName) => {
  uploadBox.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadBox.classList.add('dragover');
  });
});

['dragleave', 'drop'].forEach((eventName) => {
  uploadBox.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadBox.classList.remove('dragover');
  });
});

uploadBox.addEventListener('drop', (event) => {
  const dt = event.dataTransfer;
  if (!dt?.files?.length) {
    return;
  }
  input.files = dt.files;
  renderFileList();
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!input.files.length) {
    statusNode.textContent = '请先选择至少一个文件。';
    return;
  }

  submitBtn.disabled = true;
  statusNode.textContent = '正在转换，请稍候...';

  const formData = new FormData();
  [...input.files].forEach((file) => formData.append('files', file));

  try {
    const resp = await fetch('/api/convert', {
      method: 'POST',
      body: formData,
    });

    if (!resp.ok) {
      const errorData = await resp.json();
      throw new Error(errorData.detail || '转换失败');
    }

    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'converted_pdfs.zip';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    statusNode.textContent = '转换成功，已开始下载 ZIP 文件。';
  } catch (error) {
    statusNode.textContent = `转换失败：${error.message}`;
  } finally {
    submitBtn.disabled = false;
  }
});
