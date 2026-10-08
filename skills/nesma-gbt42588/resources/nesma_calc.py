#!/usr/bin/env python3
"""Deterministic arithmetic for the supplied GB/T 42588-2023 source.

This program does not identify user functions, deduplicate semantics, validate
DET/RET/FTR evidence, or certify compliance. See calculator-guide.md.
Python 3.8+; standard library only; no network or external commands.
"""
import argparse
import json
import os
from pathlib import Path
import sys

VERSION = "1.0.1"
WEIGHTS = {
    "ILF": {"low": 7, "medium": 10, "high": 15},
    "ELF": {"low": 5, "medium": 7, "high": 10},
    "EI": {"low": 3, "medium": 4, "high": 6},
    "EO": {"low": 4, "medium": 5, "high": 7},
    "EQ": {"low": 3, "medium": 4, "high": 6},
}
MATRIX = (("low", "low", "medium"),
          ("low", "medium", "high"),
          ("medium", "high", "high"))
AXES = {"ILF": ("ret", (1, 5), (19, 50)),
        "ELF": ("ret", (1, 5), (19, 50)),
        "EI": ("ftr", (1, 2), (4, 15)),
        "EO": ("ftr", (1, 3), (5, 19)),
        "EQ": ("ftr", (1, 3), (5, 19))}
SOURCES = {
    "indicative": "5.2.1.1, equations (1)(2); printed p10 / PDF p14",
    "complexity": "7.3-11.3; Annex B.1-B.6; printed pp51-54 / PDF pp55-58",
    "aggregate": "4.9, 5.2.2-5.2.3, Annex B.6",
    "enhancement": "5.5.3 equation (3), 5.6.4 equation (4) and step 5",
    "development": "5.6.3 steps 1-4; printed p15 / PDF p19",
}


class InputError(ValueError):
    def __init__(self, code, message, path="$", **details):
        super().__init__(message)
        self.result = {"status": "error", "error": {"code": code,
                       "path": path, "message": message, **details}}


def fail(code, message, path="$", **details):
    raise InputError(code, message, path, **details)


def shape(value, allowed, required=(), path="$"):
    if not isinstance(value, dict):
        fail("object_required", "Expected a JSON object.", path)
    extra = sorted(set(value) - set(allowed))
    if extra:
        fail("unknown_fields", "Unknown fields are not ignored.", path, fields=extra)
    absent = sorted(set(required) - set(value))
    if absent:
        fail("required_fields", "Required structural fields are absent.", path, fields=absent)


def integer(value, path, minimum=0, nullable=False):
    if nullable and value is None:
        return None
    if type(value) is not int or value < minimum:
        fail("invalid_integer", "Expected an integer >= %d; booleans, floats and strings are rejected." % minimum, path)
    return value


def choice(value, options, path):
    if not isinstance(value, str) or value not in options:
        fail("invalid_choice", "Expected one of the listed values.", path, choices=list(options))
    return value


def flag(data, name, default=False, path="$"):
    value = data.get(name, default)
    if type(value) is not bool:
        fail("invalid_boolean", "Expected a JSON boolean.", path + "." + name)
    return value


def text_field(value, path):
    if not isinstance(value, str) or not value.strip():
        fail("invalid_text", "Expected nonempty text.", path)
    return value


def column(value, edges):
    return 0 if value <= edges[0] else 1 if value <= edges[1] else 2


def weight_result(kind, complexity, basis, defaulted=False, **extra):
    return {"status": "calculated_with_defaults" if defaulted else "calculated",
            "type": kind, "complexity": complexity,
            "unit_fp": WEIGHTS[kind][complexity], "basis": basis,
            "defaulted": defaulted, **extra}


def function_value(item, method, allow_defaults, path):
    kind = choice(item.get("type"), WEIGHTS, path + ".type")
    special = choice(item.get("special", "normal"),
                     ("normal", "help", "fpa_standard_transaction"), path + ".special")
    axis_name, row_edges, det_edges = AXES[kind]
    other_axis = "ftr" if axis_name == "ret" else "ret"
    if other_axis in item:
        fail("wrong_axis", "This function category does not use this axis.", path + "." + other_axis)
    det = integer(item.get("det"), path + ".det", 1, nullable=True)
    axis = integer(item.get(axis_name), path + "." + axis_name,
                   1 if axis_name == "ret" else 0, nullable=True)
    explicit = item.get("complexity")
    if explicit is not None:
        choice(explicit, ("low", "medium", "high"), path + ".complexity")
        if method != "detailed":
            fail("conflicting_inputs", "Estimated analysis sets category weights; omit explicit complexity.", path)
        if any(key in item for key in ("det", "ret", "ftr")):
            fail("conflicting_inputs", "Supply explicit complexity OR element counts, not both.", path)
        if special == "help":
            fail("conflicting_inputs", "Help uses the special complexity rule; omit explicit complexity.", path)
    if special == "help" and kind != "EQ":
        fail("invalid_special_type", "The help rule requires EQ.", path)
    if special == "fpa_standard_transaction" and kind not in ("EI", "EO", "EQ"):
        fail("invalid_special_type", "FPA standard transactions must be EI, EO or EQ.", path)
    # The unknown special axis cannot be resolved by ordinary defaults or an
    # asserted complexity. Estimated counting uses the explicit estimated method.
    if special == "fpa_standard_transaction" and method == "detailed":
        return {"status": "needs_review", "type": kind, "review_ids": ["NR04"],
                "reason": "The 6.20 special referenced-record-type axis is unresolved; ordinary FTR is not substituted."}
    if special == "help":
        return weight_result(kind, "low" if method == "detailed" else "medium",
                             "6.13 help rule", source="6.13; printed pp24-25 / PDF pp28-29")
    if method == "estimated":
        return weight_result(kind, "low" if kind in ("ILF", "ELF") else "medium",
                             "5.2.2 estimated-analysis category weight")
    if explicit is not None:
        return weight_result(kind, explicit, "caller-supplied complexity; supporting evidence not verified")
    missing = [key for key, value in (("det", det), (axis_name, axis)) if value is None]
    if missing:
        if not allow_defaults:
            return {"status": "needs_input", "type": kind, "missing": missing,
                    "reason": "Element counts are missing; defaults require allow_defaults:true."}
        return weight_result(kind, "low" if kind in ("ILF", "ELF") else "medium",
                             "Annex B default for unknown element counts", True, missing=missing)
    row = column(axis, row_edges)
    col = column(det, det_edges)
    return weight_result(kind, MATRIX[row][col], "Annex B matrix",
                         elements={"det": det, axis_name: axis},
                         matrix_cell={"row": row + 1, "column": col + 1})


def indicative(data):
    model = choice(data.get("model"), ("conceptual", "normalized"), "$.model")
    names = ("ilf", "elf") if model == "conceptual" else ("netm", "nete")
    shape(data, ("operation", "model", *names), ("operation", "model"))
    values = {name: integer(data.get(name), "$." + name, nullable=True) for name in names}
    missing = [name for name in names if values[name] is None]
    if missing:
        return {"status": "needs_input", "model": model, "missing": missing}
    a, b = (35, 15) if model == "conceptual" else (25, 10)
    return {"status": "calculated", "model": model, "counts": values,
            "formula": "%d*%s + %d*%s" % (a, names[0], b, names[1]),
            "total_fp": a * values[names[0]] + b * values[names[1]]}


def complexity(data):
    shape(data, ("operation", "method", "type", "det", "ret", "ftr", "allow_defaults", "special"),
          ("operation", "method", "type"))
    method = choice(data["method"], ("detailed", "estimated"), "$.method")
    defaults = flag(data, "allow_defaults")
    return {"method": method, **function_value(data, method, defaults, "$")}


def aggregate(data):
    shape(data, ("operation", "method", "allow_defaults", "items"), ("operation", "method", "items"))
    method = choice(data["method"], ("detailed", "estimated"), "$.method")
    defaults = flag(data, "allow_defaults")
    if not isinstance(data["items"], list):
        fail("array_required", "items must be an array.", "$.items")
    seen, rows, unresolved = set(), [], []
    known = 0
    any_defaults = False
    for index, item in enumerate(data["items"]):
        path = "$.items[%d]" % index
        shape(item, ("id", "type", "count", "complexity", "det", "ret", "ftr", "special", "state", "reason"),
              ("id", "type", "count"), path)
        identity = text_field(item["id"], path + ".id")
        if identity in seen:
            fail("duplicate_id", "IDs must be unique; semantic deduplication remains the caller's responsibility.", path + ".id", id=identity)
        seen.add(identity)
        count = integer(item["count"], path + ".count")
        state = choice(item.get("state", "ready"), ("ready", "needs_input", "needs_review"), path + ".state")
        if "reason" in item:
            text_field(item["reason"], path + ".reason")
        if state == "ready":
            value = function_value(item, method, defaults, path)
        else:
            text_field(item.get("reason"), path + ".reason")
            if item["type"] is not None:
                # Validate all supplied counting fields even on unresolved rows.
                function_value(item, method, defaults, path)
            elif any(key in item for key in ("complexity", "det", "ret", "ftr", "special")):
                fail("unknown_category", "Element/complexity fields require a known category.", path)
            value = {"status": state, "type": item["type"], "reason": item["reason"]}
        row = {"id": identity, "count": count, **value}
        if "unit_fp" in value:
            row["fp"] = count * value["unit_fp"]
            known += row["fp"]
            any_defaults = any_defaults or value["defaulted"]
        else:
            unresolved.append(identity)
        rows.append(row)
    result = {"method": method, "known_subtotal_fp": known,
              "items": rows, "unresolved_ids": unresolved,
              "semantic_deduplication_verified": False}
    if unresolved:
        calculated = any("fp" in row for row in rows)
        result["status"] = "partial" if calculated else "needs_review" if any(
            row["status"] == "needs_review" for row in rows) else "needs_input"
    else:
        result.update(status="calculated_with_defaults" if any_defaults else "calculated", total_fp=known)
    return result


def enhancement(data):
    shape(data, ("operation", "add", "deleted", "changed_after", "conversion", "baseline", "changed_before"), ("operation",))
    values = {name: integer(data.get(name), "$." + name, nullable=True)
              for name in ("add", "deleted", "changed_after", "conversion", "baseline", "changed_before")}
    core_names = ("add", "deleted", "changed_after")
    project_missing = [name for name in (*core_names, "conversion") if values[name] is None]
    app_missing = [name for name in (*core_names, "baseline", "changed_before") if values[name] is None]
    result = {"inputs": values, "project_missing": project_missing, "application_missing": app_missing}
    if all(values[name] is not None for name in core_names):
        core = sum(values[name] for name in core_names)
        result["project_core_fp"] = core
        if values["conversion"] is not None:
            result["project_fp"] = core + values["conversion"]
    if not app_missing:
        app = values["baseline"] + values["add"] - values["deleted"] + values["changed_after"] - values["changed_before"]
        if app < 0:
            fail("negative_application", "Inputs produce a negative application size; review the baseline and change partition.")
        result["application_fp"] = app
        result["net_application_change_fp"] = app - values["baseline"]
    if values["baseline"] is not None:
        known_removed = sum(values[name] for name in ("deleted", "changed_before")
                            if values[name] is not None)
        if known_removed > values["baseline"]:
            fail("invalid_baseline_partition", "Known deleted and changed-before functions exceed the baseline; added functions cannot repair that partition.")
    complete = not project_missing and not app_missing
    any_result = any(key in result for key in ("project_core_fp", "project_fp", "application_fp"))
    result["status"] = "calculated" if complete else "partial" if any_result else "needs_input"
    return result


def development(data):
    names = ("new_application", "conversion", "other_application_changes")
    shape(data, ("operation", *names), ("operation",))
    values = {name: integer(data.get(name), "$." + name, nullable=True) for name in names}
    missing = [name for name in names if values[name] is None]
    result = {"inputs": values, "missing": missing}
    if values["new_application"] is not None:
        result["application_fp"] = values["new_application"]
    if missing:
        result["status"] = "partial" if "application_fp" in result else "needs_input"
    else:
        result.update(status="calculated", project_fp=sum(values.values()))
    return result


OPERATIONS = {"indicative": indicative, "complexity": complexity,
              "aggregate": aggregate, "enhancement": enhancement, "development": development}


def calculate(data):
    if not isinstance(data, dict):
        fail("object_required", "The input document must be a JSON object.")
    operation = choice(data.get("operation"), OPERATIONS, "$.operation")
    return {"calculator_version": VERSION, "operation": operation, "unit": "FP",
            "source": SOURCES[operation],
            "scope": "Arithmetic on supplied facts only; function identification and source compliance are not verified.",
            **OPERATIONS[operation](data)}


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail("duplicate_json_key", "Duplicate JSON keys are rejected.", key=key)
        result[key] = value
    return result


def nonfinite(value):
    fail("nonfinite_number", "JSON NaN and Infinity are rejected.", value=value)


def same_path(a, b):
    if a.resolve() == b.resolve():
        return True
    return a.exists() and b.exists() and os.path.samefile(a, b)


class JsonParser(argparse.ArgumentParser):
    def error(self, message):
        fail("cli_arguments", message)


def main(argv=None):
    try:
        parser = JsonParser(description=__doc__)
        parser.add_argument("input", help="UTF-8 JSON input file")
        parser.add_argument("--output", help="Optional UTF-8 JSON result file; stdout always receives the result")
        args = parser.parse_args(argv)
        input_path = Path(args.input)
        output_path = Path(args.output) if args.output else None
        if output_path and (same_path(input_path, output_path) or same_path(Path(__file__), output_path)):
            fail("unsafe_output_path", "Output must not overwrite the input file or calculator program.")
        data = json.loads(input_path.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=strict_object, parse_constant=nonfinite)
        result = calculate(data)
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if output_path:
            output_path.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0
    except InputError as exc:
        result = exc.result
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        result = {"status": "error", "error": {"code": "file_or_json_error", "message": str(exc)}}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
