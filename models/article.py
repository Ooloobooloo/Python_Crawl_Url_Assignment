class Article:
    def __init__(self, id=None, title=None, url=None, summary=None, content=None,
                 status=0, source_name=None, created_at=None):
        self.id = id
        self.title = title
        self.url = url
        self.summary = summary
        self.content = content
        self.status = status
        self.source_name = source_name
        self.created_at = created_at