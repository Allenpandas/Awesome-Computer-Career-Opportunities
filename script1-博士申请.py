import requests
from lxml import html
import time


# 发送HTTP请求获取网页内容
def get_webpage(url):
    response = requests.get(url)
    return response.text


# 使用lxml解析网页内容并提取信息
def parse_webpage(content):
    # 创建一个XPath解析对象
    parser = html.fromstring(content)
    li_elements = parser.xpath('//ul[@class="album__list js_album_list"]/li')
    # 遍历打印获取到的li元素内容
    job_str = ""
    i = 0
    for li_element in li_elements:
        # 第一个版本只控制取最新的一条数据
        if i < 1:
            # 使用XPath表达式提取li元素的属性值
            link = li_element.xpath('./@data-link')[0]
            title = li_element.xpath('./@data-title')[0]
            msgid = li_element.xpath('./@data-msgid')[0]
            # 调用函数，拼接数据
            job_str = handle_data(link, title, msgid)
        i = i+1
    return job_str


# 处理数据
def handle_data(link, title, msgid):
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 替换标题，添加转移符号
    title = title.replace("|", '\|')
    str = "| [" + title + "](" + link + ") |" + date + "|" + msgid + "|" + "AI求职"
    return str


# 遍历数据，查看是否存在，如果存在则追加写
def append_after_separator(job_str, file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        sign = '|-|-|-|-|'  # 标志
        separator_position = content.find(sign)
    # 位置分割
    content_before = content[:separator_position+len(sign)] + "\n"
    content_after = content[separator_position+len(sign):]
    # print("content:", content)
    # print("content_before:", content_before)
    # print("job_str:", job_str)
    # print("content_after:", content_after)
    # exit()
    with open(file_path, 'w') as file:
        file.write(content_before + job_str + content_after)


# 主函数
def main():
    # 微信公众号页面
    url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg4NDY1NDU1OA==&album_id=1979032745175515138&action=getalbum"
    webpage = get_webpage(url)
    # 解析数据
    content_str = parse_webpage(webpage)
    # print(content_str)
    # 追加写
    append_after_separator(content_str, './1-博士申请.md')


if __name__ == "__main__":
    main()
