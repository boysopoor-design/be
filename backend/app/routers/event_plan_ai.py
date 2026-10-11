import json, os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.event import Event
from app.models.event_plan import EventPlanDraft

router = APIRouter(prefix="/api/events", tags=["AI Event Planner"])

def build_plan(event, user_input=None):
    context = {"name": event.name, "event_type": event.event_type, "description": event.description, "location": event.location, "event_date": str(event.event_date) if event.event_date else None, "attendees": event.attendees, "budget_vnd": float(event.budget or 0), "additional_request": user_input or ""}
    prompt = "Create a practical event master plan. Return ONLY JSON with keys summary, concept, objectives (array), resource_gaps (array of objects name/current/required/recommendation), departments (array of objects name/staff/responsibilities), timeline (array of objects phase/task/due), budget_items (array of objects category/amount/notes), risks (array). Use Vietnamese. Context: " + json.dumps(context, ensure_ascii=False)
    model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    try:
        import requests
        response=requests.post(os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate"), json={"model":model,"prompt":prompt,"stream":False,"format":"json"}, timeout=90)
        response.raise_for_status(); raw=response.json().get("response", "{}")
        result=json.loads(raw)
        source="ollama:"+model
    except Exception as exc:
        # Do not silently present a static template as a real AI result.
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable. Please check that Ollama is running and the configured model is installed, then try again.") from exc
    return context, result, source

@router.post("/{event_id}/ai/generate-plan")
def generate_event_plan(event_id:int, payload:dict|None=None, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    event=db.query(Event).filter(Event.id==event_id, Event.created_by==current_user.id).first()
    if not event: raise HTTPException(status_code=404, detail="Event not found")
    context, result, source=build_plan(event, (payload or {}).get("request"))
    draft=EventPlanDraft(event_id=event.id,title=f"AI plan — {event.name}",input_snapshot=json.dumps(context,ensure_ascii=False),output_json=json.dumps(result,ensure_ascii=False),model_name=source,status="GENERATED",created_by=current_user.id)
    try:
        db.add(draft); db.commit(); db.refresh(draft)
    except Exception as e:
        db.rollback(); raise HTTPException(status_code=500,detail="AI created a result but the draft could not be saved. Please retry or contact support if the issue continues.") from e
    return {"draft_id":draft.id,"event_id":event.id,"status":draft.status,"model":source,"input":context,"plan":result,"notice":"Bản kế hoạch được lưu ở dạng draft; cần người dùng rà soát trước khi áp dụng."}

@router.get("/{event_id}/ai/drafts")
def list_event_plan_drafts(event_id:int, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    event=db.query(Event).filter(Event.id==event_id, Event.created_by==current_user.id).first()
    if not event: raise HTTPException(status_code=404,detail="Event not found")
    drafts=db.query(EventPlanDraft).filter(EventPlanDraft.event_id==event_id,EventPlanDraft.created_by==current_user.id).order_by(EventPlanDraft.created_at.desc()).all()
    return [{"id":d.id,"title":d.title,"status":d.status,"model":d.model_name,"created_at":d.created_at,"plan":json.loads(d.output_json)} for d in drafts]
