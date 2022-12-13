import dpkt
import socket
import pygeoip

GIP = pygeoip.GeoIP('GeoLiteCity.dat')

def main():
    f = open('data.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    kmlHeader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="routeLines">' \
                '<LineStyle>' \
                '<width>2.5</width>' \
                '<color>50780078</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlFooter = '</Document>\n</kml>\n'
    kmlDoc=kmlHeader+plotIPs(pcap)+kmlFooter
    print(kmlDoc)

def plotIPs(pcap):
    kmlPlots = ''
    for (ts, bs) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(bs)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = genKML(dst, src)
            kmlPlots = kmlPlots + KML
        except:
            pass
    return kmlPlots

def genKML(destip, srcip):
    dest = GIP.record_by_name(destip)
    src = GIP.record_by_name('xxx.xxx.xxx.xxx')
    try:
        destlongitude = dest['longitude']
        destlatitude = dest['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#routeLines</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(destip, destlongitude, destlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

if __name__ == '__main__':
    main()