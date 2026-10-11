with open(r'C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('<script>')
print('Script starts at char:', s)
print('Script length:', len(text) - s)
