from re import I
from PubPeerExtractor import PubPeerExtractor
import io
doisOrPmids = list(map(lambda x:x.strip().split("\t")[0],io.open("./papers/glioma.txt").readlines()))
pubPeerInstance = PubPeerExtractor(doisOrPmids,driverPath="./FireFoxDriver/geckodriver.exe")
pubPeerInstance.exTractFromPubpeer()
pubPeerInstance.writeToFile()