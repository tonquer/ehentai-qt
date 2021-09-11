import json
import os

# fw = open("resources.py", "w+")
# fw.write("import base64\n\n\n")
# fw.write("class DataMgr(object):\n")

files = {}
for root, dirs, filenames in os.walk("./"):
    for name in filenames:
        if name[-2:] != "md":
            continue
        if len(name.split(".")) >= 3:
            continue
        f = open(name, "r", encoding='utf-8')
        # fw.write("def get():\r\n    return )
        i = 0
        info = {}
        info['data'] = {}
        while True:
            data = f.readline()
            if not data:
                break
            data = data.replace("\\|", "、")
            data2 = data.split("|")
            if len(data2) <= 4:
                data2 = data.split(":")
                if len(data2) < 2:
                    continue
                elif data2[0] == "name":
                    name = data2[1].strip("\n").strip(" ")
                    info['name'] = name
                elif data2[0] == "key":
                    key = data2[1].strip("\n").strip(" ")
                    info['key'] = key
                elif data2[0] == "description":
                    description = data2[1].strip("\n").strip(" ")
                    info['description'] = description
                continue
            else:
                # 原始标签
                srcLabel = data2[1].strip(" ")
                if srcLabel == "原始标签" or srcLabel == "" or srcLabel == "--------":
                    continue
                # 名称
                destLabel = data2[2].strip(" ")
                if "!" in destLabel:
                    destLabelList = destLabel.split(")")
                    if len(destLabelList) >= 2:
                        destLabel = destLabelList[1]

                # 描述
                misc = data2[3].strip(" ")
                # link
                link = data2[4].strip(" ")
                info["data"][srcLabel] = {
                    "src": srcLabel,
                    "dest": destLabel,
                    "description": misc,
                    "link": link
                }
                pass

        files[info.get("key")] = info
        # data = base64.b64encode(f.read())
        # if i % 2 == 0:
        #     fw.write("\\x")
        # fw.write("  {}".format(name[:-4]))
        # files.append(name[:-4])
        # fw.write(" = \"")
        # fw.write(data.decode("utf-8"))
        # fw.write("\"\n\n")

        # f.close()
f = open("translate.json", "w")
f.write(json.dumps(files))
f.close()
# fw.write("  files = {}\n\n".format(files))
# fw.write("  @classmethod\n")
# fw.write("  def GetData(cls, name):\n")
# fw.write("      data = getattr(cls, name)\n")
# fw.write("      return base64.b64decode(data.encode('utf-8'))\n")
# fw.close()
