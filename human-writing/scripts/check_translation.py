"""只读的译文保真检查。机械约束通过不等于语义等价；任何改动均待人工复核。"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from pathlib import Path


MARKER = re.compile(r"^【([A-Za-z0-9_-]+)】", re.MULTILINE)
NOTES = re.compile(r"\[\d+\]")
NUMBERS = re.compile(r"\d+(?:[.,]\d+)*(?:%|％)?")
IMAGES = re.compile(r"!\[[^\n]*?\]\([^\n]*?\)")
QUOTE_PAIRS = {"“": "”", "‘": "’", "「": "」", "『": "』", '"': '"'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def string(value):
    return isinstance(value, str) and bool(value.strip())


def keys(value, required, optional=()):
    require(isinstance(value, dict), "manifest 中的对象必须是 JSON object")
    require(set(required) <= value.keys(), f"缺少字段 {sorted(set(required) - value.keys())}")
    require(not value.keys() - set(required) - set(optional), "manifest 含未知字段")


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON 字段重复 {key}")
        result[key] = value
    return result


def parse_units(text):
    matches = list(MARKER.finditer(text))
    require(matches and matches[0].start() == 0,
            "译文必须从行首【段号】开始，前言也必须有独立段号")
    result = {}
    for index, match in enumerate(matches):
        identity = match[1]
        require(identity not in result, f"重复段号 {identity}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[identity] = text[match.end():end]
        require(result[identity].strip(), f"空译文段 {identity}")
    return result


def quotations(text):
    """取完整的最外层引语，保留嵌套和跨行内容；英文撇号不作为引号。"""
    stack = []
    result = []
    start = 0
    for index, char in enumerate(text):
        if (char == "’" and 0 < index < len(text) - 1
                and re.fullmatch(r"[A-Za-z0-9]", text[index - 1])
                and re.fullmatch(r"[A-Za-z0-9]", text[index + 1])):
            continue  # 英文所有格或缩写中的弯撇号，不是闭引号。
        if stack and char == stack[-1]:
            stack.pop()
            if not stack:
                result.append(text[start:index + 1])
        elif char in QUOTE_PAIRS:
            if not stack:
                start = index
            stack.append(QUOTE_PAIRS[char])
        elif char in QUOTE_PAIRS.values():
            raise ValueError("存在未配对的闭引号；请先人工核对并整理输入")
    require(not stack, "存在未闭合的引号；请先人工核对并整理输入")
    # Markdown 块引文也按原有行锁定。非标准格式需在 protected 或 locked 中明确指定。
    result.extend(re.findall(r"^\s*>[^\n]*(?:\n|$)", text, re.MULTILINE))
    return result


def source_has(source, alias):
    # 不让 panel game 意外匹配 panel gamesmanship；允许逗号等词界和大小写变化。
    left = r"(?<![A-Za-z0-9_])" if alias[0].isascii() and alias[0].isalnum() else ""
    right = r"(?![A-Za-z0-9_])" if alias[-1].isascii() and alias[-1].isalnum() else ""
    return bool(re.search(left + re.escape(alias) + right, source, re.IGNORECASE))


def validate_manifest(data, baseline_bytes, before):
    keys(data, ("version", "baseline_sha256", "units", "glossary"))
    require(type(data["version"]) is int and data["version"] == 1, "不支持的 manifest version")
    require(data["baseline_sha256"] == hashlib.sha256(baseline_bytes).hexdigest(),
            "baseline_sha256 不符，禁止使用错版或已被改写的基线")
    require(isinstance(data["units"], list) and data["units"], "units 必须是非空数组")
    ids = []
    for unit in data["units"]:
        keys(unit, ("id", "source"), ("protected", "locked"))
        require(string(unit["id"]) and string(unit["source"]), "段号和原文必须是非空字符串")
        require(type(unit.get("locked", False)) is bool, "locked 必须是布尔值")
        protected = unit.get("protected", [])
        require(isinstance(protected, list) and all(string(x) for x in protected),
                "protected 必须是非空字符串的数组")
        ids.append(unit["id"])
    require(ids == list(before), "manifest 原文段号必须与基线逐项同序且唯一")
    require(isinstance(data["glossary"], list), "glossary 必须是数组，可显式使用空数组")
    aliases = set()
    for term in data["glossary"]:
        keys(term, ("source", "target"), ("forbidden",))
        require(isinstance(term["source"], list) and term["source"]
                and all(string(x) for x in term["source"]) and string(term["target"]),
                "每条术语需要非空 source 别名数组及 target 字符串")
        forbidden = term.get("forbidden", [])
        require(isinstance(forbidden, list) and all(string(x) for x in forbidden),
                "forbidden 必须是字符串数组")
        require(not any(x in term["target"] for x in forbidden), "禁译词与核准译名冲突")
        for alias in term["source"]:
            folded = alias.casefold()
            require(folded not in aliases, f"术语别名重复或冲突 {alias}")
            aliases.add(folded)
    for unit in data["units"]:
        for value in unit.get("protected", []):
            require(value in before[unit["id"]], f"保护文本不在基线段 {unit['id']} 中")
        quotations(before[unit["id"]])  # 损坏的基线是输入错误，不能作为通过依据。


def check(candidate, baseline_bytes, data):
    before = parse_units(baseline_bytes.decode("utf-8"))
    after = parse_units(candidate)
    validate_manifest(data, baseline_bytes, before)
    issues = []
    changes = []

    def issue(code, identity, message):
        issues.append({"code": code, "id": identity, "message": message})

    if list(before) != list(after):
        issue("unit_order", None, f"段号新增、遗漏或重排，原顺序 {list(before)}，候选顺序 {list(after)}")
    for unit in data["units"]:
        identity = unit["id"]
        old, new = before[identity], after.get(identity, "")
        if old != new:
            changes.append({"id": identity, "source": unit["source"], "before": old,
                            "after": new, "diff": "".join(difflib.unified_diff(
                                old.splitlines(keepends=True), new.splitlines(keepends=True),
                                fromfile=f"baseline/{identity}", tofile=f"candidate/{identity}"))})
        if unit.get("locked", False) and old != new:
            issue("locked", identity, "整段保护内容被改动")
        try:
            if quotations(old) != quotations(new):
                issue("quotation", identity, "引语新增、删改或转述，需恢复原话与嵌套关系")
        except ValueError as error:
            issue("quotation", identity, str(error))
        for label, pattern in (("note", NOTES), ("number", NUMBERS), ("image", IMAGES)):
            if pattern.findall(old) != pattern.findall(new):
                issue(label, identity, "注号、阿拉伯数字或 Markdown 图片的内容/顺序发生变化")
        for value in unit.get("protected", []):
            if old.count(value) != new.count(value):
                issue("protected", identity, f"指定保护文本出现次数改变 {value!r}")
        for term in data["glossary"]:
            target = term["target"]
            if any(source_has(unit["source"], alias) for alias in term["source"]):
                if target not in new:
                    issue("term_missing", identity, f"原文术语应使用核准译名 {target!r}")
                if old.count(target) != new.count(target):
                    issue("term_count", identity, f"核准译名次数改变 {target!r}，需对照原文核查")
            for forbidden in term.get("forbidden", []):
                if forbidden in new:
                    issue("term_forbidden", identity, f"出现项目禁译词 {forbidden!r}")
    for identity in after:
        if identity in before:
            continue
        changes.append({"id": identity, "source": "无对应原文，新增段落未获授权", "before": "",
                        "after": after[identity], "diff": "".join(difflib.unified_diff(
                            [], after[identity].splitlines(keepends=True),
                            fromfile=f"baseline/{identity}", tofile=f"candidate/{identity}"))})
    return {"mode": "translation", "status": "blocked" if issues else (
                "review_required" if changes else "unchanged"),
            "issues": issues, "changes": changes,
            "notice": "未执行创作风格禁令；所有改动均需人工对照原文复核。未改动不等于翻译正确。"}


def run(path, baseline_path, manifest_path, as_json=False):
    try:
        require(path == "-" or Path(path).resolve() != Path(baseline_path).resolve(),
                "候选译文与基线必须是不同文件")
        baseline_bytes = Path(baseline_path).read_bytes()
        data = json.loads(Path(manifest_path).read_text(encoding="utf-8"),
                          object_pairs_hook=unique_json)
        candidate = sys.stdin.read() if path == "-" else Path(path).read_bytes().decode("utf-8")
        result = check(candidate, baseline_bytes, data)
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        result = {"mode": "translation", "status": "input_error", "error": str(error)}
        code = 2
    else:
        code = 0 if result["status"] == "unchanged" else 1
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"翻译保真检查 {result['status']}")
        if "error" in result:
            print(result["error"])
        else:
            print(result["notice"])
            for item in result["issues"]:
                print(f"- [{item['code']}] 段 {item['id']}: {item['message']}")
            for item in result["changes"]:
                print(f"\n待复核【{item['id']}】\n原文 {item['source']}\n{item['diff']}")
    return code
