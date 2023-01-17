from ...api.schema import BaseSchema

class Application(BaseSchema):
    name: str
    secret: str

bubble_admin = Application(name="bubble_admin", secret="ebf08004501c6175f8d6cfd1d25a0397")
dev_app = Application(name="dev_api", secret="ada3a679abf982b4c2a773631c70e1f1")
prod_app = Application(name="production-api", secret="85d142e47033c003b715052ca4a18cde")

applications = [bubble_admin, dev_app]
    