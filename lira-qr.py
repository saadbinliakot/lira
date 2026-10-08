import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

data = "https://github.com/saadbinliakot/lira.git"

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(
    fill_color="darkblue",
    back_color="lightyellow"
)

img.save("lira_qr.png")
print("QR completed.")