from datetime import datetime

import uuid

from sqlmodel import Field, SQLModel, Relationship


class TagInfoLink(SQLModel, table=True):
    __tablename__ = "tag_info_link"
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
    info_id: int | None = Field(default=None, foreign_key="info.id", primary_key=True)


class TagReportLink(SQLModel, table=True):
    __tablename__ = "tag_report_link"
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
    info_id: int | None = Field(default=None, foreign_key="report.id", primary_key=True)


class TagOperationLink(SQLModel, table=True):
    __tablename__ = "tag_report_link"
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
    operation_id: int | None = Field(default=None, foreign_key="operation.id", primary_key=True)


class TagBase(SQLModel):
    name: str = Field(unique=True)


class Tag(TagBase, table=True):
    __tablename__ = "tag"

    id: int | None = Field(default=None, primary_key=True)
    description: str | None = None

    infos: list["LoadInfo"] = Relationship(back_populates="tags", link_model=TagInfoLink)
    reports: list["Report"] = Relationship(back_populates="tags", link_model=TagReportLink)
    operations: list["Report"] = Relationship(back_populates="tags", link_model=TagOperationLink)


class MetricBase(SQLModel):
    name: str = Field(unique=True)


class Metric(MetricBase, table=True):
    __tablename__ = "metric"

    id: int = Field(default=None, primary_key=True)
    description: str | None = None


class LoadInfoBase(SQLModel):
    uuid: uuid.UUID
    id_plan: int | None = Field(default=None)
    name: str
    start_datetime: datetime
    end_datetime: datetime
    description: str | None = None


class LoadInfo(LoadInfoBase, table=True):
    __tablename__ = "info"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    report: "Report" | None = Relationship(back_populates="info")
    tags: list["Tag"] | None = Relationship(back_populates="infos", link_model=TagInfoLink)


class OperationBase(SQLModel):
    pass


class Operation(OperationBase, table=True):
    __tablename__ = "operation"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    description: str | None = None

    report: "Report" = Relationship(back_populates="operation")
    tags: list["Tag"] = Relationship(back_populates="operations", link_model=TagOperationLink)


class ReportBase(SQLModel):
    pass


class Report(ReportBase, table=True):
    __tablename__ = "report"

    id: int = Field(primary_key=True)
    id_info: int = Field(foreign_key="info.id")
    id_operation: int = Field(foreign_key="operation.id")
    id_metric: int = Field(foreign_key="metric.id")
    metric_value: float

    info: "LoadInfo" = Relationship(back_populates="report")
    operation: "Operation" = Relationship(back_populates="report")
    metric: "Metric" = Relationship(back_populates="report")
    tags: list["Tag"] | None = Relationship(back_populates="reports", link_model=TagReportLink)
