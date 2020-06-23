import typing as T
from dataclasses import dataclass, field
from functools import partial
from io import StringIO

from markupsafe import Markup
M = Markup

__all__ = [
	"Node", "Markup", "M"
]

T_Child = T.Union["Node", T.Text]
T_TNode = T.TypeVar("T_TNode", bound="Node")
T_Attr = T.Any

class Html(T.Protocol):
	def __html__(self) -> str: ...

@dataclass
class TagData:
	name:     T.Optional[str]
	attrs:    T.Dict[str, T_Attr]         = field(default_factory=dict)
	children: T.Optional[T.List[T_Child]] = field(default_factory=list) # type: ignore # Mypy thinks List[_T] isn't an Optional[List[T_Child]]
	indent:   T.Optional[str]             = field(default=None)

def attrprop(name: str, f: T.Callable[[T.Any], T.Any] = lambda self: self) -> T.Any:
	return property(
		lambda self:    getattr(f(self), name),
		lambda self, v: setattr(f(self), name, v),
		lambda self:    delattr(f(self), name),
	)

class Node:
	@T.overload
	def __init__(self, data: TagData, /): ...
	@T.overload
	def __init__(self, name: T.Optional[str] = None, /, *children: T_Child, **attrs: T_Attr): ...

	def __init__(self, fst: T.Union[TagData, T.Optional[str]] = None, /, *args: T.Any, **kwargs: T.Any):
		if isinstance(fst, TagData):
			def _init_1(data: TagData) -> None:
				self._stack = [data]
			_init_1(*args, **kwargs)
		else:
			(T, str) # Workaround for bpo-39215
			def _init_2(name: T.Optional[str] = None, /, *children: T_Child, **attrs: T_Attr) -> None:
				self._stack = [TagData(name)]
				self.attr(**attrs)
				self.append(*children)
			_init_2(fst, *args, **kwargs)

	stackprop = partial(attrprop, f=lambda self: self._stack[-1])
	name:     T.Optional[str]             = stackprop("name")
	attrs:    T.Dict[str, T_Attr]         = stackprop("attrs")
	children: T.Optional[T.List[T_Child]] = stackprop("children")
	del stackprop

	def indent(self: T_TNode, v: T.Optional[str] = "\t", /) -> T_TNode:
		if v is not None and v.strip(): raise ValueError("Non-blank indentation")
		self._stack[-1].indent = v
		return self

	_parent: T.Optional[T.List[T_Child]] = None
	def append(self, *children: T_Child) -> None:
		if self.children is None: raise TypeError("Node is leaf")
		for child in children:
			if child is None: raise ValueError(child) # Won't happen in well-typed programs, but all programs aren't well-typed

			if isinstance(child, Node):
				if child._parent is not None:
					for i, e in enumerate(child._parent):
						if e is child:
							del child._parent[i]
							break
					else:
						raise ValueError("Parent doesn't recognize child")
				child._parent = self.children

			self.children.append(child)
	def extend(self, children: T.Iterable[T_Child]) -> None:
		self.append(*children)

	def text(self, *s: T.Text) -> None: self.append(*s)
	def raw(self, *s: T.Text) -> None: self.extend(s if hasattr(s, "__html__") else M(s) for s in s)

	def pop(self, n: int = -1) -> T_Child:
		if self.children is None: raise TypeError("Node is leaf")
		return self.children.pop(n)

	def __setitem__(self, k: str, v: T_Attr) -> None:
		self.attrs[k] = v
	def __getitem__(self, k: str) -> T_Attr:
		return self.attrs[k]
	def __hasitem__(self, k: str) -> bool:
		return k in self.attrs
	def __delitem__(self, k: str) -> None:
		del self.attrs[k]
	def attr(self, **attrs: T_Attr) -> None:
		self.attrs.update(self.mangleAttrs(attrs))
	def update(self, attrs: T.Dict[str, T_Attr]) -> None:
		self.attrs.update(attrs)

	def root(self: T_TNode) -> T_TNode:
		return type(self)(self._stack[0])
	def this(self: T_TNode) -> T_TNode:
		return type(self)(self._stack[-1])
	def here(self: T_TNode) -> T_TNode:
		return self.node(None)

	def node(self: T_TNode, name: T.Optional[str], /, *children: T_Child, **attrs: T_Attr) -> T_TNode:
		node = type(self)(name, *children, **attrs)
		node._parentNode = self
		self.append(node)
		return node

	def leaf(self: T_TNode, name: str, /, **attrs: T_Attr) -> T_TNode:
		node = self.node(name, **attrs)
		node.children = None
		return node

	_parentNode: T.Optional["Node"] = None
	def __enter__(self: T_TNode) -> T_TNode:
		if self._parentNode is None or not self._parentNode.children or self._parentNode.children[-1] is not self:
			raise RuntimeError("Not last child of parent, can't enter")
		self._parentNode._stack.append(self._stack[-1])
		return self

	def __exit__(self: T_TNode, *e: T.Any) -> None:
		if self._parentNode is None or self._parentNode._stack[-1] is not self._stack[-1]:
			raise RuntimeError("Not last child of parent, can't exit")
		assert self._parentNode._stack.pop() is self._stack[-1]

	def __str__(self) -> M:
		return self.dumps()
	def __repr__(self) -> str:
		return str(self._stack)

	def dump(self, f: T.TextIO) -> None:
		for s in self.__html_stream__():
			f.write(s)

	def dumps(self) -> M:
		f = StringIO()
		self.dump(f)
		return M(f.getvalue())

	__html__ = dumps

	def __html_stream__(self, indent: str = "") -> T.Iterable[M]:
		root = self._stack[0]
		if root.name is not None:
			yield M("<")
			yield M.escape(root.name)
			for k, v in root.attrs.items():
				if v is None: continue
				if v is False: continue
				yield M(" ")
				yield M.escape(k)
				if v is True: continue

				yield M("=\"")
				if isinstance(v, (list, tuple)):
					if any(not isinstance(v, str) or " " in v for v in v):
						raise ValueError(v)
					yield M.escape(" ".join(v))
				else:
					yield M.escape(v)
				yield M("\"")
			if root.children is None:
				yield M(" /")
			yield M(">")
		else:
			assert not root.attrs, repr(self)

		if root.children is not None:
			for ch in root.children:
				if root.indent is not None:
					yield M("\n" + indent+root.indent)
				if isinstance(ch, Node):
					yield from ch.__html_stream__(indent+(root.indent or ""))
				else:
					yield M.escape(ch)
			if root.name is not None:
				if root.indent is not None:
					yield M("\n" + indent)
				yield M("</")
				yield M.escape(root.name)
				yield M(">")

	@classmethod
	def mangleAttr(cls, k: str) -> str:
		if k == "cl": return "class"
		k = k.replace("_", "-")
		if k.startswith("-"): return "data" + k
		return k

	@classmethod
	def mangleAttrs(cls, attrs: T.Dict[str, T_Attr]) -> T.Dict[str, T_Attr]:
		return { cls.mangleAttr(k): v for k, v in attrs.items() }
