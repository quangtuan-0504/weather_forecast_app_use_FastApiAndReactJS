import React, { useState } from 'react';
import axios from 'axios';


function WeatherForecastApp() {
    const [city, setCity] = useState('');
    const [country, setCountry] = useState('');
    const [weather, setWeather] = useState(null);
    const [email, setEmail] = useState('');
    const [location, setLocation] = useState('');
    const [history, setHistory] = useState([]);

    const getWeather = async () => {
        const response = await axios.post('http://localhost:8000/weather/', { city, country });
        setWeather(response.data);
    };

    const getWeatherHistory = async () => {
        const response = await axios.get('http://localhost:8000/weather/history/');
        setHistory(response.data);
    };

    const subscribe = async () => {
        
        try {
            await axios.post('http://localhost:8000/subscribe/', { email, location });
            alert("Please check your email to confirm subscription.");
        } catch (error) {
            if (error.response) {
                alert(`Subscription failed: ${error.response.data.detail}`);
            } else {
                alert('Subscription failed: Network error');
            }
        }
    };

    const unsubscribe = async () => {
        console.log(email)
        try {
            await axios.post('http://localhost:8000/unsubscribe/', { email});
            alert("Unsubscribed successfully.");
        } catch (error) {
            if (error.response) {
                alert(`Unsubscription failed: ${error.response.data.detail}`);
            } else {
                alert('Unsubscription failed: Network error');
            }
        }
    };

    return (
        <div className="container">
            <div className="search-container">
                <input type="text" placeholder="City" value={city} onChange={e => setCity(e.target.value)} />
                <input type="text" placeholder="Country" value={country} onChange={e => setCountry(e.target.value)} />
                <button onClick={getWeather}>Search</button>
            </div>
            {weather && (
                <div className="weather-info">
                    <div className="current-weather">
                        <p>City: {weather.city}</p>
                        <p>Current Date: {weather.current_time}</p>
                        <p>Current Temperature: {weather.current_temperature}°C</p>
                        <p>Current Wind Speed: {weather.current_wind_speed} kph</p>
                        <p>Current Humidity: {weather.current_humidity}%</p>
                    </div>
                    <h2>4-Day Forecast</h2>
                    <div className="forecast">
                        {weather.forecast.map(day => (
                            <div key={day.date} className="forecast-day">
                                <p>Date: {day.date}</p>
                                <p>Temperature: {day.temperature}°C</p>
                                <p>Wind Speed: {day.wind_speed} kph</p>
                                <p>Humidity: {day.humidity}%</p>
                                <p>Condition: {day.condition}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            <div className="subscription-container">
                <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
                <input type="text" placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} />
                <button onClick={subscribe}>Subscribe</button>
                <button onClick={unsubscribe}>Unsubscribe</button>
            </div>
            <div>
                <button onClick={getWeatherHistory}>Show Weather History</button>
                {history.length > 0 && (
                    <div className="history">
                        <h3>Weather History</h3>
                        {history.map((record, index) => (
                            <div key={index} className="history-record">
                                <p>City: {record.city}</p>
                                <p>Country: {record.country}</p>
                                <p>Temperature: {record.temperature}°C</p>
                                <p>Wind Speed: {record.wind_speed} kph</p>
                                <p>Humidity: {record.humidity}%</p>
                                <p>Date: {new Date(record.date).toLocaleString()}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}


export default WeatherForecastApp;