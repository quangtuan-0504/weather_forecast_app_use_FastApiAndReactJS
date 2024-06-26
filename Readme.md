Hãy đảm bảo bạn đã cài đặt python 3 và có các trình soạn code như Vscode or pycharm để thuận tiện cho việc viết mã.
Các bước chạy mã:
- B1 : Chọn folder A để chứa repo, git clone repo về folder đó.
    Mở cmd, power shell, or terminal trong vscode , pycharm. cd vào A và gõ :
    git clone https://github.com/quangtuan-0504/weather_forecast_app_use_FastApiAndReactJS.git
    Or nếu bạn đang dùng window mở thư mục A, trên thanh đường dẫn gõ cmd->enter sẽ trực tiếp mở cmd ở thư mục A luôn mà không cần cd.
    Sau khi chạy lệnh này sẽ thấy thư mục weather_forecast_app_use_FastApiAndReactJS được tải về.
- B2 : Cài đặt môi trường ảo để chứa các gói thư viện cần thiết, tránh cài đặt trên python toàn cục sẽ dễ gây xunh đột sau này
    Giả sử bạn đang dùng vscode thì hãy mở terminal của vscode lên.
    Nếu đang đứng ở A.
    cd weather_forecast_app_use_FastApiAndReactJS
    Để tạo virtual env.
    python -m venv venv
    Để kích hoạt venv
    ./venv/Script/Activate
- B3 : Cài đặt các thư viện trong file requirements.txt
    pip install -r requirements.txt
- B4 : Phần backend xong, tiếp theo cần cài đặt cho phần frontend.
    Trong Worrkspace của Vscode mở folder weather_forecast_app_use_FastApiAndReactJS
    npx create-react-app frontend_weather
    cd weather-frontend
    npm install axios
    Sau khi chạy các lệnh này sẽ xuất hiện folder frontend_weather. 
    Copy code từ các file trong frontend_tmp qua các file tương tứng trong frontend_weather/src
    Trong file package.json hãy thêm "proxy": "http://localhost:8000"

    Cấu trúc thư mục có vẻ sẽ như sau.
    weather_forecast_app_use_FastApiAndReactJS/
    ├── backend_weather/
    │   ├── backend.py
    ├── ...
    ├── frontend_weather/
    │   ├── public/
    │   ├── src/
    │   ├── package.json
    │   └── ...
    ├── venv/
    └── requirements.txt
B5 : Hãy mở 2 terminal trong Vscode. Một cho backend và 1 cho frontend.
    Trong terminal 1 chạy:
     .\venv\Scripts\activate
     cd backend_wearther
     uvicorn backend:app --reload
    Trong terminal 2 chạy:
     cd frontend_weather
     npm start



















































