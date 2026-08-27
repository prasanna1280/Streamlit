import ast
import operator

import streamlit as st


st.set_page_config(
	page_title="Nova Calculator",
	page_icon="+",
	layout="centered",
)

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

	:root {
		--ink: #f5f7fb;
		--muted: #9ba7b8;
		--panel: #151b27;
		--button: #202a3a;
		--line: #2d394c;
		--accent: #70e1c1;
		--accent-strong: #31b99a;
	}

	.stApp {
		background: radial-gradient(circle at 15% 10%, #20334a 0, #101722 38%, #080c13 100%);
		color: var(--ink);
		font-family: 'Space Grotesk', sans-serif;
	}

	.block-container { max-width: 620px; padding-top: 4rem; padding-bottom: 3rem; }
	h1 { font-size: 2.5rem !important; letter-spacing: 0 !important; margin-bottom: 0 !important; }
	[data-testid="stMarkdownContainer"] p { color: var(--muted); }
	.eyebrow { color: var(--accent); font: 500 0.75rem 'DM Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; }
	.subtitle { color: var(--muted); margin: 0.35rem 0 1.5rem; }
	.display {
		background: linear-gradient(135deg, #1a2636, #111722);
		border: 1px solid var(--line);
		border-radius: 18px;
		box-shadow: 0 20px 50px #00000030;
		margin: 1.25rem 0 1rem;
		padding: 1.5rem 1.75rem;
		text-align: right;
	}
	.expression { color: var(--muted); font: 500 0.9rem 'DM Mono', monospace; min-height: 1.4rem; }
	.answer { color: var(--ink); font: 500 clamp(2.4rem, 9vw, 4.4rem) 'DM Mono', monospace; overflow-wrap: anywhere; }
	.stButton > button {
		background: var(--button); border: 1px solid var(--line); border-radius: 13px;
		color: var(--ink); font: 500 1.15rem 'DM Mono', monospace; height: 3.7rem;
		transition: border-color 150ms ease, transform 150ms ease, background 150ms ease;
	}
	.stButton > button:hover { background: #2b384c; border-color: var(--accent); color: var(--ink); transform: translateY(-2px); }
	.stButton > button[kind="primary"] { background: var(--accent-strong); border-color: var(--accent); color: #071712; }
	.stButton > button[kind="primary"]:hover { background: var(--accent); color: #071712; }
	.history-title { border-bottom: 1px solid var(--line); color: var(--muted); font-size: 0.78rem; margin-top: 1.5rem; padding-bottom: 0.6rem; text-transform: uppercase; }
	.history-item { color: var(--ink); font: 400 0.9rem 'DM Mono', monospace; padding: 0.55rem 0; }
	</style>
	""",
	unsafe_allow_html=True,
)


OPERATORS = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.truediv,
}


def evaluate(expression: str) -> float:
	tree = ast.parse(expression, mode="eval")

	def calculate(node: ast.AST) -> float:
		if isinstance(node, ast.Expression):
			return calculate(node.body)
		if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
			return float(node.value)
		if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
			value = calculate(node.operand)
			return value if isinstance(node.op, ast.UAdd) else -value
		if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
			left = calculate(node.left)
			right = calculate(node.right)
			return OPERATORS[type(node.op)](left, right)
		raise ValueError("Invalid expression")

	return calculate(tree)


if "expression" not in st.session_state:
	st.session_state.expression = ""
if "answer" not in st.session_state:
	st.session_state.answer = "0"
if "history" not in st.session_state:
	st.session_state.history = []


def press(value: str) -> None:
	if value == "AC":
		st.session_state.expression = ""
		st.session_state.answer = "0"
	elif value == "DEL":
		st.session_state.expression = st.session_state.expression[:-1]
	elif value == "=":
		if not st.session_state.expression:
			return
		try:
			result = evaluate(st.session_state.expression)
			formatted = f"{result:.10g}"
			st.session_state.history.insert(0, f"{st.session_state.expression} = {formatted}")
			st.session_state.history = st.session_state.history[:5]
			st.session_state.answer = formatted
			st.session_state.expression = formatted
		except (SyntaxError, ValueError, ZeroDivisionError):
			st.session_state.answer = "Error"
	elif value == "±":
		if st.session_state.expression.startswith("-"):
			st.session_state.expression = st.session_state.expression[1:]
		else:
			st.session_state.expression = "-" + st.session_state.expression
	else:
		st.session_state.expression += value


st.markdown('<div class="eyebrow">Personal utility / 01</div>', unsafe_allow_html=True)
st.title("Nova Calculator")
st.markdown('<div class="subtitle">A calm space for quick, precise calculations.</div>', unsafe_allow_html=True)
st.markdown(
	f'<div class="display"><div class="expression">{st.session_state.expression or "Ready"}</div>'
	f'<div class="answer">{st.session_state.answer}</div></div>',
	unsafe_allow_html=True,
)


buttons = [
	[("AC", "secondary"), ("DEL", "secondary"), ("(", "secondary"), (")", "secondary")],
	[("7", "secondary"), ("8", "secondary"), ("9", "secondary"), ("/", "secondary")],
	[("4", "secondary"), ("5", "secondary"), ("6", "secondary"), ("*", "secondary")],
	[("1", "secondary"), ("2", "secondary"), ("3", "secondary"), ("-", "secondary")],
	[("0", "secondary"), (".", "secondary"), ("±", "secondary"), ("+", "secondary")],
]

for row_index, row in enumerate(buttons):
	columns = st.columns(4, gap="small")
	for column, (label, kind) in zip(columns, row):
		with column:
			if st.button(label, key=f"button_{row_index}_{label}", use_container_width=True):
				press(label)
				st.rerun()

equals_column, _ = st.columns([1, 3])
with equals_column:
	if st.button("=  Calculate", type="primary", use_container_width=True):
		press("=")
		st.rerun()

if st.session_state.history:
	st.markdown('<div class="history-title">Recent calculations</div>', unsafe_allow_html=True)
	for item in st.session_state.history:
		st.markdown(f'<div class="history-item">{item}</div>', unsafe_allow_html=True)
