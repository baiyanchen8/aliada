with open("新增資料夾\image.md", "w+",encoding='utf-8') as f:
    for i in range(1,20):
# 'w' mode: overwrites the file if it exists
        f.write(f"![](LINE_ALBUM_資安理論與實務筆記_251026_{i}.jpg)\n")
    