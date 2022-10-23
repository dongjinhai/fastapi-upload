# -*- encoding:utf-8 -*-
import os
from typing import List
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.background import BackgroundTasks
from starlette.background import BackgroundTask

app = FastAPI()
root_path = Path(__file__).parent.__str__()


@app.get('/')
def index():
    return {'message': 'Hello World'}


# @app.post('/uploadfiles')
# async def create_upload_file(files: List[UploadFile] = File(...)):
#     for file in files:
#         res = await file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(res)
    
#     return {'message': 'success'}


@app.get('/xmindtoexcel')
async def xmind_to_excel():
    content = ''
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    return HTMLResponse(content=content)


@app.post('/uploadxmindfile')
async def handle_upload_file(file: UploadFile):
    """处理单个上传文件"""
    res = await file.read()
    p = Path(root_path).joinpath('files', file.filename).__str__()
    with open(p, 'wb') as f:
        f.write(res)
    
    return {'message': 'success'}


@app.get('/downloadexcelfile')
async def download_excel_file(filename: str):
    print(filename)
    """下载xmind文件处理后的xmind文件"""
    reps_filename = 'dongjinhai.py'
    filepath = Path(root_path).joinpath('excel', filename)
    resp = FileResponse('main.py', background=BackgroundTask(lambda: print('KKK')), media_type='py')
    resp.headers['Content-Disposition'] = f"attachment; filename={reps_filename}"

    return resp

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=9527)
