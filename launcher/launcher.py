import gradio as gr
import json
import subprocess
import os
import signal
import time
import openi
import zipfile

def load_llm_list(file_path):
    # 初始化一个空列表
    model_list = []

    # 打开文件并逐行读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行末的换行符并添加到列表中
            model_list.append(line.strip())
    return model_list

def load_tts_list(file_path):
    # 初始化一个空列表
    model_list = []

    # 打开文件并逐行读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行末的换行符并添加到列表中
            model_list.append(line.strip())
    return model_list

def load_ttl_list(file_path):
    # 初始化一个空列表
    model_list = []

    # 打开文件并逐行读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行末的换行符并添加到列表中
            model_list.append(line.strip())
    return model_list

def load_ttm_list(file_path):
    # 初始化一个空列表
    model_list = []

    # 打开文件并逐行读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行末的换行符并添加到列表中
            model_list.append(line.strip())
    return model_list

def write_model_to_json(model1, model2, model3, model4):
    """将选中的模型写入JSON文件"""
    json_file = 'G:\\digital-wife\\launcher\\config\\launch.json'
    with open(json_file, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data['llm'] = model1
        data['tts'] = model2
        data['ttl'] = model3
        data['ttm'] = model4
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.truncate()

processes = []

def start_project(mode):
    if mode == "体验模式（选择该按钮将屏蔽用户配置）":
        choose = "true"
    else:
        choose = "false"
    json_file = 'G:\\digital-wife\\launcher\\config\\launch.json'
    with open(json_file, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data['easy_mode'] = choose
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.truncate()

    # 读取..\\config\\launch.json文件，获取llm、tts、ttl、ttm的值定义为变量的值
    config_path = os.path.join('..', 'config', 'launch.json')
    
    if not os.path.exists(config_path):
        return "配置文件不存在，请检查路径。"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    easy_mode = config.get('easy_mode')
    llm = config.get('llm')
    tts = config.get('tts')
    ttl = config.get('ttl')
    ttm = config.get('ttm')
    
    if not all([llm, tts, ttl, ttm]):
        return "配置文件缺少必要的参数。"

    if easy_mode == 'true':
        try:
            processes.append(subprocess.Popen(os.path.join('..', 'ai', 'letta', 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'ai', 'edge-tts', 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'ai', 'dh-live', 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'ai', 'momask', 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'unity', 'start.bat'), shell=True))
            status = "项目已启动。禁止重复启动，否则后果很严重！"
        except Exception as e:
            status = f"启动项目失败: {str(e)}"
    else:
        # 创建子进程，分别启动..\\ai\\{llm/tts/ttl/ttm}\\start.bat文件
        try:
            processes.append(subprocess.Popen(os.path.join('..', 'ai', llm, 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'ai', tts, 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'ai', ttl, 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'ai', ttm, 'start.bat'), shell=True))
            processes.append(subprocess.Popen(os.path.join('..', 'unity', 'start.bat'), shell=True))
            status = "项目已启动。禁止重复启动，否则后果很严重！"
        except Exception as e:
            status = f"启动项目失败: {str(e)}"
    
    return status

def stop_project():
    global processes
    # 关闭所有子进程
    try:
        for proc in processes:
            proc.send_signal(subprocess.signal.SIGTERM)
            proc.wait()
        processes = []
        status = "项目已停止。"
    except Exception as e:
        status = f"停止项目失败: {str(e)}"
    
    return status

def unzip_file(zip_file_path, extract_to_path):
    """
    解压指定路径的zip文件到目标路径。

    参数:
    zip_file_path (str): 要解压的zip文件路径。
    extract_to_path (str): 解压文件的目标目录路径。
    """
    # 确保目标目录存在
    os.makedirs(extract_to_path, exist_ok=True)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
    print(f"文件已解压到 {extract_to_path}")

def openi_download(demo_name):
    if demo_name == "体验模式":
        # 如果.\\ai下不存在letta、edge-tts、dh-live、momask目录，则下载
        if not os.path.exists(os.path.join('..', 'ai', 'letta')) or not os.path.exists(os.path.join('..', 'ai', 'edge-tts')) or not os.path.exists(os.path.join('..', 'ai', 'dh-live')) or not os.path.exists(os.path.join('..', 'ai', 'momask')):
            openi.download_file(
            repo_id="fyf714/dw-project", 
            file=f"letta.zip", 
            cluster="npu", 
            save_path="..\\temp",
            force=False,
        )
            openi.download_file(
            repo_id="fyf714/dw-project", 
            file=f"edge-tts.zip", 
            cluster="npu", 
            save_path="..\\temp",
            force=False,
        )
            openi.download_file(
            repo_id="fyf714/dw-project", 
            file=f"dh-live.zip",
            cluster="npu", 
            save_path="..\\temp",
            force=False,
        )
            openi.download_file(
            repo_id="fyf714/dw-project", 
            file=f"momask.zip",
            cluster="npu", 
            save_path="..\\temp",
            force=False,
    )
            result = f"已下载{demo_name}。"
        else:
            result = f"{demo_name}已存在。"
        unzip_file(os.path.join('..\\temp', "letta.zip"), os.path.join('..', 'ai'))
        unzip_file(os.path.join('..\\temp', "edge-tts.zip"), os.path.join('..', 'ai'))
        unzip_file(os.path.join('..\\temp', "dh-live.zip"), os.path.join('..', 'ai'))
        unzip_file(os.path.join('..\\temp', "momask.zip"), os.path.join('..', 'ai'))
        unzip_file(os.path.join('..\\temp', "unity.zip"), os.path.join('..', 'ai'))
    else:
        #检测..\\ai\\下是否存在{demo_name}\\目录
        if not os.path.exists(os.path.join('..', 'ai', demo_name)):
            # 下载文件
            openi.download_file(
            repo_id="fyf714/dw-project", 
            file=f"{demo_name}.zip", 
            cluster="npu", 
            save_path="..\\temp",
            force=False,
        )
            result = f"已下载{demo_name}。"
        else:
            result = f"{demo_name}已存在。"
    # 将下载的zip文件解压到..\\ai\\下
        unzip_file(os.path.join('..\\temp', f"{demo_name}.zip"), os.path.join('..', 'ai'))
    return result







# 读取模型列表文件
llm_list_file = 'G:\\digital-wife\\launcher\\config\\llm.list'
llm_list = load_llm_list(llm_list_file)
tts_list_file = 'G:\\digital-wife\\launcher\\config\\tts.list'
tts_list = load_tts_list(tts_list_file)
ttl_list_file = 'G:\\digital-wife\\launcher\\config\\ttl.list'
ttl_list = load_ttl_list(ttl_list_file)
ttm_list_file = 'G:\\digital-wife\\launcher\\config\\ttm.list'
ttm_list = load_ttm_list(ttm_list_file)

# 创建 Gradio 接口
with gr.Blocks() as demo:
    txt1 = gr.Markdown("# Ditigal Wife Launcher")
    with gr.Tab("启动"):
        txt2 = gr.Dropdown(["体验模式（选择该按钮将屏蔽用户配置）", "自定义模式"], label="选择项目运行模式")
        txt3 = gr.Textbox(label="项目运行状态")
        with gr.Column():
            btn2 = gr.Button("启动项目")
            btn2.click(fn=start_project, inputs=txt2, outputs=txt3)
            btn3 = gr.Button("停止项目")
            btn3.click(fn=stop_project, inputs=None, outputs=txt3)
        
        pass
    with gr.Tab("设置"):
        llm_selecter = gr.Dropdown(llm_list, label="选择llm模型")
        tts_selecter = gr.Dropdown(tts_list, label="选择tts模型")
        ttl_selecter = gr.Dropdown(ttl_list, label="选择ttl模型")
        ttm_selecter = gr.Dropdown(ttm_list, label="选择ttm模型")
        button = gr.Button("保存")
        launch_json = 'G:\\digital-wife\\launcher\\config\\launch.json'
        button.click(fn=write_model_to_json, inputs=[llm_selecter, tts_selecter, ttl_selecter, ttm_selecter], outputs=None)
        live = True
    with gr.Tab("下载"):
        with gr.Column():
            txt16 = gr.Markdown("## 下载体验模式包")
            with gr.Row():
                txt17 = gr.Dropdown(["体验模式"],label="")
                txt20 = gr.Textbox(label="")
                btn8 = gr.Button("下载",)
                btn8.click(fn=openi_download, inputs=txt17, outputs=txt20)
            with gr.Accordion("高级下载（下载了体验模式的就不用下载以下包）"):
                txt6 = gr.Markdown("## 下载llm模型")
                with gr.Row():
                    txt4 = gr.Dropdown(llm_list,label="")
                    txt5 = gr.Textbox(label="")
                    btn4 = gr.Button("下载",)
                    btn4.click(fn=openi_download, inputs=txt4, outputs=txt5)
                txt7 = gr.Markdown("## 下载tts模型")
                with gr.Row():
                    txt8 = gr.Dropdown(tts_list,label="")
                    txt9 = gr.Textbox(label="")
                    btn5 = gr.Button("下载",)
                    btn5.click(fn=openi_download, inputs=txt8, outputs=txt9)
                txt10 = gr.Markdown("## 下载ttl模型")
                with gr.Row():
                    txt11 = gr.Dropdown(ttl_list,label="")
                    txt12 = gr.Textbox(label="")
                    btn6 = gr.Button("下载",)
                    btn6.click(fn=openi_download, inputs=txt11, outputs=txt12)
                txt13 = gr.Markdown("## 下载ttm模型")
                with gr.Row():
                    txt14 = gr.Dropdown(ttm_list,label="")
                    txt15 = gr.Textbox(label="")
                    btn7 = gr.Button("下载",) 
                    btn7.click(fn=openi_download, inputs=txt14, outputs=txt15)
                txt13 = gr.Markdown("## 下载Unity主程序")
                with gr.Row():
                    txt18 = gr.Dropdown(["Unity"],label="")
                    txt19 = gr.Textbox(label="")
                    btn9 = gr.Button("下载",) 
                    btn9.click(fn=openi_download, inputs=txt18, outputs=txt19)
    with gr.Tab("关于"):
        txt21 = gr.Markdown("## 关于")
        txt22 = gr.Markdown("## 更新日志")
        txt23 = gr.Markdown("## 联系我们")
        txt24 = gr.Markdown("## 特别鸣谢")
        txt25 = gr.Markdown("## 赞助我们")
demo.launch()
