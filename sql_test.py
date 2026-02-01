
from yaml import safe_load
import sqlglot
from sqlglot import expressions as exp

def clean_fabric_sql(sql: str) -> str:
    lines = []
    for line in sql.splitlines():
        line = line.strip()

        # Drop comments
        if line.startswith("--"):
            continue

        # Drop GO batch separator
        if line.upper() == "GO":
            continue

        if line:
            lines.append(line)

    return "\n".join(lines)



def load_sql(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_sql(sql: str):
    return sqlglot.parse(
        sql,
        dialect="tsql"
    )


def extract_select_expressions(tree):
    select = tree.find(exp.Select)
    assert select is not None, "No SELECT found"
    return select.expressions

def select_expression_map(expressions):
    result = {}
    for e in expressions:
        if e.alias:
            result[e.alias] = e
        elif isinstance(e, exp.Column):
            result[e.name] = e
    return result

def find_create_view_tree(trees, view_name):
    for tree in trees:
        # check if statement is CREATE
        if isinstance(tree, exp.Create):
            # create statement may be for TABLE, VIEW, etc.
            if tree.args.get("kind") == "VIEW":
                table = tree.this  # the view target
                if isinstance(table, exp.Table) and table.name == view_name:
                    return tree
    return None

def validate_contract(sql: str, contract: dict):
    trees = parse_sql(sql)
    view_tree = find_create_view_tree(trees, contract["view"])
    assert view_tree is not None, f"Missing view: {contract['view']}"

    expressions = extract_select_expressions(view_tree)
    expr_map = select_expression_map(expressions)

    # 1. Required columns
    for col in contract["columns"]:
        name = col["name"]
        if col.get("required", False):
            assert name in expr_map, f"Missing column: {name}"

    # 2. Transformation intent
    for col in contract["columns"]:
        name = col["name"]
        if "expression_contains" in col:
            expr_sql = expr_map[name].sql().upper()
            for token in col["expression_contains"]:
                assert token.upper() in expr_sql, (
                    f"Column {name} must contain '{token}'"
                )

    # 3. Forbidden patterns
    for rule in contract.get("rules", {}).get("forbid", []):
        assert rule.upper() not in sql.upper(), (
            f"Forbidden SQL pattern found: {rule}"
        )






def test_view():
    sql = load_sql("fabric/setup_silver_views.Notebook/notebook-content.sql")
    cleaned = clean_fabric_sql(sql)
    with open("contract.yaml") as f:
        contract = safe_load(f)
        validate_contract(cleaned, contract)