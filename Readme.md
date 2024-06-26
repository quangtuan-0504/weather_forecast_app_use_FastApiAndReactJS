# Hướng dẫn sử dụng weather_forecast_app_use_FastApiAndReactJS

Hãy đảm bảo bạn đã cài đặt Python 3 và có các trình soạn thảo code như VSCode hoặc PyCharm để thuận tiện cho việc viết mã.

## Các bước chạy mã:

### B1: Clone repository

- Chọn folder `A` để chứa repo, git clone repo về folder đó.
- Mở `cmd`, `PowerShell`, hoặc terminal trong VSCode, PyCharm.
- `cd` vào `A` và gõ:

    ```sh
    git clone https://github.com/quangtuan-0504/weather_forecast_app_use_FastApiAndReactJS.git
    ```

- Nếu bạn đang dùng Windows, mở thư mục `A`, trên thanh đường dẫn gõ `cmd` -> enter sẽ trực tiếp mở cmd ở thư mục `A` mà không cần `cd`.
- Sau khi chạy lệnh này sẽ thấy thư mục `weather_forecast_app_use_FastApiAndReactJS` được tải về.

### B2: Cài đặt môi trường ảo

- Giả sử bạn đang dùng VSCode thì hãy mở terminal của VSCode lên.
- Nếu đang đứng ở `A`:

    ```sh
    cd weather_forecast_app_use_FastApiAndReactJS
    ```

- Để tạo virtual environment:

    ```sh
    python -m venv venv
    ```

- Để kích hoạt virtual environment:

    ```sh
    ./venv/Scripts/activate
    ```

### B3: Cài đặt các thư viện

- Cài đặt các thư viện trong file `requirements.txt`:

    ```sh
    pip install -r requirements.txt
    ```

### B4: Cài đặt phần frontend

- Phần backend xong, tiếp theo cần cài đặt cho phần frontend.
- Trong Workspace của VSCode mở folder `weather_forecast_app_use_FastApiAndReactJS`:

    ```sh
    npx create-react-app frontend_weather
    cd frontend_weather
    npm install axios
    ```

- Sau khi chạy các lệnh này sẽ xuất hiện folder `frontend_weather`.
- Copy code từ các file trong `frontend_tmp` qua các file tương ứng trong `frontend_weather/src`.
- Trong file `package.json` hãy thêm `"proxy": "http://localhost:8000"`.

- Cấu trúc thư mục có thể sẽ như sau:
    ```
    weather_forecast_app_use_FastApiAndReactJS/
    ├── backend_weather/
    │ ├── backend.py
    ├── ...
    ├── frontend_weather/
    │ ├── public/
    │ ├── src/
    │ ├── package.json
    │ └── ...
    ├── venv/
    └── requirements.txt```

### B5: Chạy ứng dụng

- Hãy mở 2 terminal trong VSCode. Một cho backend và một cho frontend.
- Trong terminal 1 chạy:

    ```sh
    .\venv\Scripts\activate
    cd backend_weather
    uvicorn backend:app --reload
    ```

- Trong terminal 2 chạy:

    ```sh
    cd frontend_weather
    npm start
    ```



















































