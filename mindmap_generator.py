#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI思维导图生成器
使用OpenAI API生成Mermaid格式的思维导图，并提供Tkinter图形界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import threading
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

class MindmapGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI思维导图生成器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置OpenAI API密钥
        self.setup_openai()
        
        # 创建GUI界面
        self.create_widgets()
        
        # 生成的思维导图内容
        self.mindmap_content = ""
    
    def setup_openai(self):
        """设置OpenAI API"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            # 如果没有环境变量，提示用户输入
            self.show_api_key_dialog()
        else:
            self.client = OpenAI(api_key=api_key)
    
    def show_api_key_dialog(self):
        """显示API密钥输入对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("设置OpenAI API密钥")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="请输入您的OpenAI API密钥:", font=("Arial", 12)).pack(pady=10)
        
        api_key_var = tk.StringVar()
        entry = tk.Entry(dialog, textvariable=api_key_var, width=50, show="*")
        entry.pack(pady=5)
        entry.focus()
        
        def save_api_key():
            key = api_key_var.get().strip()
            if key:
                self.client = OpenAI(api_key=key)
                # 可以选择保存到.env文件
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f'OPENAI_API_KEY={key}\n')
                dialog.destroy()
            else:
                messagebox.showerror("错误", "请输入有效的API密钥")
        
        tk.Button(dialog, text="保存", command=save_api_key, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)
    
    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置行列权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = tk.Label(main_frame, text="AI思维导图生成器", 
                              font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 主题输入
        tk.Label(main_frame, text="输入主题:", font=("Arial", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        self.topic_var = tk.StringVar()
        self.topic_entry = tk.Entry(main_frame, textvariable=self.topic_var, 
                                   font=("Arial", 12), width=40)
        self.topic_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 生成按钮
        self.generate_btn = tk.Button(main_frame, text="生成思维导图", 
                                     command=self.generate_mindmap,
                                     bg="#2196F3", fg="white", 
                                     font=("Arial", 12, "bold"),
                                     cursor="hand2")
        self.generate_btn.grid(row=1, column=2, pady=5, padx=(10, 0))
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="生成的思维导图 (Mermaid格式)", padding="10")
        result_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 文本显示区域
        self.result_text = scrolledtext.ScrolledText(result_frame, 
                                                    width=80, height=20,
                                                    font=("Consolas", 10),
                                                    wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # 保存按钮
        self.save_btn = tk.Button(btn_frame, text="保存为.mmd文件", 
                                 command=self.save_file,
                                 bg="#4CAF50", fg="white", 
                                 font=("Arial", 10),
                                 cursor="hand2")
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清空按钮
        self.clear_btn = tk.Button(btn_frame, text="清空内容", 
                                  command=self.clear_content,
                                  bg="#FF9800", fg="white", 
                                  font=("Arial", 10),
                                  cursor="hand2")
        self.clear_btn.pack(side=tk.LEFT)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_label = tk.Label(main_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
        status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 绑定回车键
        self.topic_entry.bind('<Return>', lambda event: self.generate_mindmap())
    
    def generate_mindmap(self):
        """生成思维导图"""
        topic = self.topic_var.get().strip()
        if not topic:
            messagebox.showwarning("警告", "请输入一个主题")
            return
        
        # 检查API密钥
        if not hasattr(self, 'client') or not self.client:
            messagebox.showerror("错误", "请先设置OpenAI API密钥")
            self.show_api_key_dialog()
            return
        
        # 禁用生成按钮，防止重复点击
        self.generate_btn.config(state='disabled')
        self.status_var.set("正在生成思维导图，请稍候...")
        
        # 在新线程中生成，避免界面卡死
        thread = threading.Thread(target=self._generate_mindmap_thread, args=(topic,))
        thread.daemon = True
        thread.start()
    
    def _generate_mindmap_thread(self, topic):
        """在新线程中生成思维导图"""
        try:
            # 构建提示词
            prompt = f"""
请为主题"{topic}"生成一个详细的思维导图，使用Mermaid语法格式。

要求：
1. 使用mindmap格式
2. 包含至少3-4个主要分支
3. 每个分支下至少包含2-3个子主题
4. 结构清晰，逻辑合理
5. 只返回Mermaid代码，不要其他解释文字

示例格式：
mindmap
  root)主题(
    分支1
      子主题1
      子主题2
    分支2
      子主题1
      子主题2
    分支3
      子主题1
      子主题2
"""
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的思维导图生成助手，擅长用Mermaid语法创建结构化的思维导图。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            mindmap_content = response.choices[0].message.content.strip()
            
            # 更新UI（在主线程中）
            self.root.after(0, self._update_result, mindmap_content)
            
        except Exception as e:
            error_msg = f"生成失败: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
    
    def _update_result(self, content):
        """更新结果显示"""
        self.mindmap_content = content
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, content)
        self.status_var.set("思维导图生成完成")
        self.generate_btn.config(state='normal')
    
    def _show_error(self, error_msg):
        """显示错误信息"""
        self.status_var.set("生成失败")
        self.generate_btn.config(state='normal')
        messagebox.showerror("错误", error_msg)
    
    def save_file(self):
        """保存文件"""
        if not self.mindmap_content:
            messagebox.showwarning("警告", "没有内容可以保存")
            return
        
        # 获取主题作为默认文件名
        topic = self.topic_var.get().strip()
        default_name = f"{topic}_mindmap.mmd" if topic else "mindmap.mmd"
        
        # 选择保存位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mmd",
            filetypes=[("Mermaid files", "*.mmd"), ("All files", "*.*")],
            initialvalue=default_name
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.mindmap_content)
                self.status_var.set(f"文件已保存: {file_path}")
                messagebox.showinfo("成功", f"文件已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def clear_content(self):
        """清空内容"""
        self.result_text.delete(1.0, tk.END)
        self.mindmap_content = ""
        self.topic_var.set("")
        self.status_var.set("内容已清空")

def main():
    """主函数"""
    root = tk.Tk()
    app = MindmapGenerator(root)
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()