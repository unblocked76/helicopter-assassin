import requests
import fcntl
import os
import unity

headers_html = {
  "Content-Type":
  "text/html; charset=utf-8",
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}


def patchContent(file_name, content):
  PATCH_GUIDE = [
    "data/patch_guide.txt", "data/patch_guide_null.txt",
    "data/patch_guide_unity.txt", "data/patch_guide_ajax.txt",
    "data/patch_guide_cdn.txt", "data/patch_guide_special.txt"
  ]
  for patch_guide in PATCH_GUIDE:
    vPATCH_GUIDE_SUB = open(patch_guide).read().strip().replace(
      "\r", "").split("\n\n")
    for patch_guide_sub in vPATCH_GUIDE_SUB:
      # print("patch_guide_sub", patch_guide_sub, "\n")
      PATH_GUIDE_ITEM = patch_guide_sub.split("\n")
      dest = PATH_GUIDE_ITEM.pop()
      for source in PATH_GUIDE_ITEM:
        if content.find(source) != -1:
          content = content.replace(source, dest)
          open("patch.txt", "a").write(file_name + "\n" + patch_guide + "\n" +
                                       source + "\n" + dest + "\n\n")
  return content


def writeFile(file_name, file_content):
  global patch_found
  fw = open(file_name, "wb")
  fcntl.flock(fw, fcntl.LOCK_EX)
  if type(file_content) is str:
    textContent = file_content
    file_content = bytes(file_content, 'utf-8')
  else:
    if file_name.find(".unityweb") != -1:
      file_content = unity.patchContent(file_name, file_content)
    try:
      textContent = file_content.decode(encoding="utf-8")
    except:
      pass
    else:
      modifyContent = patchContent(file_name, textContent)
      if modifyContent != textContent:
        file_content = bytes(modifyContent, 'utf-8')
  fw.write(file_content)
  fcntl.flock(fw, fcntl.LOCK_UN)
  fw.close()
  return True


def fetchFile(path):
  print("fetchFile", path)
  game_source = open("game_source.txt").read()
  source_url = game_source.strip("/") + path
  print("--getting-- %s --" % source_url)
  try:
    res = requests.get(source_url, timeout=5)
  except:
    return False
  else:
    if res.text.find("<body>Not found at origin!") != -1:
      return False
    if res.text.find("<title>Server error</title>") != -1:
      return False
    # Make Dirs
    fw_name = os.getcwd() + "/public_html" + path
    fw_dir = os.path.split(fw_name)[0]
    try:
      os.makedirs(fw_dir)
    except:
      pass
    writeFile(fw_name, res.content)
  return True


def getIndex():
  global headers_html
  print("--cloner--getIndex--")
  game_source = open("game_source.txt").read()
  try:
    res = requests.get(game_source.strip("/") + "/",
                       headers=headers_html,
                       timeout=5)
  except:
    pass
  else:
    if res.text.find("then your request url should be as follows") != -1:
      game_source = res.text.split(
        "then your request url should be as follows")[1]
      game_source = game_source.split(">")[1]
      game_source = game_source.split("?gd_sdk_referrer_url")[0]
      game_source = game_source.replace("http://", "https://")
      game_source = game_source.replace(".com/", ".com/rvvASMiM/")
      # print("game_souce", game_source)
      writeFile("game_source.txt", game_source)
      return getIndex()
    if res.text.find("var gameSrc = \"//") != -1:
      game_source = res.text.split("var gameSrc = \"//")[1]
      game_source = "https://" + game_source.split("index.html")[0]
      writeFile("game_source.txt", game_source)
      return getIndex()
    writeFile("public_html/index.html", res.content)
