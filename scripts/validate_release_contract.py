#!/usr/bin/env python3
"""Validate a release-contract document against release/contract.schema.json.

Standard library only, by design. The release workflow runs on a GitHub-hosted
runner where installing `jsonschema` would mean a network fetch, and PR CI in
this repository is deliberately install-free and reproducible offline
(see AGENTS.md section 7). So this implements exactly the JSON Schema
2020-12 keyword subset that release/contract.schema.json actually uses:

    $ref (local pointers only), type, const, enum, required, properties,
    additionalProperties, items, minItems, maxItems, uniqueItems, contains,
    minProperties, maxProperties, pattern, minLength, maxLength, minimum,
    maximum, exclusiveMinimum, exclusiveMaximum, multipleOf,
    allOf, anyOf, oneOf, not, if/then/else

An unknown keyword is a hard error rather than a silent pass: this checker
exists because nothing validated the emitted contract, and a validator that
quietly ignores what it does not understand recreates that hole.

Usage:
    python3 scripts/validate_release_contract.py DOCUMENT [DOCUMENT ...]
    python3 scripts/validate_release_contract.py --schema PATH DOCUMENT
    python3 scripts/validate_release_contract.py --github DOCUMENT   # ::error:: lines

Exit status:
    0  every document validates
    1  at least one document is invalid (every error is printed, not just the first)
    2  usage error, unreadable file, or an unsupported schema keyword
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

DEFAULT_SCHEMA = pathlib.Path(__file__).resolve().parent.parent / "release" / "contract.schema.json"

# Annotations carry no assertion. Everything else must be implemented.
ANNOTATIONS = frozenset(
    {"$schema", "$id", "$anchor", "$comment", "$defs", "title", "description",
     "default", "examples", "deprecated", "readOnly", "writeOnly"}
)


class UnsupportedKeyword(Exception):
    """A schema used a keyword this checker does not implement."""


def json_type(value):
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "integer" if value.is_integer() else "number"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


def type_matches(value, expected):
    actual = json_type(value)
    if expected == "number":
        return actual in ("integer", "number") and not isinstance(value, bool)
    if expected == "integer":
        return actual == "integer" and not isinstance(value, bool)
    return actual == expected


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def resolve_ref(ref, root):
    if not ref.startswith("#/"):
        raise UnsupportedKeyword("only local JSON pointers are supported, got %r" % ref)
    node = root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            node = node[int(token)]
        else:
            node = node[token]
    return node


def escape(token):
    return str(token).replace("~", "~0").replace("/", "~1")


def validate(value, schema, root, pointer="", errors=None):
    """Collect every violation of `schema` by `value`. Returns a list of strings."""
    if errors is None:
        errors = []
    if schema is True or schema == {}:
        return errors
    if schema is False:
        errors.append("%s: no value is allowed here" % (pointer or "/"))
        return errors

    def fail(message):
        errors.append("%s: %s" % (pointer or "/", message))

    for keyword in schema:
        if keyword in ANNOTATIONS:
            continue
        if keyword not in KEYWORDS:
            raise UnsupportedKeyword(
                "schema keyword %r at %s is not implemented by this checker"
                % (keyword, pointer or "/")
            )

    if "$ref" in schema:
        validate(value, resolve_ref(schema["$ref"], root), root, pointer, errors)

    if "type" in schema:
        expected = schema["type"]
        options = expected if isinstance(expected, list) else [expected]
        if not any(type_matches(value, option) for option in options):
            fail("expected type %s, got %s" % ("/".join(options), json_type(value)))
            return errors  # every other assertion would just be noise

    if "const" in schema and value != schema["const"]:
        fail("must equal %s, got %s" % (canonical(schema["const"]), canonical(value)))
    if "enum" in schema and not any(value == option for option in schema["enum"]):
        fail("must be one of %s, got %s" % (canonical(schema["enum"]), canonical(value)))

    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            fail("%s does not match pattern %s" % (canonical(value), schema["pattern"]))
        if "minLength" in schema and len(value) < schema["minLength"]:
            fail("shorter than minLength %d" % schema["minLength"])
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            fail("longer than maxLength %d" % schema["maxLength"])

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            fail("%s is below minimum %s" % (value, schema["minimum"]))
        if "maximum" in schema and value > schema["maximum"]:
            fail("%s is above maximum %s" % (value, schema["maximum"]))
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            fail("%s is not greater than %s" % (value, schema["exclusiveMinimum"]))
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            fail("%s is not less than %s" % (value, schema["exclusiveMaximum"]))
        if "multipleOf" in schema and schema["multipleOf"] and value % schema["multipleOf"]:
            fail("%s is not a multiple of %s" % (value, schema["multipleOf"]))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            fail("has %d item(s), minItems is %d" % (len(value), schema["minItems"]))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            fail("has %d item(s), maxItems is %d" % (len(value), schema["maxItems"]))
        if schema.get("uniqueItems"):
            seen = {}
            for index, item in enumerate(value):
                key = canonical(item)
                if key in seen:
                    fail("items %d and %d are identical (uniqueItems)" % (seen[key], index))
                else:
                    seen[key] = index
        if "items" in schema:
            for index, item in enumerate(value):
                validate(item, schema["items"], root, "%s/%d" % (pointer, index), errors)
        if "contains" in schema and not any(
            not validate(item, schema["contains"], root, pointer, []) for item in value
        ):
            fail("no item satisfies `contains` %s" % canonical(schema["contains"]))

    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                fail("missing required property %r" % name)
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            fail("has %d propert(ies), minProperties is %d" % (len(value), schema["minProperties"]))
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            fail("has %d propert(ies), maxProperties is %d" % (len(value), schema["maxProperties"]))
        properties = schema.get("properties", {})
        for name, child in value.items():
            if name in properties:
                validate(child, properties[name], root, "%s/%s" % (pointer, escape(name)), errors)
            elif schema.get("additionalProperties") is False:
                fail("property %r is not allowed here (additionalProperties is false)" % name)
            elif isinstance(schema.get("additionalProperties"), dict):
                validate(child, schema["additionalProperties"], root,
                         "%s/%s" % (pointer, escape(name)), errors)

    for subschema in schema.get("allOf", []):
        validate(value, subschema, root, pointer, errors)
    if "anyOf" in schema and not any(
        not validate(value, subschema, root, pointer, []) for subschema in schema["anyOf"]
    ):
        fail("matches none of the anyOf alternatives")
    if "oneOf" in schema:
        matched = [index for index, subschema in enumerate(schema["oneOf"])
                   if not validate(value, subschema, root, pointer, [])]
        if len(matched) != 1:
            fail("matches %d of the %d oneOf alternatives, must match exactly 1 (value: %s)"
                 % (len(matched), len(schema["oneOf"]), canonical(value)))
    if "not" in schema and not validate(value, schema["not"], root, pointer, []):
        fail("must NOT match %s" % canonical(schema["not"]))
    if "if" in schema:
        if not validate(value, schema["if"], root, pointer, []):
            if "then" in schema:
                validate(value, schema["then"], root, pointer, errors)
        elif "else" in schema:
            validate(value, schema["else"], root, pointer, errors)

    return errors


KEYWORDS = frozenset(
    {"$ref", "type", "const", "enum", "required", "properties", "additionalProperties",
     "items", "minItems", "maxItems", "uniqueItems", "contains", "minProperties",
     "maxProperties", "pattern", "minLength", "maxLength", "minimum", "maximum",
     "exclusiveMinimum", "exclusiveMaximum", "multipleOf", "allOf", "anyOf", "oneOf",
     "not", "if", "then", "else"}
)


def load(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit("not found: %s" % path)
    except (OSError, ValueError) as exc:
        raise SystemExit("cannot read %s: %s" % (path, exc))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("documents", nargs="+", metavar="DOCUMENT")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--github", action="store_true",
                        help="emit GitHub Actions ::error file=...:: annotations")
    args = parser.parse_args(argv)

    schema = load(args.schema)
    invalid = 0
    for document_path in args.documents:
        document = load(document_path)
        try:
            errors = validate(document, schema, schema)
        except UnsupportedKeyword as exc:
            print("FATAL: %s" % exc, file=sys.stderr)
            return 2
        if errors:
            invalid += 1
            for message in errors:
                if args.github:
                    print("::error file=%s::release contract invalid at %s" % (document_path, message))
                else:
                    print("%s: INVALID at %s" % (document_path, message))
        else:
            print("%s: valid against %s" % (document_path, args.schema))
    if invalid:
        print("%d of %d document(s) failed validation." % (invalid, len(args.documents)))
    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())
