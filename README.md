# I Love Study

> 免责说明：本库仅做交流学习使用

## Intro

可以获取拉勾教育和极客时间的课程（需本身有权限），并制作为 pdf / epub。（层级目录为章节-文章-文章中的 headings）

## Preview

<img width="1436" alt="image" src="https://user-images.githubusercontent.com/8280645/166144758-5e4995cd-6440-4cfe-bd26-736d6c32a70a.png">
<img width="1136" alt="image" src="https://user-images.githubusercontent.com/8280645/166144793-18a3fedb-dac1-411e-b350-c1d19f9816c4.png">
<img width="1136" alt="image" src="https://user-images.githubusercontent.com/8280645/166144805-7f4ccb62-187c-43f4-92f8-89d28653944c.png">

## Install

使用 poetry 安装依赖：

```shell
poetry install
```

### 前置依赖

要生成 `epub` 或者 `pdf`，需要安装 `pandoc`：<https://pandoc.org/installing.html>

如果要运行生成 pdf，需要提前安装 `wkhtmltopdf`，Mac：

```shell
brew install --cask wkhtmltopdf
```

其他平台安装方式见官网：<https://wkhtmltopdf.org/>。

## Usage

> 实在是懒的搞的太像 command tools，都说了是交流学习用了。
>
> 只提供工具，课自己买。
>
> course id 拿起来很方便，暂时懒得写进脚本。

clone 项目，修改项目后 `python main.py`

### 拉勾教育

拉勾教育支持专栏课和八点一课中的文本内容，不支持音频和视频内容。

```python
"""
字段来源
course_id: 课程介绍 url 中的 courseId，本质上是 sku，在列表接口能拿到全部 course_id
token: cookie 中的 edu_gate_login_token
base_dir: 爬取数据存放的目录
epub: 转换时是否转换为 epub
pdf: 转换时是否转换为 pdf
worker: 转换时的线程数
force: 转换时默认会检测是否已存在 md / epub / pdf 并跳过，True 启用强制重新生成
"""
lago = Lago(
    courses=[685],  # course_id list
    token=token,  # 也可以设置环境变量 LAGO_TOKEN
    base_dir='./lagou_courses',
    epub=True,
    pdf=True,
    worker=5,
    force=False
)

# 单线程爬取（为了避免被封慢慢爬）
lago.run()

# 转换成 pdf / epub
lago.trans()
```

### 极客时间

极客时间支持专栏内容，支持专栏内容中的文本和音频，不支持视频课。

> 如果发现频繁 451 retry，说明被风控抓住了，换个 ip 或者换个 token，调高 sleep 时间。
>
> 因为懒这部分 451 是无限重试的（

```python
"""
字段来源
course_id: 课程介绍 url 中的 courseId，在某个接口能拿到全部 course_id
token: cookie 中的 edu_gate_login_token
base_dir: 爬取数据存放的目录
epub: 转换时是否转换为 epub
pdf: 转换时是否转换为 pdf
audio: 是否爬取音频（默认关闭，属实有点大还慢）
worker: 转换时的线程数
force: 转换时默认会检测是否已存在 md / epub / pdf 并跳过，True 启用强制重新生成
"""
geekT = GeekT(
    courses=[685],  # course_id list
    token=token,  # 也可以设置环境变量 GEEKT_TOKEN
    gcid=gcid,  # GEEKT_GCID
    base_dir='./geek_courses',
    epub=True,
    pdf=True,
    audio=False,
    worker=5,
    force=False
)

# 单线程爬取（为了避免被封慢慢爬，风控比较敏感，爬起来比隔壁拉勾更慢）
geekT.run()

# 转换成 pdf / epub
geekT.trans()
```
