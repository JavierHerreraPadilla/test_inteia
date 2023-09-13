from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .models import Base
from app.database import SessionLocal, engine
from . import schemas, models


Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=List[schemas.Event])
def get_events(checked: bool | None = None, event_type: schemas.EventType = schemas.EventType.alls, db: Session = Depends(get_db)):
    """
    obtener una lista de eventos. Puedes filtrar los eventos por su estado de "checked" y su tipo de evento. 
    Si no se proporciona ningún filtro o query paramenter, se devolverán todos los eventos.
    """
    event_filter = event_type.value if event_type.value != "all" else "%" 
    checked_filter = checked
    if checked is None:
        events = db.query(models.Event).filter(models.Event.type.like(event_filter)).all()
    else:
        events = db.query(models.Event).filter_by(checked=checked_filter).filter(models.Event.type.like(event_filter)).all()
    return events


@app.get("/event/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    obtener un evento específico por su ID. Si el evento no existe, devuelve un error 404. 
    Si el evento no está marcado como "checked", lo marca como "checked" y actualiza el campo "work" (requiere o no requiere gestión) según su tipo.
    """
    event = db.query(models.Event).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not event.checked:
        event.checked = True
        if event.type in ["commercial", "service"]:
            event.work = True
        else:
            event.work = False
        db.commit()
        event = db.query(models.Event).get(event_id)
    return event


@app.post("/create_event", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """
    crea un nuevo evento. 
    Se espera un objeto JSON que contiene los detalles del evento, como nombre, tipo, descripción y fecha. Luego, el evento se agrega a la base de datos y se devuelve como respuesta.
    """
    new_event = models.Event(
        name=event.name,
        type=event.type.value,
        description=event.description,
        event_date=event.event_date,
    )
    db.add(new_event)
    db.commit()
    return new_event


@app.patch("/check-event/{event_id}", response_model=schemas.Event)
def check_event(event_id: int, edit_data: schemas.EventEdit, db: Session = Depends(get_db)):
    """
    actualiza un evento existente. 
    Se espera un objeto JSON con los campos que se desean actualizar. Luego, se aplican las actualizaciones al evento y se devuelve como respuesta.
    """
    event = db.query(models.Event).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for attr, value in edit_data.model_dump(exclude_unset=True).items():
        setattr(event, attr, value)
        db.commit()
        event = db.query(models.Event).get(event_id)
    return event


@app.delete("/del/{event_id}", response_model=dict)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    permite eliminar un evento por su id. 
    Si el evento no existe, se devuelve un error 404. Si se elimina con éxito, se devuelve un mensaje de confirmación.
    """
    event_to_delete = db.query(models.Event).get(event_id)
    if not event_to_delete:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event_to_delete)
    db.commit()
    return {"message": "Event deleted"}