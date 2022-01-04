
  
# save_path_file = "/Users/mac/GitHub/TextDetection/output/1.xml"
  
import etree.ElementTree as gfg



def GenerateXML(path,fileNameOutput,lst,count) :
	
	root = gfg.Element("annotation")
	
	m1 = gfg.Element("folder")
	m1.text = "input"
	root.append (m1)
	m2 = gfg.Element("filename")
	file = str(fileNameOutput).split('.')[0].split('_')[1]+'.jpg'
	print(file)
	m2.text = file
	root.append (m2)
	m3 = gfg.Element("path")
	m3.text = str(path)+file
	root.append (m3)
	m4 = gfg.Element("source")
	root.append (m4)
	
	b1 = gfg.SubElement(m4, "database")
	b1.text = "Unknown"
	
	m5 = gfg.Element("size")
	root.append (m5)
	
	c1 = gfg.SubElement(m5, "width")
	c1.text = "1044"
	c2 = gfg.SubElement(m5, "height")
	c2.text = "168"
	c3 = gfg.SubElement(m5, "depth")
	c3.text = "1"
	
	m6 = gfg.Element("segmented")
	m6.text = "0"
	root.append (m6)
	
	for i in range(count):
		m7 = gfg.Element("object")
		root.append (m7)

		d1 = gfg.SubElement(m7, "name")
		d1.text = "Text"
		d2 = gfg.SubElement(m7, "pose")
		d2.text = "Unspecified"
		d3 = gfg.SubElement(m7, "truncated")
		d3.text = "0"
		d4 = gfg.SubElement(m7, "difficult")
		d4.text = "0"
		d5 = gfg.SubElement(m7, "bndbox")
        
		d11 = gfg.SubElement(d5, "xmin")
		d11.text = lst[i,0]
		d12 = gfg.SubElement(d5, "ymin")
		d12.text = lst[i,1]
		d13 = gfg.SubElement(d5, "xmax")
		d13.text = lst[i,2]
		d14 = gfg.SubElement(d5, "ymax")
		d14.text = lst[i,3]
	
 
	tree = gfg.ElementTree(root)
	# tree.parse(pretty_print = True)
	# xml_str = tree.toprettyxml(indent ="\t")
    
	gfg.indent(tree, space='\t', level=0)
	with open (path+'labelled/'+str(fileNameOutput).split('.')[0].split('_')[1]+'.xml', "wb") as files :
		tree.write(files)

def read_text(fileNameInput):
    print(fileNameInput)
    import numpy as np
    A=np.array([0,0,0,0])
    file1 = open(fileNameInput, 'r')
    Lines = file1.readlines()
    lst = []
    count = 0
    # Strips the newline character
    for line in Lines:
        print("Line is:", line)
        count += 1
        lst = line.split(',')
        lst2 = [lst[0],lst[1],lst[4],lst[5]]
        A = np.vstack([A,lst2])
    A = np.delete(A,0,0)
    return A,count

# Driver Code
if __name__ == "__main__":
    mypath = '/Users/mac/GitHub/TextDetection/input/'
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    for item in onlyfiles:
        lst1, count1 = read_text(mypath+item)
        GenerateXML(mypath,item,lst1,count1)