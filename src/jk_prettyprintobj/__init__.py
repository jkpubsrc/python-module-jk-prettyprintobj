

__version__ = "0.2020.10.23"



from .dumper import DumpMixin, Dumper, DumpCtx



def shortenText(text:str) -> str:
	if text is None:
		return None
	if len(text) > 40:
		return text[:40] + "..."
	else:
		return text

#










