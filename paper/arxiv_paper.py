import arxiv
import requests

cat_list = [
    "cs.AI",
    "cs.CE",
    "cs.CY",
    "cs.DM",
    "cs.DS",
    "cs.GT",
    "cs.IR",
    "cs.IT",
    "cs.LG",
    "cs.NE",
    "cs.SI",
    "cs.SY"
]

tag_list = [
    "ctr prediction",
    "cvr prediction",
    "budget pacing",
    "budget control",
    "bidding strategy",
    "bid landscape",
    "frequency capping",
    "retargting",
    "fraud detection",
    "DMP",
    "conversion attribution",
    "uncertainty calibration",
    "GNN",
    "generative retrieval",
    "generative model",
    "AIGC",
]

prompt1 = "请把这段英文翻译成中文：%s"

prompt2 = f"""你是一个文本打标专家，即给定一段文本，可以根据内容，打上相关性较高的标签。其中输出结果需要满足以下条件：
（1）标签范围为${"，".join(tag_list)}
（2）输出格式为python的list格式，其中list的每个元素是上述标签，比如["bidding strategy"]，或者["budget pacing", "cvr prediction"]
（3）输出个数可以是1个或者多个，如果没有相关的标签，可以输出0个，即[]
下面这段英文摘自arxiv相关论文的总结，请对其进行打标：%s
"""


def get_arxiv(start_date, end_date):
    client = arxiv.Client()
    query = " OR ".join([f"cat:{cat}" for cat in cat_list])
    query = f"({query}) AND submittedDate:[{start_date}0000 TO {end_date}2359] AND abs:advertising"
    search = arxiv.Search(
        query=query,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    results = client.results(search)
    return (
        {
            "entry_id": result.entry_id,
            "title": result.title,
            "summary": result.summary.replace("\n", "")
        }
        for result in results
    )


def get_response(url, api_key, prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "SOFA-TraceId": "0b46977c17296519321548915ef847",
        "SOFA-RpcId": "0.1",
    }
    data = {
        "model": "DeepSeek-V3",
        "messages": [
          {
            "role": "user",
            "content": f"{prompt}"
          }
        ]
      }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    result = result.get("choices", [{}])
    result = result if len(result) > 0 else [{}]
    result = result[0]
    result = result.get("message", {}).get("content", None)
    return result


def get_total(url, api_key, start_date, end_date):
    results = get_arxiv(start_date, end_date)
    for result in results:
        summary_cn = get_response(url, api_key, prompt1 % result["summary"])
        summary_cn = summary_cn.replace("\n", "") if summary_cn is not None else summary_cn
        tags = get_response(url, api_key, prompt2 % result["summary"])
        yield {
            "entry_id": result["entry_id"],
            "title": result["title"],
            "summary": result["summary"],
            "summary_cn": summary_cn,
            "tags": tags,
        }
