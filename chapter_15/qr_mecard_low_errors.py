from pyqrcode import QRCode

data = "WIFI:S:public-wifi-free;T:WPA;P:somepassword123;H:false;;"
q = QRCode(data, error="L")
q.png("/tmp/qr_wifi.png", scale=6)
