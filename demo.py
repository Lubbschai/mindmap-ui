#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示版AI思维导图生成器 - 不需要API密钥，用于测试界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import threading
import time

class MindmapGeneratorDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("AI思维导图生成器 (演示版)")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 创建GUI界面
        self.create_widgets()
        
        # 生成的思维导图内容
        self.mindmap_content = ""
    
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
        self.status_var.set("就绪 (演示模式 - 无需API密钥)")
        status_label = tk.Label(main_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
        status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 绑定回车键
        self.topic_entry.bind('<Return>', lambda event: self.generate_mindmap())
    
    def generate_mindmap(self):
        """生成思维导图（演示版）"""
        topic = self.topic_var.get().strip()
        if not topic:
            messagebox.showwarning("警告", "请输入一个主题")
            return
        
        # 禁用生成按钮，防止重复点击
        self.generate_btn.config(state='disabled')
        self.status_var.set("正在生成思维导图，请稍候...")
        
        # 在新线程中生成，避免界面卡死
        thread = threading.Thread(target=self._generate_mindmap_thread, args=(topic,))
        thread.daemon = True
        thread.start()
    
    def _generate_mindmap_thread(self, topic):
        """在新线程中生成思维导图（演示版）"""
        try:
            # 模拟API调用延迟
            time.sleep(2)
            
            # 生成演示用的思维导图内容
            mindmap_content = f"""mindmap
  root){topic}(
    核心概念
      基础理论
      关键要素
      重要特征
    应用领域
      实际场景
      使用案例
      效果评估
    发展趋势
      技术创新
      市场需求
      未来展望
    相关技术
      辅助工具
      集成方案
      优化策略"""
            
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
        self.status_var.set("思维导图生成完成 (演示模式)")
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
    app = MindmapGeneratorDemo(root)
    
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