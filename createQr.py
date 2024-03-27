import AveryLabels, ConfigManagement
from reportlab.lib.units import mm, cm
from reportlab_qrcode import QRCodeImage








def render(c,x,y):
    global startASN
    barcode_value = f"ASN{startASN:05d}"
    barcode_value_no_asn = f"{startASN:05d}"
    startASN = startASN + 1
    
    qr = QRCodeImage(barcode_value, size=y*0.8)
    qr.drawOn(c,1*mm,y*0.05)
    c.setFont("Helvetica", 3*mm)
    c.drawString(y, (y-4*mm)/2, barcode_value)
    print(x)
    print(y)


if __name__ == "__main__":
    startASN = ConfigManagement.load_asn()
    label = AveryLabels.AveryLabel(6121)
    fname = ConfigManagement.get_output_file_path(6121, startASN)
    label.open( fname )
    label.render(render, 65 )
    label.close()
    ConfigManagement.save_asn(startASN)