from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import datetime
import smtplib
from email.message import EmailMessage
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn gốc. Bạn có thể giới hạn lại theo nhu cầu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = '83443e23f2854bb197a25340242406'
DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    country = Column(String)
    temperature = Column(Float)
    wind_speed = Column(Float)
    humidity = Column(Float)
    last_updated= Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    

class EmailSubscription(Base):
    __tablename__ = "email_subscription"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    confirmed = Column(Integer, default=0)
    location= Column(String, default="New york")#
class ForecastDay(BaseModel):
    date: str
    temperature: float
    wind_speed: float
    humidity: float
    condition: str

class WeatherResponse(BaseModel):
    current_time: str#
    current_temperature: float
    current_wind_speed: float
    current_humidity: float
    forecast: List[ForecastDay]

Base.metadata.create_all(bind=engine)

class WeatherRequest(BaseModel):
    city: str
    country: str

class EmailRequest(BaseModel):
    email: str
    location: str = None#

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/weather/")
def get_weather(request: WeatherRequest, db: Session = Depends(get_db)):
    city = request.city
    country = request.country
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city},{country}&days=5&lang=vi")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="City not found")
    data = response.json()

    # Lưu thời tiết hiện tại vào database
    weather = Weather(
        city=city,
        country=country,
        temperature=data['current']['temp_c'],
        wind_speed=data['current']['wind_kph'],
        humidity=data['current']['humidity'],
        last_updated=data['current']['last_updated']
    )
    db.add(weather)
    db.commit()
    db.refresh(weather)

    # Lấy dự báo thời tiết cho 4 ngày tiếp theo
    forecast = []
    for day in data['forecast']['forecastday'][1:]:
        forecast.append(ForecastDay(
            date=day['date'],
            temperature=day['day']['avgtemp_c'],
            wind_speed=day['day']['maxwind_kph'],
            humidity=day['day']['avghumidity'],
            condition=day['day']['condition']['text']
        ))

    return WeatherResponse(
        current_time=data['current']["last_updated"],#
        current_temperature=data['current']['temp_c'],
        current_wind_speed=data['current']['wind_kph'],
        current_humidity=data['current']['humidity'],
        forecast=forecast
    )
@app.get("/weather/history/")
def get_weather_history(db: Session = Depends(get_db)):
    today = datetime.datetime.utcnow().date()

    # print(type(today))
    # print(str(today))
    # print(type(str(today)))
    
    weather_today = db.query(Weather).filter(func.date(Weather.date) == today).all()
    return weather_today

@app.post("/subscribe/")
def subscribe(request: EmailRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    email = request.email
    location = request.location
    print(f"Received subscription request for email: {email}")
    
    subscription = db.query(EmailSubscription).filter(EmailSubscription.email == email).first()
    #print(subscription.email)
    if subscription:
        if subscription.confirmed == 0:
            background_tasks.add_task(send_confirmation_email, email)
            #print("message Email already subscribed. Please check your email to confirm subscription.")
            return {"message": "Email already subscribed. Please check your email to confirm subscription."}
        #print("Email already subscribed")
        raise HTTPException(status_code=400, detail="Email already subscribed and confirmed")
    new_subscription = EmailSubscription(email=email,location=location)
    db.add(new_subscription)
    db.commit()
    background_tasks.add_task(send_confirmation_email, email)
    return {"message": "Subscription request received. Please check your email to confirm subscription."}


def send_confirmation_email(email: str):
    msg = EmailMessage()
    msg.set_content("Please confirm your subscription by clicking the following link: http://localhost:8000/confirm?email=" + email)
    msg['Subject'] = 'Weather App Subscription Confirmation'
    msg['From'] = 'qttny123@gmail.com'
    msg['To'] = email
    
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.ehlo()  # Bắt đầu giao tiếp với máy chủ SMTP
        server.starttls()  # Bắt đầu mã hóa TLS
        server.ehlo()  # Giao tiếp lại với máy chủ SMTP
        server.login("qttny123@gmail.com", "cvva uczx ecwa sxuo")
        print("login successfully.")
        server.send_message(msg)
        print("Email sent successfully")
       
    

@app.get("/confirm")
def confirm_subscription(email: str, db: Session = Depends(get_db)):
    print("confirmed")
    subscription = db.query(EmailSubscription).filter(EmailSubscription.email == email).first()
    if not subscription:
        raise HTTPException(status_code=400, detail="Invalid confirmation link")
    subscription.confirmed = 1
    db.commit()
    return {"message": "Subscription confirmed"}

# Function to send daily weather updates
def send_daily_weather_updates():
    db = SessionLocal()
    subscribers = db.query(EmailSubscription).filter(EmailSubscription.confirmed == 1).all()
    for subscriber in subscribers:
        city = subscriber.location  # Ví dụ, bạn có thể thay đổi thành thành phố mặc định hoặc lấy từ cơ sở dữ liệu
        response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=4")
        if response.status_code == 200:
            data = response.json()
            weather_forecast = data['forecast']['forecastday']
            message_content = f"Weather forecast for {city}:\n"
            for day in weather_forecast:
                message_content += f"Date: {day['date']}, Max Temp: {day['day']['maxtemp_c']}°C, Min Temp: {day['day']['mintemp_c']}°C, Condition: {day['day']['condition']['text']}\n"

            msg = EmailMessage()
            msg.set_content(message_content)
            msg['Subject'] = 'Daily Weather Forecast'
            msg['From'] = 'qttny123@gmail.com'
            msg['To'] = subscriber.email

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login("qttny123@gmail.com", "cvva uczx ecwa sxuo")
                server.send_message(msg)
    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_weather_updates, 'cron', hour=22, minute=24)  # Gửi email hàng ngày vào 7 giờ sáng
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
@app.post("/unsubscribe/")
def unsubscribe(request: EmailRequest, db: Session = Depends(get_db)):
    
    email = request.email
    print(email)
    subscription = db.query(EmailSubscription).filter(EmailSubscription.email == email).first()
    if not subscription:
        raise HTTPException(status_code=400, detail="Email not found")
    
    db.delete(subscription)
    db.commit()
    return {"message": "Unsubscribed successfully"}

@app.delete("/delete_all_history_search/")
def delete_all_history_search(db: Session = Depends(get_db)):
    try:
        num_rows_deleted = db.query(Weather).delete()
        db.commit()
        return {"message": f"{num_rows_deleted} history search(s) deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_all_emails/")
def delete_all_emails(db: Session = Depends(get_db)):
    try:
        num_rows_deleted = db.query(EmailSubscription).delete()
        db.commit()
        return {"message": f"{num_rows_deleted} email(s) deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
