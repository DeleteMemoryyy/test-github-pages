#!/usr/bin/env python3
import re
import sys
import html

# 简单的 Markdown 转换器，专为大文件优化
# 使用流式处理，避免全量加载内存
# 支持：标题、代码块、列表、链接、加粗、斜体

def convert_line(line, state):
    # 处理代码块状态
    if line.strip().startswith('```'):
        if state['in_code_block']:
            state['in_code_block'] = False
            return '</pre>\n'
        else:
            state['in_code_block'] = True
            return '<pre>\n'
    
    if state['in_code_block']:
        return html.escape(line)

    # 处理空行（段落分隔）
    if not line.strip():
        return '<br>\n'

    # 处理标题
    match = re.match(r'^(#{1,6})\s+(.+)$', line)
    if match:
        level = len(match.group(1))
        content = html.escape(match.group(2))
        return f'<h{level}>{content}</h{level}>\n'

    # 处理列表
    match = re.match(r'^[-*]\s+(.+)$', line)
    if match:
        content = html.escape(match.group(1))
        return f'<ul><li>{content}</li></ul>\n'  # 简单处理，每个列表项都包一个 ul

    # 处理行内元素
    line = html.escape(line)
    
    # 链接
    line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
    
    # 加粗
    line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
    
    # 斜体
    line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)

    return line + '<br>\n'

def main():
    input_file = 'all_docs.md'
    output_file = 'all_docs.html'
    
    print(f"Starting conversion of {input_file} to {output_file}...")
    
    # 写入 HTML 头部
    header = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Docs</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 { margin-top: 1.5em; color: #222; }
        pre {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        code {
            background-color: #e8e8e8;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
        }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { margin: 0; padding-left: 20px; }
        li { margin-bottom: 5px; }
        blockquote {
            border-left: 4px solid #ddd;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }
        .loading {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #fff;
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
<div id="content">
'''
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(header)
        
        state = {'in_code_block': False}
        line_count = 0
        
        with open(input_file, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                html_line = convert_line(line, state)
                f_out.write(html_line)
                
                line_count += 1
                if line_count % 10000 == 0:
                    print(f"Processed {line_count} lines...", flush=True)
        
        # 写入 HTML 尾部
        footer = '''
</div>
<script>
    // Simple script to enhance the view if needed
</script>
</body>
</html>'''
        f_out.write(footer)
    
    print("Conversion completed successfully!")

if __name__ == '__main__':
    main()
