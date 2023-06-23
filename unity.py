import brotli
import gzip

def patchContent(file_name, file_content):
  modifiAble= False  
  if file_name.find(".js.unityweb")!= -1:
    modifiAble= True
  if file_name.find("framework.unityweb")!= -1:
    modifiAble= True
  if not modifiAble:
    return file_content
  try:
    data_brotli = brotli.decompress(file_content)
  except:
    try:
      data_gzip= gzip.decompress(file_content)
    except:
      pass
    else:
      file_content= data_gzip
      open("patch.txt", "a").write(file_name + "\ngzip Decompress"+ "\n\n")
  else:
    file_content= data_brotli  
    open("patch.txt", "a").write(file_name + "\nbrotli Decompress"+ "\n\n")  
  return file_content
  