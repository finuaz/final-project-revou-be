from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class ToolModel(db.Model):
    __tablename__ = "Tool"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tool = db.Column(db.String(25), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    def __init__(self, tool):
        self.tool = tool

    def add_tool(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_tool(cls, tool_id):
        tool = cls.query.filter_by(id=tool_id).first()
        if tool is None:
            logging.error(f"tool with id {tool_id} not found.")
            abort(404, f"tool with id {tool_id} not found.")
        return tool

    def update_tool(self, tool_data):
        for key, value in tool_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_tool(self):
        db.session.delete(self)
        db.session.commit()
