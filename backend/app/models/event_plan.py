from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class EventPlan(Base):
    __tablename__ = "EVENT_PLANS"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("EVENTS.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(30), nullable=False, default="ACTIVE")
    is_current = Column(Boolean, nullable=False, default=False)
    total_budget = Column(Numeric(18,2))
    created_by = Column(Integer, ForeignKey("USERS.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class EventPlanDraft(Base):
    __tablename__ = "EVENT_PLAN_DRAFTS"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("EVENTS.id"), nullable=False, index=True)
    title = Column(String(255))
    input_snapshot = Column(Text, nullable=False)
    output_json = Column(Text, nullable=False)
    model_name = Column(String(100))
    status = Column(String(30), nullable=False, default="GENERATED")
    applied_plan_id = Column(Integer, ForeignKey("EVENT_PLANS.id"))
    created_by = Column(Integer, ForeignKey("USERS.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class PlanDepartment(Base):
    __tablename__ = "PLAN_DEPARTMENTS"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("EVENT_PLANS.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    recommended_staff_count = Column(Integer)
    responsibilities = Column(Text)

class PlanTask(Base):
    __tablename__ = "PLAN_TASKS"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("EVENT_PLANS.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_department_id = Column(Integer, ForeignKey("PLAN_DEPARTMENTS.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(20), nullable=False, default="MEDIUM")
    estimated_hours = Column(Numeric(8,2))
    start_date = Column(DateTime)
    due_date = Column(DateTime)
    sort_order = Column(Integer, nullable=False, default=0)

class PlanTimelineItem(Base):
    __tablename__ = "PLAN_TIMELINE_ITEMS"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("EVENT_PLANS.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    sort_order = Column(Integer, nullable=False, default=0)

class PlanBudgetItem(Base):
    __tablename__ = "PLAN_BUDGET_ITEMS"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("EVENT_PLANS.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Numeric(12,2))
    unit_cost = Column(Numeric(18,2))
    estimated_amount = Column(Numeric(18,2), nullable=False)
    notes = Column(Text)
